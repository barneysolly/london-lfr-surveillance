"""
Calculate key stats for plotting maps and dissecting information 
"""
 
import pandas as pd
import geopandas as gpd
from pathlib import Path


def load_data(data_path: Path) -> gpd.GeoDataFrame:
    """
    Load data, and slim into a GeoDataframe ready for analysis.

    Args:
        data_path (Path): Path to the processed data

    Returns:
        gpd.GeoDataFrame: Data ready for analysis
    """
    complete_dataset = gpd.read_file(data_path)
    complete_gdf = complete_dataset[['LSOA11CD', 'stop_search_count_2025', 'stop_search_count_2023', 'abs_change', 'lfr_count' 'Index of Multiple Deprivation (IMD) Decile', 'geometry']]

    return complete_gdf


def lfr_deployments_high_stop_search_lsoas(quantile: float, total_lfr: float, complete_gdf: gpd.GeoDataFrame) -> tuple[float, float, float]:
    """
    Calculate percentage of LFR deployments that occured in LSOAs with high stop & search activity in 2025.

    Args:
        quantile (float): quantile of stop and search activity to be analysed against
        total_lfr (float): total number of LFR deployments
        complete_gdf (GeoDataFrame): dataset for analysis

    Returns:
        float: Percentage of LFR deployments that occured in LSOAs expeicneing specific quantile of stop & search 
    """

    top_stop_search = complete_gdf['stop_search_count_2025'].quantile(quantile)

    high_stop_search_lsoas = complete_gdf[complete_gdf['stop_search_count_2025'] >= top_10_stop_search]

    lfr_in_quantile = high_stop_search_lsoas['lfr_count'].sum()

    pct_in_quantile = lfr_in_quantile / total_lfr * 100

    return top_stop_search, lfr_in_quantile, pct_in_quantile


def lfr_deployments_rising_falling(complete_gdf: gpd.GeoDataFrame, total_lfr: float) -> tuple[float, float, float, float,float,float]:
    """
    Calcualte percentage of LFR deployments that occur in LSOAs with rising, falling and stable stop & search

    Args:
        total_lfr (float): total number of LFR deployments
        complete_gdf (GeoDataFrame): dataset for analysis

    Returns:
        tuple[float]: 3 percentages for lfr deployments in areas of rising stop & search, no change and falling stop & search
    """

    rising_search = complete_gdf[complete_gdf['abs_change'] > 0]
    no_change = complete_gdf[complete_gdf['abs_change'] == 0]
    falling_search = complete_gdf[complete_gdf['abs_change'] < 0]

    lfr_rising = rising_search['lfr_count'].sum()
    lfr_no_change = no_change['lfr_count'].sum()
    lfr_falling = falling_search['lfr_count'].sum() 

    pct_in_rising = lfr_rising / total_lfr * 100 
    pct_no_change = lfr_no_change / total_lfr * 100
    pct_falling = lfr_falling / total_lfr * 100 

    return lfr_rising, lfr_no_change, lfr_falling, pct_in_rising, pct_no_change, pct_falling

def lfr_deployments_high_imd(complete_gfd: gpd.GeoDataFrame, total_lfr: float) -> tuple[float, float, float, float]:
    """
    Calcualte percentage of LFR deployments that occur in LSOAs with high levels of deprivation

    Args:
        total_lfr (float): total number of LFR deployments
        complete_gdf (GeoDataFrame): dataset for analysis

    Returns:
        tuple[float]: 2 percentages for lfr deployments in areas of different levels of deprivation measured by IMD
    """ 

    highest_decile = complete_gfd[complete_gfd['Index of Multiple Deprivation (IMD) Decile'] == 1]
    three_highest_deciles = complete_gfd[complete_gfd['Index of Multiple Deprivation (IMD) Decile'] < 4]

    hi_dec_sum = highest_decile.shape[0]
    hi_three_dec = three_highest_deciles.shape[0]

    lfr_highest = highest_decile['lfr_count'].sum()
    lfr_three_highest = three_highest_deciles['lfr_count'].sum()

    imd_lfr_pct = lfr_highest / total_lfr * 100 
    imd_three_lfr_pct = lfr_three_highest / total_lfr * 100 

    return hi_dec_sum, hi_three_dec, lfr_highest, lfr_three_highest, imd_lfr_pct, imd_three_lfr_pct

def create_dataframe_with_stats(key_stats: dict) -> pd.DataFrame:
    """
    Collate all information into a single Dataframe from a dictionary

    Args:
        key_stats (dict): dict containing key stats as floats

    Returns:
        Dataframe: Contains all the data formatted as a DataFraem 
    """ 

    stats_df = pd.DataFrame([key_stats])
    stats_df = stats_df.round(2)

    return stats_df

    

if __name__ == "__main__":
    in_path = Path("../data/prcoessed/combined_counts.gpkg")
    out_path = Path("../outputs/tables/summary_stats.csv")

    complete_dataset = load_data(in_path)

    total_lfr = complete_dataset['lfr_count'].sum()

    top_10_stop_search, lfr_in_top_10, pct_in_top_10 = lfr_deployments_high_stop_search_lsoas(0.9, complete_dataset)
    top_20_stop_search, lfr_in_top_20, pct_in_top_20 = lfr_deployments_high_stop_search_lsoas(0.8, complete_dataset)

    lfr_rising, lfr_no_change, lfr_falling, pct_in_rising, pct_no_change, pct_falling = lfr_deployments_rising_falling(complete_dataset, total_lfr)

    hi_dec_sum, hi_three_dec, lfr_highest, lfr_three_highest, imd_lfr_pct, imd_three_lfr_pct = lfr_deployments_high_imd(complete_dataset, total_lfr)

    key_stats = {
        "total_lfr": total_lfr,

        "top_10_stop_search_threshold": top_10_stop_search,
        "lfr_in_top_10": lfr_in_top_10,
        "pct_lfr_in_top_10": pct_in_top_10,

        "top_20_stop_search_threshold": top_20_stop_search,
        "lfr_in_top_20": lfr_in_top_20,
        "pct_lfr_in_top_20": pct_in_top_20,

        "lfr_rising": lfr_rising,
        "lfr_no_change": lfr_no_change,
        "lfr_falling": lfr_falling,

        "pct_lfr_rising": pct_in_rising,
        "pct_lfr_no_change": pct_no_change,
        "pct_lfr_falling": pct_falling,

        "lsoas_highest_imd_decile": hi_dec_sum,
        "lsoas_top_3_imd_deciles": hi_three_dec,

        "lfr_in_highest_imd": lfr_highest,
        "lfr_in_top_3_imd": lfr_three_highest,

        "pct_lfr_highest_imd": imd_lfr_pct,
        "pct_lfr_top_3_imd": imd_three_lfr_pct,
    }

    summary_statistics = create_dataframe_with_stats(key_stats)

    summary_statistics.to_csv(out_path)
