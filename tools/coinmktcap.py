from typing import List

# from tradeapp.exchanges.binancef.models.timeframe import Timeframe
# from tradeapp.exchanges.binancef.models.trend import Trend
import requests
from bs4 import BeautifulSoup

import pandas as pd

from enum import Enum,auto

class Trend(Enum):
    UPTREND = auto()
    DOWNTREND = auto()
    
    def __str__(self) -> str:
        return f'{self.name}'
    def __eq__(self, __value: object) -> bool:
        return self.name ==  __value
    def __hash__(self) -> int:
        return hash(self.name)


class Timeframe(Enum):
    M1 = '1m'
    M5 = '5m'
    M15 = '15m'
    M30 = '30m'
    H1 = '1h'
    H4 = '4h'
    DAY = '1d'
    WEEK = '1w'

    def __repr__(self) -> str:
        return  f'{self.value}'

    def __str__(self) -> str:
        return  f'{self.value}'
    def __eq__(self, __value: object) -> bool:
        return self.value==__value
    def __hash__(self) -> int:
        return hash(self.value)
# from tradeapp.exchanges.binancef.models.trend import Trend

# from tradeapp.exchanges.binancef.binanceFuture import (
#     binance_future,
#     get_bal_of,
#     market_buy_order,
#     klines_future,
#     last_price,
#     market_sell_order
# )

link = "https://fr.tradingview.com/chart/?symbol=BINANCE%3A{}"


# @logger_wrapper(__name__,"retreiving klines")
def klines_future(pair:str,interval:str):
    rs = requests.get("https://fapi.binance.com/fapi/v1/indexPriceKlines",params={
        "pair": pair,
        "contractType": "PERPERTUAL",
        "interval" : interval
    })
    df = pd.DataFrame(rs.json(),columns=["open time","open","high","low","close","volume","close time","1","2","3","4","5"])
    df = df.get(["open time","open","high","low","close","close time"])
    df[["open","high","low","close"]] = df[["open","high","low","close"]].astype(float)
    # df = df.set_index([pd.Index([i for i in range(df.shape[0])]),'open time'])
    # print(df)
    return df

def trend_calculator(df:pd.DataFrame) -> Trend:
        """give the trend of the current stock

        Args:
            df (pd.DataFrame): contains ohlc data of given crypto
        """
        # data
        
        sma_size = 200
        # Get the trend of the market by using sma200
        # Get list of 5 last closed price
        price: List[float] = df["close"][-5:].to_list()
        # calculate sma
        df[f"SMA_{sma_size}"] = df["close"].rolling(window=sma_size).mean()
        sma_value: List[float] = df[f"SMA_{sma_size}"][-5:].to_list()
        # condition
        cond = price > sma_value
        if cond:
            return Trend.UPTREND
        return Trend.DOWNTREND

# print(gainers_losers())

def trend(crypto,timeframe):
    klines = klines_future(crypto,timeframe)
    return trend_calculator(klines)

# data = pd.DataFrame.from_dict(gainers_losers(),orient='index')
# data = data.transpose()
# data.to_excel('crypto.xlsx')

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
        'trend_d1' : [trend(p.text+'USDT',Timeframe.DAY) for p in gainers],
        'trend_4h' : [trend(p.text+'USDT',Timeframe.H4) for p in gainers],
        'trend_1h' : [trend(p.text+'USDT',Timeframe.H1) for p in gainers],
        'chart_link' : [link.format(p.text+"USDT") for p in gainers]
    }
    losers ={
        'crypto' : [p.text+'USDT' for p in losers],
        'volume' : [vol for vol in losers_volume],

        'trend_d1' : [trend(p.text+'USDT',Timeframe.DAY) for p in losers],
        'trend_4h' : [trend(p.text+'USDT',Timeframe.H4) for p in losers],
        'trend_1h' : [trend(p.text+'USDT',Timeframe.H1) for p in losers],

        'chart_link' : [link.format(p.text+"USDT") for p in losers]
    }
    return gainers,losers

if __name__ == "__main__":

    gainers,losers = gainers_losers()

    #for gainers
    df_gainers = pd.DataFrame.from_dict(gainers,orient='index')
    df_gainers = df_gainers.transpose()
    df_gainers.to_excel('gainers.xlsx')

    #for losers
    df_losers = pd.DataFrame.from_dict(losers,orient='index')
    df_losers = df_losers.transpose()
    df_losers.to_excel('losers.xlsx')
