## Australia Macro Economic Indicators

This project is a python Data Engineering pipeline to extract macro economic indicator from
ABS (Australian Bureau of Statistics) and the RBA (Reserve Bank of Australia)

### Usage

1. clone repository

`git clone https://github.com/pedrojunqueira/macro_australia.git`

2. cd into it

`cd macro_australia`

3. create a virtual environment, activate it, upgrade pip and install dependencies

`python -m venv .venv`

`source .venv/bin/activate`

`pip install --upgrade pip`

`pip install -r requirements.txt`

4. run the historical pipeline (first time one)

`python ./src/historical_data.py`

5. when latest data is required just run the main pipeline

`python pipeline.py`

### Power BI csv table for visualisation

a file will be dumped in the root folder called `final.csv` which you can use to chart and compare the main indicators

### What indicators are available in the out of the box configuration ?

| Indicator               |
| ----------------------- |
| weekly_earnings_old     |
| weekly_earnings         |
| contruction_no          |
| new_built_no            |
| existing_dwelling_no    |
| contruction_value       |
| new_built_value         |
| existing_dwelling_value |
| variable_loan_owner     |
| cash_rate               |
| cpi                     |
| unemployement_rate      |

### Folder for the data files

```bash
├── database
├── processed
├── source
```

for the first time you need to create them. For this just run

`python create_data_dirs.py`
