"""
Extract LSOA data and join stop & search, LFR deployments, and IMD data to polygons 
"""
 
import pandas as pd
import geopandas as gpd
from pathlib import Path


def load_geo_df(geo_path: Path) -> gpd.GeoDataFrame:
    """
    Load GeoDataFrames from a saved file.

    Args:
        geo_path (Path): Path to the GeoDataFrame file

    Returns:
        gpd.GeoDataFrame: GeoDataFrame to be manipulated
    """
    geo_df = gpd.read_file(geo_path)

    return geo_df



def load_lsoa(zip_path: Path, shp_inside_zip: Path) -> gpd.GeoDataFrame:
    """
    Unzip, load and convert LSOA data 

    Args:
        zip_path (Path): Zip containing raw LSOA data
        shp_inside_zip (Path): Path inside zip leading to LSOAs

    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing LSOAs
    """
    lsoa_gdf = gpd.read_file(f"zip://{zip_path}!{shp_inside_zip}")

    lsoa_gdf = lsoa_gdf.to_crs("EPSG:4326")

    return lsoa_gdf


def load_imd(imd_path: Path) -> pd.DataFrame:
    """
    Load the IMD data into a DataFrame for merging 

    Args:
        imd_path (Path): Path to IMD csv

    Returns:
        pd.DataFrame: DataFrame containing IMD data 
    """
    imd_df = pd.read_csv(imd_path)

    return imd_df



