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
from tools import *

apikey='eKDyjsVeMhssfXL89oil2keouZSfpnJwqJV3mfvApOYDylfUjGc6hKAtapQIHL3b'
secretkey='hISw2v7P96RXq698sIQVUGHfhX3Jt8aqh9FOlURGfXFwelYKq1R5oPfUbfWtD9lo'



#------------boucle pour se connecter---------------------
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


have_btc = True # have BTC
Have_other_coin = False #don't have BTC,meaning i have a crypto

show_trade_info = False #pour montrer les infos sur le terminal

sell_order = False
buy_order = False

profit_target_price = 0 #mon take profit price
loss_target_price = 0 #mon stop loss price
bought_at= 0 #le prix auxquelle j'ai achete
now_price = 0 #prix actuelle
percent_of_profit = 0 #percent iim making in a trade



search_coin = True

#---------------------------------------------------------------

#---------------------------------------------------------------

time_when_passing_order = 0
time_now =0
time_passed_in_trade =  0

while True:
    print(datetime.datetime.now())

    #--------process to choose a crypto to trade with----------------------
    if search_coin:
        
        info_for_coin = coin_for_trade()

        coin_to_trade = info_for_coin['coin to trade']
        coin = str(coin_to_trade.replace('BTC',''))# coin that i am using
        #price change percent
        price_change = info_for_coin['price change']
        print(f'crypto that we gonna use is {coin_to_trade}, price change = {price_change}%')
        #---------------------------------------------------------------------------------------------

        coinGoodForUse = coin_approvement(coin_to_trade)#get the trend and the price tricks


        if coinGoodForUse:
            buy_order = True
            sell_order = False
        



    #---------------pour recuperer le prix-------------
    coin_price = get_coin_price(coin_to_trade)

    print('prix recuperer')
    #---------------------------------------------------------------

    print(coin_to_trade)


    



    #------------------------------_-


    if 0!=profit_target_price <= coin_price:
        print('Profit of 1%, SELL')
        sell_order = True
        buy_order = False

    if 0!=loss_target_price >= coin_price:
        print('loss of 1%,SELL')
        sell_order = True
        buy_order = False


    time_now = datetime.datetime.timestamp(datetime.datetime.now())


    if show_trade_info:
        nowPriceMoves = check_price_moves(coin_to_trade)
        if nowPriceMoves: #if true there is price trick
            sell_order = True
            buy_order = False
        #-------------------------------
        time_passed_in_trade =  time_now - time_when_passing_order
        print(f"bought at {bought_at}\ntake profit at {profit_target_price}\nstop loss at {loss_target_price}\nnow price{coin_price}\n")
        percent_of_profit = percent_change(bought_at,coin_price)
        print(percent_of_profit)


    #pour ne passer que 2heures dans une trade
    if time_when_passing_order>0 and  time_passed_in_trade >10800:
        sell_order = True
        buy_order = False


    



#-----------------------


    if buy_order and have_btc:

        balance = margin_balance_of('BTC')
        #order_quantity=balance / coin_price
        order_quantity = order_quantity_of(balance,coin)

        #print('sma signal buy and have BTC')
        #try:
        #buy order
        margin_buy_order(coin_to_trade,order_quantity)
        #-------------------------
        print(f' {datetime.datetime.now()} bought {order_quantity}{coin} of {float(order_quantity*coin_price)} at {coin_price} \n')
        Have_other_coin = True #don't have BTC
        have_btc = False # have btc
        search_coin = False#don't search coin until i sell it

        compteur_pour_searchcoin=0 #counter of searching coin initialized
        percent_of_profit = 0 #percent i'm making in a trade initialize

        time_when_passing_order = datetime.datetime.timestamp(datetime.datetime.now())#time when passing order

        bought_at = coin_price
        operation = 'Buy'


        profit_target_price = percent_calculator(coin_price,0.3)#target profit price
        loss_target_price = percent_calculator(coin_price,-1)#stop loss

        show_trade_info = True

        now_time = datetime.datetime.now()

        now_time = now_time.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        #--------------------------------------------

        trade_details = {'time':now_time,'symbol':coin,'operation':operation,'quantity':order_quantity,'price':coin_price}
        write_json(trade_details)


        #except:

        #    print('erreur lors de l achat')

        #    pass




    if buy_order and Have_other_coin:
        print('No BTC for BUY ORDER')

    #-------------------------------------



    if sell_order and Have_other_coin:
        balance = margin_balance_of(coin)
        order_quantity = balance
        print(f'sell_order of {coin}')
        #sell order
        margin_sell_order(coin_to_trade,order_quantity)
        #sell_order
        print(f'{datetime.datetime.now()} sold {order_quantity}{coin} of {(float(order_quantity*coin_price))} at {coin_price} ')
        have_btc = True # have BTC
        Have_other_coin = False #don't have BTC,meaning i have a crypto
        search_coin = True #search for another coin
        operation = 'Sell'

        profit_target_price = 0
        loss_target_price = 0


        now_time = datetime.datetime.now()
        now_time = now_time.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        #--------------------------------------------
        trade_details = {'time':now_time,'symbol':coin,'operation':operation,'quantity':order_quantity,'price':coin_price}
        write_json(trade_details)

        show_trade_info = False

        compteur_pour_searchcoin=0 #counter of searching coin initialized
        percent_of_profit = 0 #percent i'm making in a trade initialized

        time_when_passing_order = 0
        time_passed_in_trade = 0
        #    print('erreur lors du vente')



    if sell_order and have_btc:
        print(f'No {coin} for SELL ORDER')
        search_coin=True

    print(time_passed_in_trade)

    print('------------------------------------\n')

    time.sleep(3)
