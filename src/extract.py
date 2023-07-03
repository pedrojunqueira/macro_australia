from pathlib import Path
from datetime import date

import pandas as pd
import requests

BASE_URLS = {'abs': 'https://www.abs.gov.au', 'rba': 'https://www.rba.gov.au'}


def download_data(data_files_path: Path) -> None:
    try:
        releases = pd.read_parquet(
            data_files_path / 'database' / 'releases.parquet'
        )

        latest_releases = releases[releases['type'] == 'latest']
        for _, row in latest_releases.iterrows():
            print(f'downloading... {row["name"]}')
            agency = row['agency']
            file = row['file']
            address = row['address']
            current_date = date.today()
            folder_date = current_date.strftime('%Y%m%d')
            folder_path = Path(
                data_files_path / 'source' / agency / folder_date
            )
            if not folder_path.exists():
                folder_path.mkdir(parents=True)

            url = f'{BASE_URLS[agency]}/{address}/{file}'

            try:
                r = requests.get(url)
                with open(folder_path / file, 'wb') as fp:
                    fp.write(r.content)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
