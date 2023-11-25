from typing import List

# from tradeapp.exchanges.binancef.models.timeframe import Timeframe
# from tradeapp.exchanges.binancef.models.trend import Trend
import requests
from bs4 import BeautifulSoup

import pandas as pd

import csv

# from tradeapp.exchanges.binancef.binanceFuture import (
#     binance_future,
#     get_bal_of,
#     market_buy_order,
#     klines_future,
#     last_price,
#     market_sell_order
# )

link = "https://fr.tradingview.com/chart/?symbol=BINANCE%3A{}"


def gainers_losers():
    # Get trending coins
    lnk = "https://coinmarketcap.com/gainers-losers"

    req = requests.get(lnk)
    soup = BeautifulSoup(req.text,features="html.parser")

    gainers_table,losers_table = soup.find_all('table')
    # tds:list = gainers_table.find_all('p',{'class':'sc-4984dd93-0 kKpPOn'})
    gainers = gainers_table.find_all('p',{'class':'sc-4984dd93-0 iqdbQL coin-item-symbol'})
    gainers_volume_tr = gainers_table.find_all('tr')
    # print(gainers_volume_tr[1].fin)
    gainers_volume = [tr.find_all('td')[4].text for tr in gainers_volume_tr[1:]]
    # print(gainers_volume_tr_td)
    losers = losers_table.find_all('p',{'class':'sc-4984dd93-0 iqdbQL coin-item-symbol'})
    losers_volume_tr = losers_table.find_all('tr')
    # print(gainers_volume_tr[1].fin)
    losers_volume = [tr.find_all('td')[4].text for tr in losers_volume_tr[1:]]
    # print(losers_volume_tr_td)
    # data ={
    #     'gainers':[p.text+'USDT' for p in gainers],
                  
    #     'losers':[p.text+'USDT' for p in losers]
    # }
    gainers = {
        'crypto' : [p.text+'USDT' for p in gainers],
        'volume' : [vol for vol in gainers_volume],
        'chart_link' : [link.format(p.text+"USDT") for p in gainers]
    }
    losers ={
        'crypto' : [p.text+'USDT' for p in losers],
        'volume' : [vol for vol in losers_volume],
        'chart_link' : [link.format(p.text+"USDT") for p in losers]
    }
    return gainers,losers



# def get_trend(self, df:pd.Dataframe) -> Trend:
#         """give the trend of the current stock

#         Args:
#             df (pd.DataFrame): contains ohlc data of given crypto
#         """
#         # data
        
#         sma_size = 200
#         # Get the trend of the market by using sma200
#         # Get list of 5 last closed price
#         price: List[float] = df["Close"][-5:].to_list()
#         # calculate sma
#         df[f"SMA_{sma_size}"] = df["Close"].rolling(window=sma_size).mean()
#         sma_value: List[float] = df[f"SMA_{sma_size}"][-5:].to_list()
#         # condition
#         cond = price > sma_value
#         if cond:
#             return Trend.UPTREND
#         return Trend.DOWNTREND

# print(gainers_losers())



# data = pd.DataFrame.from_dict(gainers_losers(),orient='index')
# data = data.transpose()
# data.to_excel('crypto.xlsx')

gainers,losers = gainers_losers()

#for gainers
df_gainers = pd.DataFrame.from_dict(gainers,orient='index')
df_gainers = df_gainers.transpose()
df_gainers.to_excel('gainers.xlsx')

#for losers
df_losers = pd.DataFrame.from_dict(losers,orient='index')
df_losers = df_losers.transpose()
df_losers.to_excel('losers.xlsx')
