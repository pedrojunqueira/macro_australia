from pathlib import Path

from src.config import PUBLICATIONS
from src.get_publications_issues import extract_and_load
from src.extract import download_data
from src.transform_raw import process_raw_data, process_raw_metadata
from src.transform_merge import concatenate_files
from src.transform_presentation import pbi_file

# get publication info


BASE_PATH = Path(__file__).parent

print("extracting publication data")

extract_and_load(PUBLICATIONS, BASE_PATH)

# extract (data from web)

print("downloading raw data")

download_data(BASE_PATH)

# transform raw

print("transforming raw data")


for agency in ['abs', 'rba']:
    process_raw_data(agency, BASE_PATH)
    print("transformed raw data")
    process_raw_metadata(agency, BASE_PATH)
    print("transformed raw metadata")

# transform merge

print("merging files")

concatenate_files('data', BASE_PATH)
print("merged data files and saved to database")
concatenate_files('metadata', BASE_PATH)
print("merged metadata files and saved to database")

# transform presentation

print("producing final file to pbi")

pbi_file(BASE_PATH)

print("done")
