import numpy as np
import pandas as pd
from binance.client import Client
from binance.enums import *
import math
import datetime
import time
import json
import random

"""
-in the function coinfortrade() i've removed the 1hour function , i'mworking with the 15min chart
"""


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_--_-_-_-_-_-_
apikey='eKDyjsVeMhssfXL89oil2keouZSfpnJwqJV3mfvApOYDylfUjGc6hKAtapQIHL3b'
secretkey='hISw2v7P96RXq698sIQVUGHfhX3Jt8aqh9FOlURGfXFwelYKq1R5oPfUbfWtD9lo'

client = Client(apikey,secretkey)
#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

def get_list_of_crypto():
    x = client.get_margin_account()
    a=[]
    for i in x['userAssets']:
        #if float(i['asset'])>0:
        a.append(i['asset'])

    return a

list_of_crypto = get_list_of_crypto()


#placer un ordre d'achat
def margin_buy_order(coin_to_trade:str,order_quantity:float):
    client.create_margin_order(symbol=coin_to_trade,side=SIDE_BUY,type=ORDER_TYPE_MARKET,quantity=order_quantity)



#placer un ordre de vente
def margin_sell_order(coin_to_trade:str,order_quantity:float):
    client.create_margin_order(symbol=coin_to_trade,side=SIDE_SELL,type=ORDER_TYPE_MARKET,quantity=order_quantity)



#ecrire dans un fichier json
def write_json(text):
    with open('./test.json','r') as f:
        j = json.load(f)
        j.append(text)
    with open('./test.json','w') as f:
        json.dump(j,f,indent= 4)



#calcule du pourcentage
def percent_calculator(x:float,y:int):
    """
    calcule d'un nombre par rapport a un pourcentage du nombre d'origine
    """
    z=x+((x*y)/100)
    return z


def percent_change(original_number:float,new_number:float):
    """
    variation du prix en pourcentage entrer 2nombres
    """
    z = ((new_number-original_number)/original_number)*100
    return z


def margin_balance_of(coin:str):
    """
    recuperer la balance d'un crypto
    """

    info = client.get_margin_account()
    for i in info['userAssets']:
        if coin=='ETH':
            if i['asset']==coin:
                balance = float(str(i['free'])[:5])

        if coin=='BTC':
            if i['asset']==coin:
                balance = float(str(i['free'])[:7])

        elif i['asset']==coin:
            balance = (float(str(i['free'])[:5]))
    return balance

def order_quantity_of(balance:float,coin:str):
    """
    permet d'avoir une quantite pour placer l'ordre
    """
    #il determine la quantite a utiliser pour placer un ordre en analysant so prix

    coin_ticker_usd = client.get_symbol_ticker(symbol=coin+'USDT')
    coin_price_usd= float(coin_ticker_usd['price'])
    coin_ticker = client.get_symbol_ticker(symbol=coin+'BTC')
    coin_price = float(coin_ticker['price'])
    if coin=='ETH':
        q = balance / coin_price
        q =float(str(q)[:5])
    if coin!='ETH':
        if 50<=coin_price_usd:#si le prix est entre 50 et 700
            q = balance / coin_price
            q =float(str(q)[:5])

        elif 16<=coin_price_usd<=49:#si le prix est entre 16 et 49
            q = balance / coin_price
            q =float(str(q)[:3])

        elif 0.18<=coin_price_usd<=15:#si le prix est entre 0 et 15
            q = balance / coin_price
            q =float(str(q)[:2])
        elif coin_price<0.18:
            q = balance / coin_price
            q =float(str(q)[:3])
    return q#q c'est la quqntite



def hour1_trend(coin_to_trade:str):
    """
    tendance d'un crypto dans un timeframe de 1heure
    """

    klines_1hour = client.get_historical_klines(coin_to_trade, Client.KLINE_INTERVAL_1HOUR, "5 days ago UTC")


    #changer timestamp en date
    for kline in klines_1hour:
        kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)

    klines = pd.DataFrame(klines_1hour)#changer en dataframe
    klines.drop(columns=[1,2,3,5,6,7,8,9,10,11],inplace= True)#supprimer les collonnes qui ne sont pas necessaires
    klines.columns = ['open_time','close_price']#renommer les colonnes

    #creer un SMA_30
    klines['SMA_30'] = klines.iloc[:,1].rolling(window=30).mean()

    #creer un SMA50
    klines['SMA_50'] = klines.iloc[:,1].rolling(window=50).mean()

    #trier les indexes pour que 0 correspondents avec maintenant
    klines.sort_index(ascending=False,inplace=True)
    #refaire les index
    klines.reset_index(inplace = True)
    #supprimer un colonnes pas important
    klines.drop(columns=['index'],inplace=True)
    #si SMA_30 est superieur a SMA_50
    if klines.loc[0]['SMA_30']>klines.loc[0]['SMA_50']:
        up_trend = True
        print(" 1h : uptrend")
    #si SMA_30 est inferieur a SMA_50
    if klines.loc[0]['SMA_30'] < klines.loc[0]['SMA_50']:
        up_trend = False
        print(" 1h : downtrend")

    return up_trend


