from pathlib import Path

import pandas as pd


BASE_PATH = Path(__file__).parent
SOURCE_PATH = BASE_PATH / 'processed'

metadata_files = SOURCE_PATH.glob('metadata*.csv*')

metadata_dfs = []
rows = 0
for file in metadata_files:
    df = pd.read_csv(file)
    metadata_dfs.append(df)
    rows += df.shape[0]

all_metadata = pd.concat(metadata_dfs)

all_metadata.to_parquet(BASE_PATH / "database" / "metadata.parquet", index=False, engine="pyarrow")

data_files = SOURCE_PATH.glob('data*.csv')

data_dfs = []

for file in data_files:
    df = pd.read_csv(file)
    data_dfs.append(df)

all_data = pd.concat(data_dfs)

all_data.to_parquet(BASE_PATH / "database" / "data.parquet", index=False, engine="pyarrow")