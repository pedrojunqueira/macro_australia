import pandas as pd

df_parquet = pd.read_parquet('pbi_file.parquet')

print(df_parquet.tail())