def minute15_trend(coin_to_trade:str):
    """
    tendance d'un crypto dans un timeframe de 1heure
    """
    getKlines = False
    while not getKlines:
        try:
            klines_15min = client.get_historical_klines(coin_to_trade, Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")
            getKlines = True
        except:
            pass


    #changer timestamp en date
    for kline in klines_15min:
        kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)

    klines = pd.DataFrame(klines_15min)#changer en dataframe
    klines.drop(columns=[1,2,3,5,6,7,8,9,10,11],inplace= True)#supprimer les collonnes qui ne sont pas necessaires
    klines.columns = ['open_time','close_price']#renommer les colonnes

    #creer un SMA_30
    klines['SMA_30'] = klines.iloc[:,1].rolling(window=30).mean()

    #creer un SMA50
    klines['SMA_50'] = klines.iloc[:,1].rolling(window=50).mean()

    #trier les indexes pour que 0 correspondents avec maintenant
    klines.sort_index(ascending=False,inplace=True)

    #refaire les index
    klines.reset_index(inplace = True)

    #supprimer un colonnes pas important
    klines.drop(columns=['index'],inplace=True)

    #si SMA_30 est superieur a SMA_50
    if klines.loc[0]['SMA_30']>klines.loc[0]['SMA_50']:
        up_trend = True
        print(" 15min : uptrend")

    #si SMA_30 est inferieur a SMA_50
    if klines.loc[0]['SMA_30'] < klines.loc[0]['SMA_50']:
        up_trend = False
        print(" 15min : downtrend")

    return up_trend



def price_trick(coin_to_trade:str):
    """
    *coin_to_trade,ex:ETHBTC
    *coinBase,ex: for ETHBTC, BTC is coinBase

    *price tricks if:
    -coin price under SMA30 and 50 but SMA30 is higher than SMA50
    -if the trend didn't start 6candles before
    -if price is verry high when the SMA30 break the SMA50
    -The coin price is between the SMA30 and SMA50 but the SMA30 is higher than the SMA50
    """

    coin_price = get_coin_price(coin_to_trade)
    #coin = str(coin_to_trade.replace('BTC',''))



    getKlines = False
    while not getKlines:
        try:
            klines_15min = client.get_historical_klines(coin_to_trade, Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")
            getKlines = True
        except:
            pass

    #changer timestamp en date
    for kline in klines_15min:
        kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)

    klines = pd.DataFrame(klines_15min)#changer en dataframe
    klines.drop(columns=[1,2,3,5,6,7,8,9,10,11],inplace= True)#supprimer les collonnes qui ne sont pas necessaires
    klines.columns = ['open_time','close_price']#renommer les colonnes

    #creer un SMA_30
    klines['SMA_30'] = klines.iloc[:,1].rolling(window=30).mean()

    #creer un SMA50
    klines['SMA_50'] = klines.iloc[:,1].rolling(window=50).mean()

    #trier les indexes pour que 0 correspondents avec maintenant
    klines.sort_index(ascending=False,inplace=True)

    #refaire les index
    klines.reset_index(inplace = True)

    #supprimer un colonnes pas important
    klines.drop(columns=['index'],inplace=True)

    price_trick = False
    if coin_price < klines.loc[0]['SMA_30'] and coin_price<=(klines.loc[0]['SMA_50']) and (klines.loc[0]['SMA_30']>klines.loc[0]['SMA_50']):
        price_trick = True
        #print("price under sma30 and 50")
    if klines.loc[6]['SMA_30']>klines.loc[6]['SMA_50'] and klines.loc[3]['SMA_30']>klines.loc[3]['SMA_50'] :#si la tendance etait la meme il y a 6bougies don't buy
        price_trick = True
        #print(" too late to enter the trend")
    if  coin_price > percent_calculator(klines.loc[0]['SMA_30'],1):
        price_trick = True
        #print(" too late, price really high")
    if klines.loc[0]['SMA_30']>coin_price>klines.loc[0]['SMA_50']:
        price_trick = True
        #print(" price between SMA30 and SMA50")


    return price_trick






