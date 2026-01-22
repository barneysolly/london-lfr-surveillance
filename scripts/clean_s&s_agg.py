"""
Extract Jan-Nov 2023, and Jan-Nov 2025 Stop & Search statisics, concatenate and convert to GeoDataFrame.
"""

from pathlib import Path
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def load_stop_search(folder_path: Path, year: int) -> pd.DataFrame:
    """
    Load and concatenate stop & search data from multiple CSVs using Pandas.

    Args:
        folder_path (Path): Path to the folder containing CSVs 
        year (int): flag to indicate year

    Returns:
        pd.DataFrame: Concatenated Stop and Search data
    """
    if year == 2025:
        csv_files = sorted(folder_path.glob("2025-*-metropolitan-stop-and-search.csv"))
        dataframes = []

        for file in csv_files:
            df = pd.read_csv(file)
            dataframes.append(df)

        stop_and_search_2025 = pd.concat(dataframes, ignore_index=True)

        return stop_and_search_2025
        
    elif year == 2023:
        csv_files = sorted(folder_path.glob("2023-*-metropolitan-stop-and-search.csv"))
        dataframes = []

        for file in csv_files:
            df = pd.read_csv(file)
            dataframes.append(df)

        stop_and_search_2023 = pd.concat(dataframes, ignore_index=True)

        return stop_and_search_2023
        


def convert_to_geo_data(stop_and_search_df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Convert DataFrames to GeoDataFrames.

    Args:
        stop_and_search_df (DataFrame): Dataframe to be converted 

    Returns:
        gpd.DataFrame: Geodataframe produced from conversion 
    """
    gdf = gpd.GeoDataFrame(
        stop_and_search_df,
        geometry=[Point(xy) for xy in zip(stop_and_search_df.Longitude, stop_and_search_df.Latitude)],
        crs="EPSG:4326"
    )

    return gdf


if __name__ == "__main__":

    folder_path_2025 = Path("../data/raw")
    folder_path_2023 = Path("../data/raw/stop_search_jan_nov_2023")

    out_path_2025 = Path("../data/processed/lsoa_data_2025.gpkg")
    out_path_2023 = Path("../data/processed/lsoa_data_2023.gpkg")


    stop_search_2025 = load_stop_search(folder_path_2025, 2025)
    stop_and_search_2023 = load_stop_search(folder_path_2025, 2023)

    geo_search_2025 = convert_to_geo_data(stop_search_2025)
    geo_stop_and_search_2023 = convert_to_geo_data(stop_and_search_2023)


    geo_search_2025.to_file(out_path_2025, driver="GPKG")
    geo_stop_and_search_2023.to_file(out_path_2023, driver="GPKG")

    
