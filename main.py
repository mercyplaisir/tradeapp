import json
import numpy as np
import pandas as pd
from binance.client import Client
import e #contains the api and secret keys
import math
import Coinpaprika
import datetime
import time


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




#------------------------------------------------
while True:
    #boucle pour recuperer le prix
    btc_price = client.get_avg_price(symbol='BTCUSDT')
    btc_price = float(btc_price['price'])
    btc_price
    print('prix recuperer\n')


    #-----fin------------


    #-------pou recuperer les SMA-----------------------
    # fetch 1 minute klines for the last day up until now
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    print('klines recuperer\n')

    #changer timestamp en date
    for kline in klines:
        kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3) 

    klines = pd.DataFrame(klines)#changer en dataframe
    klines.drop(columns=[1,2,3,5,6,7,8,9,10,11],inplace= True)#supprimer les collonnes qui ne sont pas necessaires
    klines.columns = ['open_time','close_price']#renommer les colonnes

    #creer un SMA9
    klines['SMA_9'] = klines.iloc[:,1].rolling(window=9).mean()

    #creer un SMA15
    klines['SMA_15'] = klines.iloc[:,1].rolling(window=15).mean()

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

            info = client.get_account()
            print('info recuperer')
            get_info_error = False

        except:
            print('impossible de recuperer les infos')


    #create a dataframe that store and study the balances
    balance_dataframe= pd.DataFrame(info['balances'])


    #sort the portfolio by the quantity
    balance_dataframe.sort_values('free',ascending= False, inplace= True)

    #refaire les index
    balance_dataframe.reset_index(inplace = True)

    #supprimer un colonnes pas important
    balance_dataframe.drop(columns=['index'],inplace=True)
    #supprimer les deux indexes suivant le premier puisque il peut nuire l'algorithme

    balance_dataframe.drop(index=[1,2],inplace=True)

    #--------fin--------------------

    #si SMA9 est superieur a SMA15
    if klines.loc[0]['SMA_9']>klines.loc[0]['SMA_15']:
        print("SMA_9 > SMA_15")
        Sma_signal_buy = True
        print('time to buy\n')

    #si SMA9 est inferieur a SMA15
    if klines.loc[0]['SMA_9'] == klines.loc[0]['SMA_15']:
        print("SMA_9 < SMA_15")
        Sma_signal_sell = True
        print('tmie to sell\n')


    #si je n'ais pas de USDT et que j'ai le BTC dans ma wallet
    if balance_dataframe.loc[0]['asset'] == 'BTC':

        Have_Btc = True
        Have_Usdt = False

        #sell order
        sell_order = client.order_market_sell(symbol='BNBBTC',quantity=balance_dataframe.loc[0]['free'])

    # #si je n'ais pas de BTC et que j'ai le USDT dans ma wallet
    if balance_dataframe.loc[0]['asset'] == 'USDT':
        Have_Btc = False
        Have_Usdt = True

        #buy order
        buy_order = client.order_market_buy(symbol='BTCUSDT',quantity=(float(balance_dataframe.loc[0]['free'])/btc_price))

    #-----------------------------------------------------------------


    try:
        if Sma_signal_buy and Have_Usdt:
            buy_order
            print(' {} bought btc at {} \n'.format(datetime.datetime.now(),btc_price))

    except:
        pass   

    try:
        if Sma_signal_sell and Have_Btc :
            sell_order
            print(' {} sold btc of {} \n'.format(datetime.datetime.now(),(float(balance_dataframe.loc[0]['free'])*btc_price)))
    except:
        pass
    
    time.sleep(3)
    print('retour a la ligne')






























































