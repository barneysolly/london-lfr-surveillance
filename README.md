# Live Facial Recognition and Stop & Search Mapping (London, 2023–2025)

## Overview
This project analyses the spatial relationship between Live Facial Recognition (LFR) deployment locations and stop and search incidents in London. The analysis uses open data and GIS methods to explore patterns of policing intensity, change over time, and deprivation.

The main outputs are:
- Report: Analysis of the maps and summary statistics with policy related conclusions (Report - Live Facial Recognition Deployments, London 2025)
- Map 1: Stop and Search levels in 2025 with LFR deployment locations (2025_lfr_s&s)
- Map 2: Change in Stop and Search (2023–2025) with LFR deployment locations (change_over_time)
- Map 3: Deprivation (IMD) with LFR deployment locations (lfr_index_multiple_dep)
- Summary statistics table of the relationship between LFR deployment and stop and search / deprivation (Table of results)

## Data Sources
- Home Office Stop and Search (2023 and 2025)
- Metropolitan Police Service LFR deployment locations (2023–2025)
- ONS LSOA boundaries (2011)
- IMD 2019 (England)

## Tools and Software
- Python (data processing and analysis)
- QGIS (map creation and styling)

### Python Libraries
The Python environment requires the following packages (see `requirements.txt`):
- pandas
- geopandas
- shapely
- geopy
- pymupdf

## File Structure
project-folder/
│
├── data/
│   └── processed/
│       ├── 2023_stop_search_aggregated.csv
│       ├── imd_dep_london.gpkg
│       ├── lfr_clean_geo.csv
│       ├── lfr_deployments.gpkg
│       ├── lsoa_change_2023_2025.gpkg
│       ├── lsoa_stop_search.gpkg
│       └── stop_search_aggregated.csv
│
├── notebooks/
│   ├── 01_lfr_extraction.ipynb
│   ├── 02_stop_search_extraction.ipynb
│   ├── 03_LSOA_aggregation.ipynb
│   ├── 04_hist_s&s_extraction.ipynb
│   ├── 05_2023_LSOA_agg_join.ipynb
│   ├── 06_deprivation_extract_join.ipynb
│   └── 07_stats_calc.ipynb
│
├── outputs/
│   ├── maps/
│   │   ├── 2025_lfr_s&s.pdf
│   │   ├── 2025_lfr_s&s.png
│   │   ├── change_over_time.pdf
│   │   ├── change_over_time.png
│   │   ├── lfr_index_multiple_dep.pdf
│   │   └── lfr_index_multiple_dep.png
│   │
│   └── tables/
│       ├── summary_stats.csv
│       └── Table of results.pdf
│
├── scripts/
│   ├── clean_imd.py
│   ├── clean_lfr.py
│   ├── clean_s&s_agg.py
│   ├── lsoa_agg.py
│   └── stats_analysis.py
│
├── requirements.txt
├── README.md
└── Report - Live Facial Recognition Deployments, London 2025.pdf
└── Report - Live Facial Recognition Deployments, London 2025.docx

## Data Availability
Raw source datasets are not included in this repository due to size and licensing restrictions.  
Raw data can be downloaded from the original sources (see Data Sources).  
Processed datasets used in the analysis are provided in the `data/processed/` folder.

## Notes

Datasets require manual download.
https://data.police.uk/data/
https://data.london.gov.uk/dataset/lsoa-atlas-2n8zy/
https://www.met.police.uk/SysSiteAssets/media/downloads/force-content/met/advice/lfr/deployment-records/live-facial-recognition---deployment-record-2025-to-date.pdf

The stop and search dataset is limited to January–November 2025 to align with available data.

The map outputs are stored in the outputs/maps folder as both PDF and PNG.

## License / Attribution

All datasets used are publicly available from the relevant government and police sources. The maps and analysis were created by the author.

