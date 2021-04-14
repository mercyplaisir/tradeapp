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


bnb_traded = False #it mean i have bnb in my wallet
btc_traded = True #it mean i have btc in my wallet


#------------------------------------------------
while True:
    #boucle pour recuperer le prix
    prices = client.get_all_tickers()
    bnb_price = float(prices[11]['price'])
    print('------------------------------------')
    print('prix recuperer')


    #-----fin------------


    #-------pou recuperer les SMA-----------------------
    # fetch 1 minute klines for the last day up until now
    klines = client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    print('klines recuperer')

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


    if bnb_traded:
    #sort the portfolio by the quantity
        balance_dataframe.sort_values('free',ascending= False, inplace= True)

    #refaire les index
    balance_dataframe.reset_index(inplace = True)

    #supprimer un colonnes pas important
    balance_dataframe.drop(columns=['index'],inplace=True)
    #supprimer les deux indexes suivant le premier puisque il peut nuire l'algorithme

    balance_dataframe.drop(index=[1,2],inplace=True)
    
    if bnb_traded:
        print('i have btc')
    if btc_traded:
        print('i have bnb')

    #--------fin--------------------

    Sma_signal_buy = False
    Sma_signal_sell = False
    Have_bnb = False
    Have_btc = False
    Have_not_btc = False
    Have_not_bnb = True

    #si SMA9 est superieur a SMA15
    if klines.loc[0]['SMA_9']>klines.loc[0]['SMA_15']:
        print("SMA_9 > SMA_15")
        Sma_signal_sell = False
        Sma_signal_buy = True
        print('time to buy')

    #si SMA9 est inferieur a SMA15
    if klines.loc[0]['SMA_9'] < klines.loc[0]['SMA_15']:
        print("SMA_9 < SMA_15")
        Sma_signal_sell = True
        Sma_signal_buy = False
        print('time to sell')

    price_trick = False # pour voir si le marche ne triche pas
       #le prix inferieur a SMA 9             le prix inferieur ou egale a valeur de SMA 15 -30 and SMA9 est superieur a SMA15
    if bnb_price < klines.loc[0]['SMA_9'] and bnb_price<=(klines.loc[0]['SMA_15']-30) and (klines.loc[0]['SMA_9']>klines.loc[0]['SMA_15']):
        print("price under SMA9 and SMA15. it's a trick")
        Sma_signal_sell = True
        Sma_signal_buy = False
        price_trick = True


    #si je n'ais pas de btc et que j'ai le bnb dans ma wallet
    if balance_dataframe.loc[0]['asset'] == 'BNB':
        
        Have_bnb = True
        Have_btc = False
        Have_not_btc = True



    # #si je n'ais pas de bnb et que j'ai le btc dans ma wallet
    if balance_dataframe.loc[0]['asset'] == 'BTC':
        
        Have_bnb = False
        Have_btc = True
        Have_not_bnb = True
        
    #-----------------------------------------------------------------


    if price_trick:
        print("dont buy just sell")


    if Sma_signal_buy and Have_btc:
        x = balance_dataframe.loc[0]['free']
        x= x[:6]
        x = float(x)- 2
        #buy order
        buy_order = client.order_market_buy(symbol='BNBBTC',quantity=x)
        buy_order
        print(' {} bought bnb at {} \n'.format(datetime.datetime.now(),bnb_price))
        bnb_traded = False
        btc_traded = True

    if Sma_signal_buy and Have_not_btc:
        print('No money for BUY ORDER')
    

    if Sma_signal_sell and Have_bnb :
        x = balance_dataframe.loc[0]['free']
        x= x[:4]
        x = float(x)
        
        #sell order
        sell_order = client.order_market_sell(symbol='BNBBTC',quantity=x)
        
        sell_order
        print(' {} sold bnb of {} \n'.format(datetime.datetime.now(),(float(balance_dataframe.loc[0]['free'])*bnb_price)))
        bnb_traded = True
        btc_traded = False

    
    if Sma_signal_sell and Have_not_bnb:
        print('No bnb for SELL ORDER')
    

    time.sleep(10)
   


