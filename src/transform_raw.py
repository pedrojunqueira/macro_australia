from pathlib import Path
from datetime import date

import pandas as pd


def transfor_rba_files(files) -> list:
    transformed_files = []

    for file in files:
        df = pd.read_excel(file, skiprows=10, sheet_name='Data')

        df.rename(columns={'Series ID': 'Month'}, inplace=True)

        series_data = df.melt(id_vars=['Month'])

        series_data.columns = [col.lower() for col in series_data.columns]

        transformed_files.append(series_data)

    return transformed_files


def transform_abs_files(files) -> list:
    transformed_dfs = []

    for file in files:
        df = pd.read_excel(file, skiprows=9, sheet_name='Data1')

        df.rename(columns={'Series ID': 'Month'}, inplace=True)

        series_data = df.melt(id_vars=['Month'])

        series_data.columns = [col.lower() for col in series_data.columns]

        transformed_dfs.append(series_data)

    return transformed_dfs


def transform_abs_files_meta(files) -> list:
    transformed_dfs = []

    for file in files:
        df = pd.read_excel(file, sheet_name='Data1')

        df_metadata = df[:9].T

        df_metadata = df_metadata.reset_index()

        df_metadata.columns = df_metadata.iloc[0, :].to_list()

        df_metadata.drop(0, inplace=True)

        df_metadata = df_metadata.rename(columns={'Unnamed: 0': 'Content'})

        df_metadata.columns = [
            '_'.join(col.split()).replace('.', '').lower()
            for col in df_metadata.columns
        ]

        df_metadata.drop(
            columns=[
                'data_type',
                'collection_month',
                'series_start',
                'series_end',
                'no_obs',
            ],
            inplace=True,
        )

        df_metadata = df_metadata[
            ['series_id', 'content', 'frequency', 'unit', 'series_type']
        ]

        transformed_dfs.append(df_metadata)

    return transformed_dfs


def transform_rba_files_meta(files) -> list:
    transformed_dfs = []

    for file in files:
        df = pd.read_excel(file, sheet_name='Data', skiprows=1)

        df_metadata = df[:9]

        df_metadata = df_metadata.dropna(how='all')

        df_metadata = df_metadata.T

        df_metadata = df_metadata.reset_index()

        df_metadata.columns = df_metadata.iloc[0, :].to_list()

        df_metadata.drop(0, inplace=True)

        df_metadata.columns = [
            '_'.join(col.split()).replace('.', '').lower()
            for col in df_metadata.columns
        ]

        df_metadata.rename(
            columns={
                'description': 'content',
                'type': 'series_type',
                'units': 'unit',
            },
            inplace=True,
        )

        df_metadata.drop(
            columns=['title', 'source', 'publication_date'], inplace=True
        )

        df_metadata = df_metadata[
            ['series_id', 'content', 'frequency', 'unit', 'series_type']
        ]

        transformed_dfs.append(df_metadata)

    return transformed_dfs


FILE_TRANSFORMERS = {'rba': transfor_rba_files, 'abs': transform_abs_files}

METADATA_TRANSFORMERS = {
    'rba': transform_rba_files_meta,
    'abs': transform_abs_files_meta,
}


def get_latest_files(
    agency: str, data_files_path: Path, history: bool = False
) -> Path:
    folder_path = data_files_path / "source" / agency

    subdirectories = [
        subdir for subdir in folder_path.iterdir() if subdir.is_dir()
    ]

    sorted_digit_dirs = sorted(
        [
            subdir.name
            for subdir in subdirectories
            if subdir.name.isdigit() and len(subdir.name) == 8
        ],
        reverse= True
    )


    if sorted_digit_dirs:
        latest_download = sorted_digit_dirs[0]
    else:
        latest_download = None

    return (
        folder_path.glob(f'{latest_download}/*.xls*')
        if not history
        else folder_path.glob(f'history/*.xls*')
    )


def process_raw_data(
    agency: str, data_files_path: Path, history: bool = False
) -> None:
    files = (
        [file for file in get_latest_files(agency, data_files_path)]
        if not history
        else [file for file in get_latest_files(agency, data_files_path, True)]
    )
    
    file_transformer = FILE_TRANSFORMERS[agency]

    transformed_dfs = file_transformer(files)

    for i, df in enumerate(transformed_dfs):
        current_date = date.today()
        folder_date_name = current_date.strftime('%Y%m%d')
        folder_path = (
            Path(data_files_path / 'processed' / folder_date_name)
            if not history
            else Path(data_files_path / 'processed' / 'history')
        )
        if not folder_path.exists() and not history:
            folder_path.mkdir(parents=True)

        series_file_name = f'data_{files[i].name.split(".")[0]}.csv'

        sink_file_path = (
            data_files_path / 'processed' / folder_date_name / series_file_name
            if not history
            else data_files_path / 'processed' / 'history' / series_file_name
        )

        df.to_csv(sink_file_path, index=False)


def process_raw_metadata(agency: str, data_files_path: Path) -> None:
    files = [file for file in get_latest_files(agency, data_files_path)]

    file_transformer = METADATA_TRANSFORMERS[agency]

    transformed_dfs = file_transformer(files)

    for i, df in enumerate(transformed_dfs):
        current_date = date.today()
        folder_date_name = current_date.strftime('%Y%m%d')
        folder_path = Path(data_files_path / 'processed' / folder_date_name)
        if not folder_path.exists():
            folder_path.mkdir(parents=True)

        series_file_name = f'metadata_{files[i].name.split(".")[0]}.csv'

        sink_file_path = (
            data_files_path / 'processed' / folder_date_name / series_file_name
        )

        df.to_csv(sink_file_path, index=False)
