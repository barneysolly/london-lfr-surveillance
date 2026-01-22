"""
Extract and clean Live Facial Recognition deployment data from PDF files.
"""

import fitz  
import pandas as pd
import geopandas as gpd
import time
from pathlib import Path
from shapely.geometry import Point
from geopy.geocoders import Nominatim



def load_lfr(pdf_path: Path) -> pd.DataFrame:
    """
    Load LFR deployment data from a PDF file using PyMuPDF.

    Args:
        pdf_path (Path): Path to the raw LFR PDF

    Returns:
        pd.DataFrame: Extracted LFR deployment table
    """
    doc = fitz.open(pdf_path)
    all_rows = []

    for i, page in enumerate(doc):
        tabs = page.find_tables()
        
        if tabs.tables:
            raw_data = tabs[0].extract()
            
            if i == 0:
                all_rows.extend(raw_data[2:])
            else:
                all_rows.extend(raw_data[:])
        else:
            print(f"Page {i} is empty or has no table; skipping...")

    records_lfr = pd.DataFrame(all_rows)

    doc.close()

    headers = [
    'Deployment Location',
    'Date',
    'Duration',
    'LFR Use Case',
    'Watchlist Size',
    'Min Threshold Setting',
    'Total Alerts',
    'True Alerts Confirmed',
    'True Alerts Unconfirmed',
    'False Alerts Confirmed',
    'False Alerts Unconfirmed',
    'False Alert Rate',
    'Outcome - Arrest',
    'Outcome - Other',
    'No action',
    'Faces seen (estimate)']

    records_lfr = records_lfr.dropna(how='any')

    records_lfr.reset_index(drop=True, inplace=True)
    records_lfr['Deployment Location'] = records_lfr['Deployment Location'].str.replace("\n", " ")

    return pd.DataFrame(records_lfr)


def create_geometry(geo_lfr_df: pd.DataFrame) -> gpd.GeoDataFrame:
    """
    Convert LFR DataFrame to GeodataFrame

    Args:
        geo_lfr_df (DataFrame): DataFrame of LFR deployments

    Returns:
        gpd.GeoDataFrame: Geodatatframe containing geocoded LFR locations
    """

    geo_lfr_df["Deployment Location"] = (
        geo_lfr_df["Deployment Location"]
        .str.replace("’", "'", regex=False)
        .str.replace("–", "-", regex=False)
        .str.replace(r"\bSt\b", "Street", regex=True)
        .str.replace(r"\bRd\b", "Road", regex=True)
        .str.replace(r"\bSq\b", "Square", regex=True)
        .str.replace(r"\bStn\b", "Station", regex=True)
        .str.replace("B'Way", "Broadway", regex=False)
        .str.replace("Junc", "Junction", regex=False)
        .str.strip()
    )

    geolocator = Nominatim(user_agent="lfr_deployment")

    latitudes = []
    longitudes = []
    errors = []

    for i, address in enumerate(geo_lfr_df["Deployment Location"]):
        try:
            query = f"{address}, London, UK"
            location = geolocator.geocode(query)
        except Exception as e:
            print(f"Error at row {i}: {e}")
            errors.append(i)
            location = None

        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
        else:
            latitudes.append(None)
            longitudes.append(None)
            print(f"Row {i}: '{address}' could not be geocoded")

        time.sleep(1)

    geo_lfr_df["latitude"] = latitudes
    geo_lfr_df["longitude"] = longitudes

    geo_lfr_df["Deployment Location"] = (
    geo_lfr_df["Deployment Location"]
    .str.replace("Junctiontion", "Junction", regex=False)
    .str.replace("B'way", "Broadway", regex=False)
    )

    # manually assing the missing rows 
    # https://www.gps-coordinates.net/

    geo_lfr_df.loc[26, ["latitude", "longitude"]] = [51.506255, -0.220575]
    geo_lfr_df.loc[39, ["latitude", "longitude"]] = [51.51498, -0.300407]
    geo_lfr_df.loc[87, ["latitude", "longitude"]] = [51.427739, -0.16829]
    geo_lfr_df.loc[94, ["latitude", "longitude"]] = [51.51498, -0.300407]
    geo_lfr_df.loc[98, ["latitude", "longitude"]] = [51.511903, -0.014372]
    geo_lfr_df.loc[102, ["latitude", "longitude"]] = [51.531707, -0.124766]
    geo_lfr_df.loc[103, ["latitude", "longitude"]] = [51.506295, -0.231435]
    geo_lfr_df.loc[119, ["latitude", "longitude"]] = [51.509759, -0.13355]
    geo_lfr_df.loc[130, ["latitude", "longitude"]] = [51.544337, -0.00632]
    geo_lfr_df.loc[171, ["latitude", "longitude"]] = [51.543793, 0.049819]
    geo_lfr_df.loc[198, ["latitude", "longitude"]] = [51.509759, -0.13355]
    geo_lfr_df.loc[207, ["latitude", "longitude"]] = [51.507459, -0.222272]
    geo_lfr_df.loc[227, ["latitude", "longitude"]] = [51.545284, -0.074968]

    lfr_gdf = gpd.GeoDataFrame(
        geo_lfr_df,
        geometry=[Point(xy) for xy in zip(lfr_df.longitude, lfr_df.latitude)],
        crs="EPSG:4326"
    )

    return lfr_gdf


if __name__ == "__main__":
    in_path = Path("../data/raw/live-facial-recognition---deployment-record-2025-to-date.pdf")
    out_path = Path("../data/processed/lfr_deployments.gpkg")


    lfr_df = load_lfr(in_path)
    lfr_gdf = create_geometry(lfr_df)

    lfr_gdf.to_file(out_path, driver="GPKG")

    