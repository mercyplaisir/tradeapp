#import json
import numpy as np
import pandas as pd
from binance.client import Client
from binance.enums import *
import math
import datetime
import time
import json

apikey='pPLvK8xoiqqTQi1IoLJQscGmI4uEqZBvkONXEfA7mq5dVptusfiYNaobXTiPHlv'
secretkey='teJqKc0KiS6Ftg4FPPwfb2rocz8t8S7MmjnwjouoYuezp2Ue5Gsojmr9fXkqdYFK'



#boucle pour se connecter
disconnected = True
while disconnected:
    try :
        client = Client(apikey,secretkey)
        print("vous etes connecter\n")
        disconnected = False
        connected = True
    except:
        print("impossible de se connecter\nveuillez patientez\n")
#----------------------------------------

profit_of_3_percent = False # pour rester dans le profit
Have_usdt = True # have usdt
Have_not_usdt = False #don't have usdt,meaning i have a crypto

profit_target_price = 0 #mon take profit price
loss_target_price = 0 #mon stop loss price

Have_usdt = True
Have_not_usdt = False

#---------------------------------------------------------------

def margin_buy_order(coin,order_quantity):
    order = client.create_margin_order(symbol=coin,side=SIDE_BUY,type=ORDER_TYPE_MARKET,quantity=order_quantity)

def margin_sell_order(coin,order_quantity):
    order = client.create_margin_order(symbol=coin,side=SIDE_SELL,type=ORDER_TYPE_MARKET,quantity=order_quantity)

def write_json(text:dict):
    with open('./test.json','a') as f:
        json.dump(text,f,indent= 4)

def percent_calculator(x:float,y:int):
    z=x+((x*3)/100)
    return z

#---------------------------------------------------------------



while True:
    #--------process to choose a crypto to rade with----------------------
    tickers = client.get_ticker()


    list_of_crypto = ['BTC','ETH','XRP','BNB','OCEAN','OGN']
    crypto_info = []
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
            if (i+'USDT') == ticker['symbol']:
                crypto_info.append(ticker)
    crypto_info = pd.DataFrame(crypto_info)

    crypto_info[['priceChange', 'priceChangePercent']] = crypto_info[['priceChange', 'priceChangePercent']].astype(float)

    #trier les indexes pour que 0 correspondents avec maintenant
    crypto_info.sort_values('priceChangePercent',ascending=False,inplace=True)

    #refaire les index
    crypto_info.reset_index(inplace = True)

    #supprimer un colonnes pas important
    crypto_info.drop(columns=['index'],inplace=True)

    #coin that we gonna use to trade
    coin_to_trade = crypto_info.iloc[0]['symbol']
    #price change percent
    price_change = crypto_info.iloc[0]['priceChangePercent']
    print(f'crypto that we gonna use is {coin_to_trade}, price change = {price_change}%')
    #---------------------------------------------------------------------------------------------
    #----------------boucle pour recuperer le prix-------------
    coin_ticker = client.get_symbol_ticker(symbol=coin_to_trade)
    coin_price = float(coin_ticker['price'])


    print('prix recuperer')
    #---------------------------------------------------------------

    #-------pou recupererles klines en 15 min et calculer les SMA-----------------------

    # fetch 15 minute klines for the last day up until now
    #klines_1min = client.get_historical_klines(coin_to_trade, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
    klines_15min = client.get_historical_klines(coin_to_trade, Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")

    print('klines recuperer')
    #changer timestamp en date
    for kline in klines_15min:
        kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)

    klines = pd.DataFrame(klines_15min)#changer en dataframe
    klines.drop(columns=[1,2,3,5,6,7,8,9,10,11],inplace= True)#supprimer les collonnes qui ne sont pas necessaires
    klines.columns = ['open_time','close_price']#renommer les colonnes

    #creer un SMA15
    klines['SMA_15'] = klines.iloc[:,1].rolling(window=15).mean()

    #creer un SMA50
    klines['SMA_50'] = klines.iloc[:,1].rolling(window=50).mean()

    #trier les indexes pour que 0 correspondents avec maintenant
    klines.sort_index(ascending=False,inplace=True)

    #refaire les index
    klines.reset_index(inplace = True)

    #supprimer un colonnes pas important
    klines.drop(columns=['index'],inplace=True)



    #-------------------------------------------

    #si SMA9 est superieur a SMA15
    if klines.loc[0]['SMA_15']>klines.loc[0]['SMA_50']:
        print("SMA_15 > SMA_50")
        Sma_signal_sell = False
        Sma_signal_buy = True
        
        print('SMA signal buy')

    #si SMA9 est inferieur a SMA15
    if klines.loc[0]['SMA_15'] < klines.loc[0]['SMA_50']:
        print("SMA_15 < SMA_50")
        Sma_signal_sell = True
        Sma_signal_buy = False
        profit_of_3_percent = False # pour rester dans le profit
        print('SMA signal sell')

    price_trick = False # pour voir si le marche ne triche pas
        #le prix inferieur a SMA 9             le prix inferieur ou egale a valeur de SMA 15 -30 and SMA9 est superieur a SMA15
    if coin_price < klines.loc[0]['SMA_15'] and coin_price<=(klines.loc[0]['SMA_50']-90) and (klines.loc[0]['SMA_15']>klines.loc[0]['SMA_50']):
        print("price under SMA9 and SMA15. SELL")
        Sma_signal_sell = True
        Sma_signal_buy = False
        price_trick = True



    #------------------------------_-

    sell_for_profit = False #declencheur de take profit



    if profit_target_price != 0 and profit_target_price<=coin_price:
        print('Profit of 3%, SELL')
        sell_for_profit=True



    coin = str(coin_to_trade.replace('USDT',''))# coin that i am using

