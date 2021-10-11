import os, os.path

from tableauscraper import TableauScraper as TS
import pandas as pd

url = 'https://public.tableau.com/views/COVID-19CasesandDeathsinthePhilippines_15866705872710/Home'

ts = TS()
ts.loads(url)
dashboard = ts.getWorkbook()

ws_current_new = ts.getWorksheet('Epi_TotalCases#')
ws_active = ts.getWorksheet('Epi_ActiveCases#')
ws_deaths = ts.getWorksheet('Epi_Deaths#')
ws_recovered = ts.getWorksheet('Epi_Recovered#')

current_new = (ws_current_new.data \
    .drop(
        columns=[
            'ATTR(Max DateRepConf Shortened)-alias',
            'ATTR(Max DateRepConf)-alias'])
    .rename(
        columns={
            'AGG(Count - Cases)-alias': 'Total Cases',
            'AGG(Count - Cases (new))-alias': 'New Cases'})
    .replace('[,%]', '', regex=True)
    .apply(pd.to_numeric, errors='ignore')
)

active = (ws_active.data \
    .drop(
        columns=[
            'Max DateRepConf-alias',
            'AGG(Count - Active Cases (new))-alias'])
    .rename(columns={'AGG(Count - Active Cases)-alias': 'Active Cases'})
    .replace('[,%]', '', regex=True)
    .apply(pd.to_numeric, errors='ignore')
)

deaths = (ws_deaths.data \
    .drop(columns='ATTR(Max DateRepRem)-alias')
    .rename(columns={'AGG(Count - Deaths)-alias': 'Deaths'})
    .replace('[,%]', '', regex=True)
    .apply(pd.to_numeric, errors='ignore')
)

recovered = (ws_recovered.data \
    .drop(columns='ATTR(Max DateRepRem)-alias')
    .rename(columns={'AGG(Count - Recoveries)-alias': 'Recoveries'})
    .replace('[,%]', '', regex=True)
    .apply(pd.to_numeric, errors='ignore')
)

dfs = [current_new, active, deaths, recovered]
national = pd.concat(dfs, axis='columns').to_json(orient='records').strip('[]')

if not os.path.exists('data'):
    os.mkdir('data')
with open('data/national.json', 'w', encoding='utf-8') as f:
    f.write(national)