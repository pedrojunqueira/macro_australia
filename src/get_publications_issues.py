from datetime import datetime, date
from collections import defaultdict, namedtuple
from pathlib import Path


from bs4 import BeautifulSoup
import requests
import pandas as pd

BASE_URLS = {
    "abs": "https://www.abs.gov.au",
    "rba": "https://www.rba.gov.au/statistics/",
}
BASE_PATH = Path(__file__).parent.parent

Release = namedtuple(
    'Release', ['agency', 'name', 'address', 'release_date', 'type', 'file']
)


publications = {
    "house_prices": (
        "abs",
        "/statistics/economy/price-indexes-and-inflation/residential-property-price-indexes-eight-capital-cities",
        "641606.xlsx",
    ),
    "weekly_earnings": (
        "abs",
        "/statistics/labour/earnings-and-working-conditions/average-weekly-earnings-australia",
        "6302002.xlsx",
    ),
    "house_finance": (
        "abs",
        "/statistics/economy/finance/lending-indicators",
        "560103.xlsx",
    ),
    "inflation": (
        "abs",
        "/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia",
        "640101.xlsx",
    ),
    "unemployment": (
        "abs",
        "/statistics/labour/employment-and-unemployment/labour-force-australia",
        "6202001.xlsx",
    ),
    "cash_rate": ("rba", "/statistics/tables/xls", "f01hist.xls"),
    "variable_home_loan": ("rba", "/statistics/tables/xls", "f05hist.xls"),
}


def get_latest_release(html: str, pub: tuple) -> list:
    agency, _, file = pub
    latests = []
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find(
        id="block-views-block-topic-releases-listing-topic-latest-release-block"
    )
    if div:
        latest_release = div.find_all('a')[0]

        if latest_release:
            address_url = latest_release["href"]
            release_month = address_url.split("/")[-1]
            try:
                dt = datetime.strptime(release_month, "%b-%Y")
                release_date = dt.strftime("%Y-%m-%d")
            except Exception:
                release_date = None
            latests.append(
                Release(
                    name=latest_release.text,
                    address=address_url,
                    type="latest",
                    release_date=release_date,
                    agency=agency,
                    file=file,
                )
            )

    return latests


def get_future_releases(html: str, pub: tuple) -> list:
    agency, address, file = pub

    future_releases = []
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find(
        id="block-views-block-topic-releases-listing-future-releases-block"
    )

    if div:
        view_content_div = div.find('div', class_='view-content')
        views_row_divs = view_content_div.find_all('div', class_='views-row')

        for views_row in views_row_divs:
            release_title = views_row.contents[0].strip()
            time_tag = views_row.find('time')
            datetime_attr = time_tag['datetime']
            dt = datetime.strptime(datetime_attr, '%Y-%m-%dT%H:%M:%SZ')
            url_extension = dt.strftime('%b-%Y')
            future_release_address = f"{address}/{url_extension.lower()}"
            future_releases.append(
                Release(
                    name=release_title,
                    release_date=datetime_attr,
                    type="future_release",
                    address=future_release_address,
                    agency=agency,
                    file=file,
                )
            )

    return future_releases


def releases_to_pd_data(release: namedtuple) -> defaultdict:
    release_data = defaultdict(list)
    d = release._asdict()
    for k, v in d.items():
        release_data[k].append(v)
    return pd.DataFrame(release_data)


def get_rba_relase(stat: str, pub: tuple) -> None:
    agency, address, file = pub
    dt = datetime.now()
    release_date = dt.strftime('%Y-%m-%d')
    latests = []
    latests.append(
        Release(
            name=stat,
            address=address,
            type="latest",
            release_date=release_date,
            agency=agency,
            file=file,
        )
    )
    return latests


def get_all_releases(publications):
    dfs = []

    for stat, pub in publications.items():
        agency, address, _ = pub
        if agency == "rba":
            latest_rba = get_rba_relase(stat, pub)
            for r in latest_rba:
                df = releases_to_pd_data(r)
                dfs.append(df)
            continue
        r = requests.get(f"{BASE_URLS[agency]}{address}")
        if r.status_code == 200:
            html = r.text

            latest_abs = get_latest_release(html, pub)
            future_abs = get_future_releases(html, pub)

            for r in future_abs:
                df = releases_to_pd_data(r)
                dfs.append(df)
            for r in latest_abs:
                df = releases_to_pd_data(r)
                dfs.append(df)

    return pd.concat(dfs)


release_df = get_all_releases(publications)

release_df.to_parquet(
    BASE_PATH / "database" / "releases.parquet", index=False, engine="pyarrow"
)
