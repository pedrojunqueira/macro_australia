from pathlib import Path

import pandas as pd


BASE_PATH = Path(__file__).parent
SOURCE_PATH = BASE_PATH / 'source'

excel_files = SOURCE_PATH.glob('abs/*.xls*')

for file in excel_files:

    df = pd.read_excel(file, sheet_name="Data1")

    df_metadata = df[:9].T

    df_metadata = df_metadata.reset_index()

    df_metadata.columns =  df_metadata.iloc[0,:].to_list()

    df_metadata.drop(0, inplace= True)

    df_metadata = df_metadata.rename(columns={"Unnamed: 0":"Content"})

    df_metadata.columns =  [ '_'.join(col.split()).replace('.','').lower() for col in df_metadata.columns ]

    df_metadata.drop(columns=["data_type", "collection_month", "series_start", "series_end", "no_obs"], inplace=True)

    df_metadata = df_metadata[["series_id", "content", "frequency", "unit", "series_type"]]

    metadata_file_name = f"metadata_{file.name.split('.')[0]}.csv"

    sink_file_path = BASE_PATH / 'processed' / metadata_file_name

    df_metadata.to_csv(sink_file_path, index=False)

