import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError
import pickle
import requests

#Scrapes wikipedia S&P 500 ticker table to create object
def save_sp500_tickers():
    resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(resp.text, "html.parser")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []

    for row in table.find_all('tr')[1:]:
        ticker = row.find_all('td')[0].text
        tickers.append(ticker)

    with open('sp500_tickers.pickle', 'wb') as f:
        pickle.dump(tickers, f)

#Gathering all ADJ close data from Yahoo API for tickers created
#and storing in stock_data directory
def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500_tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists("stock_data"):
        os.makedirs("stock_data")


    start = dt.datetime(2000,1,1)
    end = dt.datetime(2016,12,31)

    for ticker in tickers:
        try:
            if not os.path.exists("stock_data/{}".format(ticker)):
                df = web.DataReader(ticker, 'yahoo', start, end)
                df.to_csv("stock_data/{}".format(ticker))
                print("Gathered data on {}".format(ticker))
            else:
                print("Already have data for {}".format(ticker))

        except RemoteDataError:
            print("Data Error")
            continue
            
get_data_from_yahoo()
