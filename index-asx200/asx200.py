import bs4 as bs
import pickle
import requests

def save_asx200_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/S%26P/ASX_200#Constituent_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')

    table = soup.table

    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    return tickers

asx200_tickers = save_asx200_tickers()

print(asx200_tickers[201])
print(len(asx200_tickers))