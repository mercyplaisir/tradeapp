import numpy as np
import pandas as pd
from binance.client import Client
from binance.enums import *
import math
import datetime
import time
import json
import random
import websocket

"""
-in the function coinfortrade() i've removed the 1hour function , i'mworking with the 5min chart
- i'm using SMA 15 and SMA 30

"""


#-_-_-_-_-_-_-_-_-_-_-_-_-_-_--_-_-_-_-_-_
apikey='eKDyjsVeMhssfXL89oil2keouZSfpnJwqJV3mfvApOYDylfUjGc6hKAtapQIHL3b'
secretkey='hISw2v7P96RXq698sIQVUGHfhX3Jt8aqh9FOlURGfXFwelYKq1R5oPfUbfWtD9lo'

#------------boucle pour se connecter---------------------
client = Client(apikey,secretkey)
#----------------------------------------




#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-

#def get_list_of_crypto():
#    x = client.get_margin_account()
#    a=[]
#    for i in x['userAssets']:
#        #if float(i['asset'])>0:
#        a.append(i['asset'])

#    return a

list_of_crypto = ['ETH','DOGE','XRP','BNB','LINK','ADA','LTC','DOT','AAVE','NEO','BCH']





#placer un ordre d'achat
def margin_buy_order(coin_to_trade:str,order_quantity:float):
    """A margin buy order"""
    client.create_margin_order(symbol=coin_to_trade,side=SIDE_BUY,type=ORDER_TYPE_MARKET,quantity=order_quantity)



#placer un ordre de vente
def margin_sell_order(coin_to_trade:str,order_quantity:float):
    """ A margin sell order """
    client.create_margin_order(symbol=coin_to_trade,side=SIDE_SELL,type=ORDER_TYPE_MARKET,quantity=order_quantity)



#ecrire dans un fichier json
def write_json(text):
    """ Write in a json file"""
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
        if coin_price_usd>=5000:#si le prix est entre 50 et 700
            q = balance / coin_price
            q =float(str(q)[:6])


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



def get_klines(coin_to_trade:str,timeframe:str,interval:str):
    """
    Get the klines for the timeframe given and in interval given.
    timeframe ex:1m,5m,15m,1h,2h,6h,8h,12h,1d,1M,1w,3d

    """

    try:
        klines_list = client.get_historical_klines(coin_to_trade, timeframe, f"{interval} ago UTC")

        #changer timestamp en date
        for kline in klines_list:
            kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)

        klines = pd.DataFrame(klines_list)#changer en dataframe
        klines.drop(columns=[2,3,5,6,7,8,9,10,11],inplace= True)#supprimer les collonnes qui ne sont pas necessaires

        klines.columns = ['open_time','open_price','close_price']#renommer les colonnes

        #creer un SMA_30
        klines['SMA_30'] = klines.iloc[:,1].rolling(window=15).mean()

        #creer un SMA50
        klines['SMA_50'] = klines.iloc[:,1].rolling(window=30).mean()

        #calculate sma20
        klines['SMA_20'] = klines.iloc[:,1].rolling(window=20).mean()

        # calculate the standar deviation
        klines['rstd'] = klines.iloc[:,1].rolling(window=20).std()

        klines['upper_band'] = klines['SMA_20'] + 2 * klines['rstd']
        #klines['upper_band'] = upper_band.rename(columns={symbol: 'upper'})
        klines['lower_band'] = klines['SMA_20'] - 2 * klines['rstd']
        #klines['lower_band'] = lower_band.rename(columns={symbol: 'lower'})

        #klines = klines.join(upper_band).join(lower_band)



        #trier les indexes pour que 0 correspondents avec maintenant
        klines.sort_index(ascending=False,inplace=True)

        #refaire les index
        klines.reset_index(inplace = True)

        #supprimer un colonnes pas important
        klines.drop(columns=['index','rstd'],inplace=True)

        return klines

    except:
            print('no klines')


    return klines



def price_study(coin_to_trade:str,klines,advanced:bool):
    """
    study made on klines(dataframe)
    """
    coin_price = get_coin_price(coin_to_trade)

    if not advanced:

        a=[]
        for n in range(0,4):
            if float(klines.loc[n]['close_price'])>float(klines.loc[n]['open_price'])>=float(klines.loc[n+1]['close_price'])>float(klines.loc[n+1]['open_price'])>float(klines.loc[n+1]['SMA_20']) and coin_price >=percent_calculator(float(klines.loc[0]['SMA_20']),0.7):
                y=True
                a.append(y)
            else:
                y=False
                a.append(y)
        j=0
        for i in a:
            if i==True:
                j+=1
            else:
                break
        if j==4:
            bool_answer=True
        else:
            bool_answer=False
