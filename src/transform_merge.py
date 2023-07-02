from pathlib import Path

import pandas as pd


BASE_PATH = Path(__file__).parent.parent
SOURCE_PATH = BASE_PATH / 'processed'


def get_latest_files(agency: str = None) -> Path:
    folder_path = SOURCE_PATH

    if agency:
        folder_path = SOURCE_PATH / agency

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

    return folder_path.glob(f"{latest_download}/*.csv*")


def concatenate_files(file_type: str) -> None:
    processed_files = get_latest_files()

    file_paths = [
        file
        for file in processed_files
        if file.name.startswith(file_type) and file.name.endswith('.csv')
    ]

    dfs = []
    for file in file_paths:
        df = pd.read_csv(file)
        dfs.append(df)

    concatenated = pd.concat(dfs)

    concatenated.to_parquet(
        BASE_PATH / "database" / f"{file_type}.parquet",
        index=False,
        engine="pyarrow",
    )


concatenate_files("data")
concatenate_files("metadata")
