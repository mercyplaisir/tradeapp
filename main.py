import json
import numpy as np
import pandas as pd
from binance.client import Client
from binance.enums import *
import math
import datetime
import time
import e # contain os environ that contain binance  keys

#boucle pour se connecter
disconnected = True
while disconnected:
    try :
        client = Client(e.api_key, e.secret_key)
        print("vous etes connecter\n")
        disconnected = False
        connected = True
    except:
        print("impossible de se connecter\nveuillez patientez\n")


#---------fin-------------

#-------------------------------------


usdt_traded = True #it mean i have usdt in my wallet
btc_traded = False #it mean i have btc in my wallet


#------------------------------------------------
while True:
    #boucle pour recuperer le prix
    btc_price = client.get_margin_price_index(symbol='BTCUSDT')
    btc_price = float(btc_price['price'])

    print('------------------------------------')
    print('prix recuperer')


    #-----fin------------


    #-------pou recuperer les SMA-----------------------
    # fetch 1 minute klines for the last day up until now
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    print('klines recuperer')

    #changer timestamp en date
    for kline in klines:
        kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)

    klines = pd.DataFrame(klines)#changer en dataframe
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

    #------------------Fin-----------------------------

        #--------pour recuperer la balance---------------
        #boucle pour recuperer les infos
    get_info_error = True
    while get_info_error:
        #get all the info of my  account
        try:
            info = client.get_margin_account()

            print('info recuperer')
            get_info_error = False
        except:
            print('impossible de recuperer les infos')
    balance_dataframe= pd.DataFrame(info['userAssets'])

    #supprimer BNB pour qu'il ne nous derange pas
    balance_dataframe.drop(index=52,inplace=True)

    #sort the portfolio by the quantity
    if usdt_traded:
        #sort the portfolio by the quantity
        balance_dataframe.sort_values('free',ascending= False, inplace= True)
        #refaire les index
        balance_dataframe.reset_index(inplace = True)

        #supprimer un colonnes pas important
        balance_dataframe.drop(columns=['index'],inplace=True)

    if btc_traded:
        balance_dataframe.drop(index=3,inplace=True)
        #sort the portfolio by the quantity
        balance_dataframe.sort_values('free',ascending= False, inplace= True)
        #refaire les index
        balance_dataframe.reset_index(inplace = True)

        #supprimer un colonnes pas important
        balance_dataframe.drop(columns=['index'],inplace=True)


    if btc_traded:
        print('i have btc')
    if usdt_traded:
        print('i have usdt')

    #--------fin--------------------

    Sma_signal_buy = False
    Sma_signal_sell = False
    Have_usdt = False
    Have_btc = False
    Have_not_btc = False
    Have_not_usdt = False

    #si SMA9 est superieur a SMA15
    if klines.loc[0]['SMA_15']>klines.loc[0]['SMA_50']:
        print("SMA_15 > SMA_50")
        Sma_signal_sell = False
        Sma_signal_buy = True
        print('time to buy')

    #si SMA9 est inferieur a SMA15
    if klines.loc[0]['SMA_15'] < klines.loc[0]['SMA_50']:
        print("SMA_15 < SMA_50")
        Sma_signal_sell = True
        Sma_signal_buy = False
        print('time to sell')

    price_trick = False # pour voir si le marche ne triche pas
       #le prix inferieur a SMA 9             le prix inferieur ou egale a valeur de SMA 15 -30 and SMA9 est superieur a SMA15
    if btc_price < klines.loc[0]['SMA_15'] and btc_price<=(klines.loc[0]['SMA_50']-90) and (klines.loc[0]['SMA_15']>klines.loc[0]['SMA_50']):
        print("price under SMA9 and SMA15. SELL")
        Sma_signal_sell = True
        Sma_signal_buy = False
        price_trick = True


    #si je n'ais pas de btc et que j'ai le usdt dans ma wallet
    if balance_dataframe.loc[0]['asset'] == 'USDT':

        Have_usdt = True
        Have_btc = False
        Have_not_btc = True



    # #si je n'ais pas de usdt et que j'ai le btc dans ma wallet
    if balance_dataframe.loc[0]['asset'] == 'BTC':

        Have_usdt = False
        Have_btc = True
        Have_not_usdt = True

    #-----------------------------------------------------------------



    if Sma_signal_buy and Have_usdt:
        x = balance_dataframe.loc[0]['free']
        x= x[:6]
        x = float(x)
        order_quantity=x / btc_price
        order_quantity = float(str(order_quantity)[:7])
        order_quantity
        try:
            #buy order
            order = client.create_margin_order(symbol='BTCUSDT',side=SIDE_BUY,type=ORDER_TYPE_MARKET,quantity=order_quantity)
            #-------------------------
            print(' {} bought btc of {} at {} \n'.format(datetime.datetime.now(),(float(order_quantity*btc_price)), btc_price))
            usdt_traded = False #don't have usdt
            btc_traded = True # have btc
        except:
            i=0
            if i==15:
                print('15 times with error to sell')
                break
            i+=1
            pass



    if Sma_signal_buy and Have_not_usdt:
        print('No usdt for BUY ORDER')


    if Sma_signal_sell and Have_btc :
        x = balance_dataframe.loc[0]['free']
        x= x[:7]
        order_quantity = float(x)

        #sell order
        try:
            order = client.create_margin_order(symbol='BTCUSDT',side=SIDE_SELL,type=ORDER_TYPE_MARKET,quantity=order_quantity)
            #sell_order
            print(' {} sold btc of {} at {} \n'.format(datetime.datetime.now(),(float(order_quantity*btc_price)), btc_price))
            usdt_traded = True # have usdt
            btc_traded = False #don't have btc
        except:
            i=0
            if i==15:
                print('15 times with error to sell')
                break
            i+=1
            pass


    if Sma_signal_sell and Have_not_btc:
        print('No BTC for SELL ORDER')


    time.sleep(5)