#-----------------------


    if Sma_signal_buy and Have_usdt and not profit_of_3_percent:
        balance = client.get_asset_balance(asset='USDT')
        #info = client.get_margin_account()
        
        x = balance['free']
        x= x[:6]
        x = float(x)
        
        order_quantity=x / coin_price
        order_quantity = float(str(order_quantity)[:7])
        order_quantity
        print('sma signal buy and have usdt')
        try:
            #buy order
            margin_buy_order(coin_to_trade,order_quantity)
            #-------------------------
            print(f' {datetime.datetime.now()} bought {order_quantity}{coin} of {float(order_quantity*coin_price)} at {coin_price} \n')
            Have_not_usdt = True #don't have usdt
            Have_usdt = False # have btc
            operation = 'Buy'


            profit_target_price = percent_calculator(coin_price,3)#target profit price
            #--------------------------------------------
            
            trade_details = {'symbol':coin,'operation':operation,'quantity':order_quantity,'price':coin_price}
            write_json(trade_details)


        except:
            
            print('erreur lors de l achat')

            pass



    if Sma_signal_buy and Have_not_usdt:
        print('No USDT for BUY ORDER')

    #-------------------------------------
    
    if Sma_signal_sell or sell_for_profit and Have_not_usdt:
        #trades = client.get_my_trades(symbol="BTCUSDT")
        balance = client.get_asset_balance(asset=coin)
        #info = client.get_margin_account()
        x =balance['free']
        x= x[:7]
        order_quantity = float(x)
        print('smasignal sell and have no usdt')
        if sell_for_profit:
            profit_of_3_percent =True

        #sell order
        try:
            margin_sell_order(coin_to_trade,order_quantity)
            #sell_order
            print(f'{datetime.datetime.now()} sold {order_quantity}{coin} of {(float(order_quantity*coin_price))} at {coin_price} ')
            Have_usdt = True # have usdt
            Have_not_usdt = False #don't have usdt,meaning i have a crypto
            operation = 'Sell'
            
            #--------------------------------------------
            trade_details = {'symbol':coin,'operation':operation,'quantity':order_quantity,'price':coin_price}
            write_json(trade_details)
        except:
            print('erreur lors du vente')
            


    if Sma_signal_sell and Have_usdt:
        print(f'No {coin} for SELL ORDER')

    
    print('------------------------------------\n')

    

