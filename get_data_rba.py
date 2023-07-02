from pathlib import Path

import pandas as pd


BASE_PATH = Path(__file__).parent
SOURCE_PATH = BASE_PATH / 'source'

excel_files = SOURCE_PATH.glob('rba/*.xls*')

for file in excel_files:

    df = pd.read_excel(file, skiprows=10, sheet_name="Data")

    df.rename(columns={"Series ID":"Month"}, inplace=True)

    series_data =  df.melt(id_vars=["Month"])
   
    series_data.columns =  [col.lower() for col in series_data.columns ]

    print(series_data.columns)
   
    series_file_name = f"data_{file.name.split('.')[0]}.csv"

    sink_file_path = BASE_PATH / 'processed' / series_file_name

    series_data.to_csv(sink_file_path, index=False)