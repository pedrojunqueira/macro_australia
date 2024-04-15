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

4. create data folders (first time only)

for the first time you need to create them. For this just run
`python create_data_dirs.py`

### Folder for the data files are:

```bash
├── database
├── processed
│   └── history
├── source
│   ├── abs
│   │   └── history
│   └── rba
│       └── history
```

5. run the historical pipeline (first time only)

`python ./src/historical_data.py`

6. when latest data is required just run the main pipeline

`python pipeline.py`

### Power BI csv table for visualisation

a file will be dumped in the root folder called `final.csv` which you can use to chart and compare the main indicators

### What indicators are available in the out of the box configuration ?

| Indicator               | source |
| ----------------------- | ------ |
| weekly_earnings_old     | ABS    |
| weekly_earnings         | ABS    |
| contruction_no          | ABS    |
| new_built_no            | ABS    |
| existing_dwelling_no    | ABS    |
| contruction_value       | ABS    |
| new_built_value         | ABS    |
| existing_dwelling_value | ABS    |
| variable_loan_owner     | RBA    |
| cash_rate (interests)   | RBA    |
| cpi (inflation)         | ABS    |
| unemployement_rate      | ABS    |

## Power BI report

A Power BI report with the data can be viewed in this [link addrress](https://app.powerbi.com/view?r=eyJrIjoiZGI3ZjY3MmQtODY4NC00ZGIwLTliNDYtNTY1MDdmZWRkZWVhIiwidCI6ImM3NjcyNjNkLWRjNmItNGYyZS1iNDc5LTc1YWMyYjQ2ZWEwOSIsImMiOjN9&pageName=ReportSection)

In the root directory a Power BI project file can be found under the power_bi folder

If you have Power BI desktop installed just open the file `abs_data.pbip` then you will have a Power BI project to work from.

To know more about Power BI project and how to integrate it with git read more [here](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview).

```bash
├── power_bi
│   ├── abs_data.Dataset
│   │   ├── definition.pbidataset
│   │   ├── diagramLayout.json
│   │   ├── item.config.json
│   │   ├── item.metadata.json
│   │   └── model.bim
│   ├── abs_data.Report
│   │   ├── StaticResources
│   │   │   ├── RegisteredResources
│   │   │   │   ├── abstrans3601216882942926.png
│   │   │   │   └── rbatrans9061234309651067.png
│   │   │   └── SharedResources
│   │   │       └── BaseThemes
│   │   │           └── CY23SU04.json
│   │   ├── datasetDiagramLayout.json
│   │   ├── definition.pbir
│   │   ├── item.config.json
│   │   ├── item.metadata.json
│   │   └── report.json
│   └── abs_data.pbip
```

you can use the embeded version Iframe of the report using this link below

```html
<iframe
  title="Report Section"
  width="600"
  height="373.5"
  src="https://app.powerbi.com/view?r=eyJrIjoiZGI3ZjY3MmQtODY4NC00ZGIwLTliNDYtNTY1MDdmZWRkZWVhIiwidCI6ImM3NjcyNjNkLWRjNmItNGYyZS1iNDc5LTc1YWMyYjQ2ZWEwOSIsImMiOjN9&pageName=ReportSection"
  frameborder="0"
  allowfullscreen="true"
></iframe>
```
## targeted series

| series_id   | content                                                                                                      | frequency | unit               | series_type        |
|-------------|--------------------------------------------------------------------------------------------------------------|-----------|--------------------|--------------------|
| A84423050A  | Unemployment rate ;  Persons ;                                                                               | Month     | Percent            | Seasonally Adjusted|
| A84998735A  | Earnings; Persons; Total earnings ;                                                                          | Biannual  | $                  | Seasonally Adjusted|
| A108284976J | Households ;  Housing Finance ;  Owner occupier ;  Construction of dwellings ;  New loan commitments ;  Number ;| Month     | Number             | Original           |
| A108280580R | Households ;  Housing Finance ;  Owner occupier ;  Purchase of newly erected dwellings ;  New loan commitments ;  Number ;| Month     | Number             | Original           |
| A108299018F | Households ;  Housing Finance ;  Owner occupier ;  Purchase of existing dwellings ;  New loan commitments ;  Number ;| Month     | Number             | Original           |
| A108284975F | Households ;  Housing Finance ;  Owner occupier ;  Construction of dwellings ;  New loan commitments ;  Value ;| Month     | $ Millions         | Original           |
| A108280579F | Households ;  Housing Finance ;  Owner occupier ;  Purchase of newly erected dwellings ;  New loan commitments ;  Value ;| Month     | $ Millions         | Original           |
| A108299017C | Households ;  Housing Finance ;  Owner occupier ;  Purchase of existing dwellings ;  New loan commitments ;  Value ;| Month     | $ Millions         | Original           |
| FILRHLBVS   | Lending rates; Housing loans; Banks; Variable; Standard; Owner-occupier                                    | Monthly   | Per cent per annum | Original           |
| A2325847F   | Percentage Change from Corresponding Quarter of Previous Year ;  All groups CPI ;  Australia ;             | Quarter   | Percent            | Original           |
| FIRMMCRT    | Cash Rate Target; monthly average                                                                           | Monthly   | Per cent           | Original           |


## ABS downloads

house_prices - 641606.xlsx - end december 2021
weekly_earnings - 6302002.xlsx - end november 2023 - ok
house_finance - 560103.xlsx - end january 2024 - ok
inflation - 640101.xlsx - end december 2023 - ok
unemployment - 6202001.xlsx - february 2024  ok
cash_rate - f01hist.xlsx - march 2024
variable_home_loan - f05hist.xlsx - march 2024
