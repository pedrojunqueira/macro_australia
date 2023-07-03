from pathlib import Path


def create_data_subdirectories():
    subdirectories = ['database', 'processed', 'source']

    current_directory = Path.cwd()

    # Check if subdirectories exist, and create them if they don't

    for subdir in subdirectories:
        new_directory = current_directory / subdir
        if new_directory.exists():
            print(f"{subdir} already exist")
        else:
            print(f"{subdir} created")
            new_directory.mkdir()


if __name__ == '__main__':
    create_data_subdirectories()
