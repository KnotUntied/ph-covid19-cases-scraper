import os, os.path

from tableauscraper import TableauScraper as TS
import pandas as pd

url = 'https://public.tableau.com/views/COVID-19CasesandDeathsinthePhilippines_15866705872710/Cases'

ts = TS()
ts.loads(url)
dashboard = ts.getWorkbook()

ws = ts.getWorksheet('C_Table')

if not os.path.exists('data'):
    os.mkdir('data')
with open('data/local.json', 'w', encoding='utf-8') as f:
    (ws.data \
        .drop(index=ws.data[ws.data['ProvinceCity Clean-value'] == '%null%'].index)
        .pivot(
            index='ProvinceCity Clean-alias',
            columns='Measure Names-alias',
            values='Measure Values-alias')
        .replace('[,%]', '', regex=True)
        .apply(pd.to_numeric)
        .to_json(
            path_or_buf=f,
            orient='index',
            force_ascii=False)
    )