def coin_for_trade():
    """
    fonction pour recuperer le coin for trade et son price change
    """
    redo_search = True

    while redo_search:
        getTickers=False
        while not getTickers:
            try:
                tickers = client.get_ticker()
                getTickers=True
            except:
                pass
        crypto_info = []
        cryptoList = []
        for ticker in tickers:
            ticker.pop('weightedAvgPrice')
            ticker.pop('quoteVolume')
            ticker.pop('firstId')
            ticker.pop('lastId')
            ticker.pop('count')
            ticker.pop('highPrice')
            ticker.pop('lowPrice')
            ticker.pop('lastQty')
            ticker.pop('prevClosePrice')
            ticker.pop('bidPrice')
            ticker.pop('bidQty')
            ticker.pop('askPrice')
            ticker.pop('askQty')
            ticker.pop('volume')
            for i in list_of_crypto:
                if (i+'BTC') == ticker['symbol']:
                    crypto_info.append(ticker)

        for z in crypto_info:#['symbol']:
            cryptoList.append(z['symbol'])


        crypto_infoPD = pd.DataFrame(crypto_info)

        crypto_infoPD[['priceChange', 'priceChangePercent']] = crypto_infoPD[['priceChange', 'priceChangePercent']].astype(float)

        #trier les indexes pour que 0 correspondents avec le crypto ayant pricechange percent eleve
        crypto_infoPD.sort_values('priceChangePercent',ascending=False,inplace=True)

        #refaire les index
        crypto_infoPD.reset_index(inplace = True)

        #supprimer un colonnes pas important
        crypto_infoPD.drop(columns=['index'],inplace=True)

        nonePickedUp = True

        for n in range(0,(len(cryptoList)-24)):
            #coin that we gonna use to trade
            #n = random.randint(0,(len(list_of_crypto)-1))#pick a random crypto from the list of crypto
            coin_to_trade = crypto_infoPD.iloc[n]['symbol']
            price_change = crypto_infoPD.iloc[n]['priceChangePercent']

            print(coin_to_trade,' : ',price_change)
            #up_trend_1hour = hour1_trend(coin_to_trade) #tendance pour 1heure
            up_trend_15min = minute15_trend(coin_to_trade) #tendance pour 15min
            isThere_price_trick = True

            if up_trend_15min: #removed the 1hour working with the 15min
                isThere_price_trick = price_trick(coin_to_trade) #price trick

            if not isThere_price_trick:
                print('no price tricks')
            elif isThere_price_trick:
                print('Not a good one')


            if up_trend_15min and not isThere_price_trick :
                redo_search=False
                nonePickedUp = False

                print('got it')
                break
            print('-----------------------------')
        if nonePickedUp:
            time.sleep(20)
    b = {'coin to trade':coin_to_trade,'price change': price_change}
    return b

def get_coin_price(coin_to_trade):
    """
    get coin price

    """
    coin_ticker = client.get_symbol_ticker(symbol=coin_to_trade)
    coin_price = float(coin_ticker['price'])
    return coin_price


def coin_approvement(coin_to_trade):
    """
    it's appprouve if the coin is really good to use
    """
    buy = False
    #up_trend_1hour = hour1_trend(coin_to_trade)
    up_trend_15min = minute15_trend(coin_to_trade)
    isThere_price_trick = price_trick(coin_to_trade) # pour voir si le marche ne triche pas   

    if up_trend_15min and not isThere_price_trick:
        buy = True
    return buy






def check_price_moves(coin_to_trade:str):
    """
    when i'm in a trade it checks the price movement and return a boolean value.
    False if it's for a sell 
    True if it's for a hold
    """

    coin_price = get_coin_price(coin_to_trade)
    #coin = str(coin_to_trade.replace('BTC',''))



    getKlines = False
    while not getKlines:
        try:
            klines_15min = client.get_historical_klines(coin_to_trade, Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")
            getKlines = True
        except:
            pass

    #changer timestamp en date
    for kline in klines_15min:
        kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)

    klines = pd.DataFrame(klines_15min)#changer en dataframe
    klines.drop(columns=[1,2,3,5,6,7,8,9,10,11],inplace= True)#supprimer les collonnes qui ne sont pas necessaires
    klines.columns = ['open_time','close_price']#renommer les colonnes

    #creer un SMA_30
    klines['SMA_30'] = klines.iloc[:,1].rolling(window=30).mean()

    #creer un SMA50
    klines['SMA_50'] = klines.iloc[:,1].rolling(window=50).mean()

    #trier les indexes pour que 0 correspondents avec maintenant
    klines.sort_index(ascending=False,inplace=True)

    #refaire les index
    klines.reset_index(inplace = True)

    #supprimer un colonnes pas important
    klines.drop(columns=['index'],inplace=True)

    price_trick = False
    if coin_price < klines.loc[0]['SMA_30'] and coin_price<=(klines.loc[0]['SMA_50']) and (klines.loc[0]['SMA_30']>klines.loc[0]['SMA_50']):
        price_trick = True
        #print("price under sma30 and 50")

    if klines.loc[0]['SMA_30']>coin_price>klines.loc[0]['SMA_50']:
        price_trick = True
        #print(" price between SMA30 and SMA50")


    return price_trick



