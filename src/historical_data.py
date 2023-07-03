from pathlib import Path

import requests

from transform_raw import process_raw_data

BASE_PATH = Path(__file__).parent.parent


def download_data(data_files_path: Path) -> None:
    weekly_earnings = 'https://www.abs.gov.au/ausstats/meisubs.NSF/log?openagent&6302002.xls&6302.0&Time%20Series%20Spreadsheet&16F1263CC960388CCA257A5B00121514&0&May%202012&16.08.2012&Latest'

    r = requests.get(weekly_earnings)

    with open(
        data_files_path / 'source' / 'abs' / 'history' / '6302002.xls', 'wb'
    ) as fp:
        fp.write(r.content)


download_data(BASE_PATH)
process_raw_data('abs', BASE_PATH, True)