def spatial_join_geo_data_to_lsoa(data_geo: gpd.GeoDataFrame, lsoa_geo: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Spatial join the lsoa polygons to a dataset 

    Args:
        data_geo (GeoDataFrame): GeoDataFrame containing police data
        lsoa_geo (GeoDataFrame): GeoDataFrame containing LSOA polygons to be joined to 

    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing the police data joined to LSOA polygons 
    """

    joined_police_data = gpd.sjoin(
    data_geo,
    lsoa_geo,
    how="left",
    predicate="within"
    )

    return joined_police_data


def count_stop_search_by_lsoa(joined_data_geo: gpd.GeoDataFrame, lsoa_geo: gpd.GeoDataFrame, year: int) -> gpd.GeoDataFrame:
    """
    Count the number of incidents per LSOA and merge into new GeoDataFrame 

    Args:
        joined_data_geo (GeoDataFrame): GeoDataFrame containing police data and LSOA polygons
        lsoa_geo (GeoDataFrame): GeoDataFrame containing LSOA data used for merging 

    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing the police data joined to LSOA polygons with a count
    """
    lsoa_counts = (
        joined_data_geo
        .groupby("LSOA11CD")
        .size()
        .reset_index(name=f"stop_search_count_{year}")
    )

    lsoa_with_counts = (
        lsoa_geo
        .merge(lsoa_counts, on="LSOA11CD", how="left")
        .fillna({f"stop_search_count_{year}": 0})
    )

    return lsoa_with_counts


def count_lfr_by_lsoa(lfr_lsoa: gpd.GeoDataFrame, lsoa_geo: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Count LFR deployments per LSOA.

    Args:
        lfr_lsoa (GeoDataFrame): GeoDataFrame containing LFR deployments and LSOA polygons
        lsoa_geo (GeoDataFrame): GeoDataFrame containing LSOA data used for merging 

    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing the LFR joined to LSOA polygons with a count
    """

    lfr_counts = (
        lfr_lsoa
        .groupby("LSOA11CD")
        .size()
        .reset_index(name="lfr_count")
    )

    lsoa_with_lfr = (
        lsoa_geo
        .merge(lfr_counts, on="LSOA11CD", how="left")
        .fillna({"lfr_count": 0})
    )

    return lsoa_with_lfr

def merge_all_data(stop_search_2025: gpd.GeoDataFrame, stop_search_2023: gpd.GeoDataFrame, lfr_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Merge all the counts per LSOA into a single GeoDataFrame for analysis.

    Args:
        stop_search_2025 (GeoDataFrame): GeoDataFrame containing 2025 stop and search counts per LSOA
        stop_search_2023 (GeoDataFrame): GeoDataFrame containing 2023 stop and search counts per LSOA
        lfr_gdf (GeoDataFrame): GeoDataFrame containing LFR counts per LSOA

    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing a unified GeoDataFrame with all the counts for each activity per LSOA 
    """

    unified_gdf = (
        stop_search_2025.merge(
            stop_search_2023[["LSOA11CD", "stop_search_count_2023"]], 
            how="left",
            on="LSOA11CD"
        )
        .merge(
            lfr_gdf[["LSOA11CD", "lfr_count"]],
            how="left",
            on="LSOA11CD"
        )
    )

    return unified_gdf

def calcualte_change_stop_search(unified_gdf: gpd.geoDataFrame) -> gpd.GeoDataFrame:
    """
    Calculate the difference between Jan-Nov 2023 stop & search statistics and Jan_nov 2025 stop & search statistics

    Args:
        unified_gdf (GeoDataFrame): the dataframe containing counts of incidends per LSOA 

    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing an additional column measuring aboslute difference in stop and search
    """
    unified_gdf["abs_difference"] = (unified_gdf["stop_search_count_2025"] - unified_gdf["stop_search_count_2023"])

    return unified_gdf


def merge_imd_with_counts(abs_difference_complete_gdf: gpd.GeoDataFrame, imd_df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Merge the IMD data (London only) with the unified dataset

    Args:
        abs_difference_complete_gdf (GeoDataFrame): the GeoDataFrame containing counts of incidends per LSOA + difference between years
        imd_df: (DataFrame): the DataFrame containing IMD information to be added (London must be extracted)

    Returns:
        gpd.GeoDataFrame: GeoDataFrame containing additional IMD data 
    """
    relevant_lsoas = abs_difference_complete_gdf['LSOA11CD'].unique()

    imd_london_df = imd_df[imd_df['LSOA11CD'].isin(relevant_lsoas)]

    merged_gdf = abs_difference_complete_gdf.merge(
        imd_london_df[['LSOA11CD', 'Index of Multiple Deprivation (IMD) Decile']],
        how='left',
        on='LSOA11CD')
    
    return merged_gdf





if __name__ == "__main__":

    in_path_2025 = Path("../data/processed/lsoa_data_2025.gpkg")
    in_path_2023 = Path("../data/processed/lsoa_data_2023.gpkg")

    in_path_lfr = Path("../data/processed/lfr_deployments.gpkg")

    in_path_imd = Path("../data/processed/imd_2019.csv")

    zip_path = Path("../data/raw/statistical-gis-boundaries-london.zip")
    shp_inside_zip_path = "statistical-gis-boundaries-london/ESRI/LSOA_2011_London_gen_MHW.shp"

    out_path = Path("../data/processed/combined_counts.gpkg")


    geo_search_2025 = load_geo_df(in_path_2025)
    geo_stop_search_2023 = load_geo_df(in_path_2023)
    lfr_geo = load_geo_df(in_path_lfr)
    lsoa_geo = load_lsoa(zip_path, shp_inside_zip_path)
    imd_df = load_imd(in_path_imd)

    joined_search_2025 = spatial_join_geo_data_to_lsoa(geo_search_2025, lsoa_geo)
    joined_stop_search_2023 = spatial_join_geo_data_to_lsoa(geo_stop_search_2023, lsoa_geo)
    joined_lfr = spatial_join_geo_data_to_lsoa(lfr_geo, lsoa_geo)

    counts_joined_search_lsoa_2025 = count_stop_search_by_lsoa(joined_search_2025, lsoa_geo, 2025)
    counts_joined_stop_search_lsoa_2023 = count_stop_search_by_lsoa(joined_stop_search_2023, lsoa_geo, 2023)
 
    lfr_counts_lsoa = count_lfr_by_lsoa(joined_lfr, lsoa_geo)

    complete_gdf_with_counts = merge_all_data(counts_joined_search_lsoa_2025, counts_joined_stop_search_lsoa_2023, lfr_counts_lsoa)

    abs_difference_complete_gdf = calcualte_change_stop_search(complete_gdf_with_counts)

    final_gdf_set = merge_imd_with_counts(abs_difference_complete_gdf, imd_df)

    final_gdf_set.to_file(out_path, driver="GPKG")

    