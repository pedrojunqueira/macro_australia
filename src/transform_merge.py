from pathlib import Path

import pandas as pd


def get_latest_files(data_files_path: Path) -> Path:
    folder_path = data_files_path / 'processed'

    subdirectories = [
        subdir for subdir in folder_path.iterdir() if subdir.is_dir()
    ]

    sorted_digit_dirs = sorted(
        [
            subdir.name
            for subdir in subdirectories
            if subdir.name.isdigit() and len(subdir.name) == 8
        ]
    )

    latest_download = sorted_digit_dirs[-1]

    return folder_path.glob(f'{latest_download}/*.csv*')


def concatenate_files(file_type: str, data_files_path: Path) -> None:
    processed_files = get_latest_files(data_files_path)

    file_paths = [
        file
        for file in processed_files
        if file.name.startswith(file_type) and file.name.endswith('.csv')
    ]

    history_file_paths = [
        file
        for file in (data_files_path / 'processed').glob(f'history/*.csv*')
        if file.name.startswith(file_type) and file.name.endswith('.csv')
    ]

    file_paths.extend(history_file_paths)

    dfs = []
    for file in file_paths:
        df = pd.read_csv(file)
        dfs.append(df)

    concatenated = pd.concat(dfs)

    concatenated.to_parquet(
        data_files_path / 'database' / f'{file_type}.parquet',
        index=False,
        engine='pyarrow',
    )
