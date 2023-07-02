from pathlib import Path

import pandas as pd

BASE_PATH = Path(__file__).parent
DATABASE_PATH = BASE_PATH / 'database'

data = DATABASE_PATH / 'data.parquet'

df_data = pd.read_parquet(data)


def merge_columns(df:pd.DataFrame, first_col: str, second_col:str)-> pd.DataFrame:
    last_col1_index = df[first_col].last_valid_index()
    df[second_col] = pd.concat([df[first_col].iloc[:last_col1_index + 1], df[second_col].iloc[last_col1_index + 1:]])
    df.drop(columns=[first_col], inplace=True)
    return df

target_series =  [
                 'A2772132V',
                 'A84998735A',
                 'A108284976J',
                'A108280580R',
                'A108299018F',
                'A108284975F',
                'A108280579F',
                'A108299017C', 
                'FILRHLBVS',
                'FIRMMCRT',
                'A2325847F',
                'A84423050A']

filter = (df_data['variable'].
 isin(target_series)
)

df_data = df_data[filter]

headers = [
           'weekly_earnings_old', 
           'weekly_earnings',
            'contruction_no',
            'new_built_no',
            'existing_dwelling_no',
            'contruction_value',
            'new_built_value',
            'existing_dwelling_value',
            'variable_loan_owner',
            'cash_rate',
            'cpi',
            'unemployement_rate']


df_data['month'] = pd.to_datetime(df_data['month'])

first_month = df_data['month'].min().replace(day=1)
last_month = df_data['month'].max().replace(day=1)

data_period = pd.date_range(start=first_month, end=last_month, freq='M')

df = pd.DataFrame()

df['month'] = data_period

df['month'] = df['month'].dt.to_period('M').dt.to_timestamp()


df = df.set_index('month')


for s, head in zip(target_series,headers):
    serie_df = df_data[df_data['variable'] == s][['month','value']]
    serie_df['month'] = serie_df['month'].dt.to_period('M').dt.to_timestamp()
    serie_df = serie_df.set_index('month')
    df[head] = serie_df

df = df.reset_index()

df = merge_columns(df, 'weekly_earnings_old', 'weekly_earnings')

max_index = max([ df[col].first_valid_index() for col in df.columns if df[col].first_valid_index() != 0 ])

for col in df.columns:
    df[col].fillna(method='ffill', inplace=True)

# combine loans and calculate average loan size

loan_columns =  ['contruction_no',
                'new_built_no',
                'existing_dwelling_no',
                'contruction_value',
                'new_built_value',
                'existing_dwelling_value']

df['total_new_loans_no'] = df['contruction_no'] + df['new_built_no'] + df['existing_dwelling_no'] 
df['total_new_loans_value'] = df['contruction_value'] + df['new_built_value'] + df['existing_dwelling_value'] 
df['average_loan_value'] = ( df['total_new_loans_value'] / df['total_new_loans_no'] ) * 1000
df['average_yearly_interest'] = ((df['variable_loan_owner']/100) * df['average_loan_value']) * 1000
df['loan_repayment_perc_income'] = df['average_yearly_interest'] / (df['weekly_earnings']*52)

df.drop(columns=loan_columns, inplace=True)

df_final = df[646:]

df_final.to_csv("final.csv", index=False)