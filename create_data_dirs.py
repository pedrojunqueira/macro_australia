from pathlib import Path


def create_data_subdirectories():
    current_directory = Path.cwd()

    subdirs = [
        'source/abs/history',
        'source/rba/history',
        'processed/history',
        'database',
    ]

    for p in subdirs:
        directory_path = current_directory / p
        directory_path.mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    create_data_subdirectories()
