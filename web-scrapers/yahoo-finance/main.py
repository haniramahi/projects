import datetime
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import pandas as pd
import time

# get today's date formatted as YYYYMMDD
today = datetime.datetime.now().strftime('%Y%m%d')

# import the list of tickers
data = pd.read_csv('./tickers.csv')
tickers = DataFrame(data)

df = DataFrame()
for i in range(len(tickers['Symbol'])):
    summary_tab = {}
    ticker = tickers['Symbol'].iloc[i]
    print(ticker)

    # send out request and store response in a variable
    url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch'
    r = requests.get(url=url)
    src = r.content

    # parse the summary tab on the webpage and store it 2 separate lists
    shorba = BeautifulSoup(src, 'lxml')
    summary_tab_headers = [entry.text for entry in shorba.find_all('td', {'class': 'C($primaryColor) W(51%)'})]
    summary_tab_values = [entry.text for entry in shorba.find_all('td', {'class': 'Ta(end) Fw(600) Lh(14px)'})]
    summary_tab = {summary_tab_headers[i]: summary_tab_values[i] for i in range(len(summary_tab_headers))}
    summary_tab['Name'] = tickers['Name'].iloc[i]
    summary_tab['Ticker'] = ticker
    summary_tab['Sector'] = tickers['Sector'].iloc[i]
    summary_tab['Date'] = datetime.date.today().strftime('%m/%d/%Y')
    
    print(summary_tab)
    # store it into a dataframe
    df = df.append(summary_tab,ignore_index=True)
    time.sleep(2)

df.to_csv(f'./data/{today}_stock_data.csv')