"""
Extract and clean IMD data from XLSX files 
"""
from pathlib import Path
import pandas as pd

def load_imd_xlsx(imd_path: Path, sheet: str) -> pd.DataFrame:
    """
    Load IMD data from an xlsx file using Pandas

    Args:
        imd_path (Path): Path to the raw IMD xlsx
        sheet (str): sheet of data to be extracted 

    Returns:
        pd.DataFrame: Extracted IMD table
    """

    deprivation_df = pd.read_excel(imd_path, sheet)
    deprivation_df = deprivation_df.rename(columns={'LSOA code (2011)': 'LSOA11CD'})

    return deprivation_df

if __name__ == "__main__":
    
    in_path = Path("'../data/raw/File_1_-_IMD2019_Index_of_Multiple_Deprivation.xlsx'")
    out_path = Path("../data/processed/imd_2019.csv")


    imd_df = load_imd_xlsx(in_path, 'IMD2019')
    imd_df.to_csv(out_path)


    