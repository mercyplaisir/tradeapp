#import json
import numpy as np
import pandas as pd
from binance.client import Client
from binance.enums import *
import math
import datetime
import time
import json
import random

apikey='pPLvK8xoiqqTQi1IoLJQscGmI4uEqZBvkONXEfA7mq5dVptusfiYNaobXTiPHlvn'
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
have_btc = True # have BTC
Have_other_coin = False #don't have BTC,meaning i have a crypto

profit_target_price = 0 #mon take profit price
loss_target_price = 0 #mon stop loss price



search_coin = True

#---------------------------------------------------------------

def margin_buy_order(coin_to_trade:str,order_quantity:float):
    order = client.create_margin_order(symbol=coin_to_trade,side=SIDE_BUY,type=ORDER_TYPE_MARKET,quantity=order_quantity)

def margin_sell_order(coin_to_trade:str,order_quantity:float):
    order = client.create_margin_order(symbol=coin_to_trade,side=SIDE_SELL,type=ORDER_TYPE_MARKET,quantity=order_quantity)

def write_json(text):
    with open('./test.json','r') as f:
        j = json.load(f)
        j.append(text)
    with open('./test.json','w') as f:
        json.dump(j,f,indent= 4)

def percent_calculator(x:float,y:int):
    z=x+((x*y)/100)
    return z

def margin_balance_of(coin:str):
    info = client.get_margin_account()
    for i in info['userAssets']:
        if coin=='ETH':
            if i['asset']==coin:
                balance = float(str(i['free'])[:5])

        if coin=='BTC':
            if i['asset']==coin:
                balance = float(str(i['free'])[:7])

        elif i['asset']==coin:
            balance = round((float(str(i['free'])[:4])),3)
    return balance


def order_quantity_of(balance:float,coin:str):
    
    coin_ticker_usd = client.get_symbol_ticker(symbol=coin+'USDT')
    coin_price_usd= float(coin_ticker_usd['price'])
    coin_ticker = client.get_symbol_ticker(symbol=coin+'BTC')
    coin_price = float(coin_ticker['price'])
    if coin=='ETH':
        q = balance / coin_price
        q =float(str(q)[:5])
    if coin!='ETH':
        if 500<=coin_price_usd<=700:
            q = balance / coin_price
            q =float(str(q)[:5])

        elif 16<=coin_price_usd<=49:
            q = balance / coin_price
            q =float(str(q)[:3])

        elif 0<=coin_price_usd<=15:
            q = balance / coin_price
            q =float(str(q)[:2])
    return q
    


#---------------------------------------------------------------



while True:


    #--------process to choose a crypto to trade with----------------------
    if search_coin:
        tickers = client.get_ticker()


        list_of_crypto = ['DOGE','ETH','XRP','BNB','LTC','BCH']
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
                if (i+'BTC') == ticker['symbol']:
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
        n = random.randint(0,5)#pick a random crypto
        coin_to_trade = crypto_info.iloc[n]['symbol']
        coin = str(coin_to_trade.replace('BTC',''))# coin that i am using
        #price change percent
        price_change = crypto_info.iloc[n]['priceChangePercent']
        print(f'crypto that we gonna use is {coin_to_trade}, price change = {price_change}%')
        #---------------------------------------------------------------------------------------------
        #----------------boucle pour recuperer le prix-------------
        coin_ticker = client.get_symbol_ticker(symbol=coin_to_trade)
        coin_price = float(coin_ticker['price'])

        print('prix recuperer')
    #---------------------------------------------------------------



    print(coin_to_trade)
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
    klines['SMA_30'] = klines.iloc[:,1].rolling(window=30).mean()

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
    if klines.loc[0]['SMA_30']>klines.loc[0]['SMA_50']:
        print("SMA_30 > SMA_50")
        Sma_signal_sell = False
        Sma_signal_buy = True

        print('SMA signal buy')

    #si SMA9 est inferieur a SMA15
    if klines.loc[0]['SMA_30'] < klines.loc[0]['SMA_50']:
        print("SMA_30 < SMA_50")
        Sma_signal_sell = True
        Sma_signal_buy = False
        profit_of_3_percent = False # pour rester dans le profit
        print('SMA signal sell')

    price_trick = False # pour voir si le marche ne triche pas
        #le prix inferieur a SMA 9             le prix inferieur ou egale a valeur de SMA 15 -30 and SMA9 est superieur a SMA15
    if coin_price < klines.loc[0]['SMA_30'] and coin_price<=(klines.loc[0]['SMA_50']) and (klines.loc[0]['SMA_30']>klines.loc[0]['SMA_50']):
        print("price under SMA9 and SMA15. SELL")
        Sma_signal_sell = True
        Sma_signal_buy = False
        price_trick = True



    #------------------------------_-

    sell_for_profit = False #declencheur de take profit
    sell_for_loss = False #declencheur de stop loss



    if profit_target_price == coin_price:
        print('Profit of 2%, SELL')
        sell_for_profit=True

    if loss_target_price == coin_price:
        print('loss of 2%,SELL')
        sell_for_loss= True





#-----------------------


    if Sma_signal_buy and have_btc and not profit_of_3_percent:

        balance = margin_balance_of('BTC')
        #order_quantity=balance / coin_price
        order_quantity = order_quantity_of(balance,coin)

        print('sma signal buy and have BTC')
        #try:
        #buy order
        margin_buy_order(coin_to_trade,order_quantity)
        #-------------------------
        print(f' {datetime.datetime.now()} bought {order_quantity}{coin} of {float(order_quantity*coin_price)} at {coin_price} \n')
        Have_other_coin = True #don't have BTC
        have_btc = False # have btc
        search_coin = False#don't search coin until i sell it


        operation = 'Buy'


        profit_target_price = percent_calculator(coin_price,2)#target profit price
        loss_target_price = percent_calculator(coin_price,-2)#stop loss


        now_time = datetime.datetime.now()

        now_time = now_time.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        #--------------------------------------------

        trade_details = {'time':now_time,'symbol':coin,'operation':operation,'quantity':order_quantity,'price':coin_price}
        write_json(trade_details)


        #except:

        #    print('erreur lors de l achat')

        #    pass



    if Sma_signal_buy and Have_other_coin:
        print('No BTC for BUY ORDER')

    #-------------------------------------



    if Sma_signal_sell or sell_for_profit or sell_for_loss:

        if Have_other_coin:
            balance = margin_balance_of(coin)
            order_quantity = balance
            print(f'sma signal sell and have {coin}')
            #sell order
            margin_sell_order(coin_to_trade,order_quantity)
            #sell_order
            print(f'{datetime.datetime.now()} sold {order_quantity}{coin} of {(float(order_quantity*coin_price))} at {coin_price} ')
            have_btc = True # have BTC
            Have_other_coin = False #don't have BTC,meaning i have a crypto
            search_coin = True#search for another coin
            operation = 'Sell'


            now_time = datetime.datetime.now()
            now_time = now_time.strftime("%d-%b-%Y (%H:%M:%S.%f)")
            #--------------------------------------------
            trade_details = {'time':now_time,'symbol':coin,'operation':operation,'quantity':order_quantity,'price':coin_price}
            write_json(trade_details)
        
            #    print('erreur lors du vente')
            if sell_for_profit:
                profit_of_3_percent =True


    if Sma_signal_sell and have_btc:
        print(f'No {coin} for SELL ORDER')
        search_coin=True


    print('------------------------------------\n')

    time.sleep(3)











