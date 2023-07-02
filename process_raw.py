from pathlib import Path
from datetime import date

import pandas as pd

BASE_PATH = Path(__file__).parent
SOURCE_PATH = BASE_PATH / 'source'


def transfor_rba_files(files)-> list:
    
    transformed_files = []

    for file in files:

        df = pd.read_excel(file, skiprows=10, sheet_name="Data")

        df.rename(columns={"Series ID":"Month"}, inplace=True)

        series_data =  df.melt(id_vars=["Month"])
    
        series_data.columns =  [col.lower() for col in series_data.columns]

        transformed_files.append(series_data)

    return transformed_files

def transform_abs_files(files)->list:
    
    transformed_dfs = []
    
    for file in files:

        df = pd.read_excel(file, skiprows=9, sheet_name="Data1")

        df.rename(columns={"Series ID":"Month"}, inplace=True)

        series_data =  df.melt(id_vars=["Month"])

        series_data.columns =  [col.lower() for col in series_data.columns ]

        transformed_dfs.append(series_data)
    
    return transformed_dfs

FILE_TRANSFORMERS = {"rba": transfor_rba_files,
                     "abs": transform_abs_files}


def get_latest_files(agency:str)-> Path:

    folder_path = SOURCE_PATH / agency 

    subdirectories = [subdir for subdir in folder_path.iterdir() if subdir.is_dir()]

    sorted_digit_dirs = sorted([subdir.name for subdir in subdirectories if subdir.name.isdigit() and len(subdir.name) == 8])

    latest_download = sorted_digit_dirs[0]

    return folder_path.glob(f'{latest_download}/*.xls*')


def process_raw_data(agency:str)-> None:

    files = [file for file in get_latest_files(agency)]

    file_transformer = FILE_TRANSFORMERS[agency]

    transformed_dfs = file_transformer(files)

    for i, df in enumerate(transformed_dfs):

        current_date = date.today()
        folder_date_name = current_date.strftime("%Y%m%d")
        folder_path = Path(BASE_PATH / "processed" / folder_date_name)
        if not folder_path.exists():
            folder_path.mkdir(parents=True)

        series_file_name = f"data_{files[i].name.split('.')[0]}.csv"

        sink_file_path = BASE_PATH / 'processed' / folder_date_name / series_file_name

        df.to_csv(sink_file_path, index=False)

    
for agency in ["abs", "rba"]:
    process_raw_data(agency)