#-------------------------------------------------------------------------------

    elif advanced:

        if float(klines.loc[0]['SMA_20'])>float(klines.loc[1]['close_price'])>float(klines.loc[1]['open_price'])>=float(klines.loc[2]['close_price'])<float(klines.loc[2]['open_price']):
            if float(klines.loc[1]['close_price']) >= percent_calculator(float(klines.loc[2]['open_price']),0.5):
                bool_answer = True
            else:
                bool_answer = False
        else:
            bool_answer = False





    return bool_answer




def hour1_trend(coin_to_trade:str):
    """
    tendance d'un crypto dans un timeframe de 1heure
    """
    up_trend = False
    try:
        klines = get_klines(coin_to_trade,'1h','5 days')

        up_trend = price_study(coin_to_trade,klines,False)
    except:
        up_trend=False

    return up_trend


def minute5_trend(coin_to_trade:str):
    """
    tendance d'un crypto dans un timeframe de 1heure
    """

    up_trend = False
    try:
        klines= get_klines(coin_to_trade,'5m','1day')

        up_trend = price_study(coin_to_trade,klines,True)
    except:
        up_trend=False
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

    #coin_price = get_coin_price(coin_to_trade)
    #coin = str(coin_to_trade.replace('BTC',''))

    try:
        klines= get_klines(coin_to_trade,'5m','1 day')

        price_trick = price_study(coin_to_trade,klines,True)

    except:
        price_trick= True
    return price_trick




traded_crypto = []#liste des crypto deja trader

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

        time_now = datetime.datetime.now()
        print(time_now)

        cryptoList=[ticker['symbol'] for ticker in tickers if (ticker['symbol'].replace('BTC','')) in list_of_crypto ]
        crypto_info = [ticker for ticker in tickers if ticker['symbol']in cryptoList]
        

        crypto_infoPD = pd.DataFrame(crypto_info)

        crypto_infoPD[['priceChange', 'priceChangePercent']] = crypto_infoPD[['priceChange', 'priceChangePercent']].astype(float)

        #trier les indexes pour que 0 correspondents avec le crypto ayant pricechange percent eleve
        crypto_infoPD.sort_values('priceChangePercent',ascending=False,inplace=True)

        #refaire les index
        crypto_infoPD.reset_index(inplace = True)

        #supprimer un colonnes pas important
        crypto_infoPD.drop(columns=['index'],inplace=True)

        nonePickedUp = True

        for n in range(0,(len(cryptoList)-1)):
            coin_to_trade = crypto_infoPD.iloc[n]['symbol']
            price_change = crypto_infoPD.iloc[n]['priceChangePercent']
            coin = str(coin_to_trade.replace('BTC',''))
        
            if coin not in traded_crypto:
                
                
                print(coin_to_trade,' : ',price_change)
                #up_trend_1hour = hour1_trend(coin_to_trade) #tendance pour 1heure
                up_trend = hour1_trend(coin_to_trade) #tendance pour 15min



                if up_trend: #removed the 1hour working with the 15min
                    price_5min = minute5_trend(coin_to_trade) #price trick

                    if not price_5min:
                        print('no')
                    elif price_5min:
                        print('good one')


                if up_trend and price_5min :
                    redo_search=False
                    nonePickedUp = False

                    print('got it')
                    b = {'coin to trade':coin_to_trade,'price change': price_change}
                    return b
                    break
                print('-----------------------------')

            elif coin in traded_crypto:
                continue


            if len(traded_crypto)>= (len(list_of_crypto)//2):#delete the list if traded the half of the list
                traded_crypto.clear()

        if nonePickedUp:
            time.sleep(300)




def get_coin_price(coin_to_trade):
    sockete = f"wss://stream.binance.com:9443/ws/{coin_to_trade.lower()}@kline_1m"
    was= websocket.create_connection(sockete)

    json_result = was.recv()
    was.close()
    dict_result=json.loads(json_result)

    return float(dict_result['k']['c'])#close price


def coin_approvement(coin_to_trade):
    """
    it's appprouve if the coin is really good to use
    """
    buy = False
    #up_trend_1hour = hour1_trend(coin_to_trade)
    up_trend = hour1_trend(coin_to_trade)
    price_5min = minute5_trend(coin_to_trade)

    if up_trend and not price_5min:
        buy = True
    return buy










