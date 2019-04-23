import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle

import requests
import time

import pandas as pd
import requests
import time

Pull asx200 tickers from wikipedia
def save_asx200_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/S%26P/ASX_200#Constituent_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')

    table = soup.table

    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    
    with open('asx200tickers.pickle','wb') as f:
        pickle.dump(tickers, f)

    return tickers

#get data for each ticker
def get_asx_data(reload_asx = True):
    if reload_asx:
        tickers = save_asx200_tickers()
    else:
        with open("asc200tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2010, 1, 1)
    end = dt.datetime.now()
    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'robinhood', start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df = df.drop("Symbol", axis=1)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))

get_asx_data()