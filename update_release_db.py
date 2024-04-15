import pandas as pd


releases_new = pd.read_csv('releases.csv')

print(releases_new.tail(5))

releases_new.to_parquet('releases.parquet', index=False, engine='pyarrow')

releases_parquet = pd.read_parquet('releases.parquet')

print(releases_parquet.tail(5)) 