from random import randint
import datetime
import sys
sys.path.append(sys.path[0] + '/..')

import json
import pandas as pd
import websocket
from binance.client import Client
from binance.enums import *
from binance.exceptions import *
import mysql.connector

from view.tools import BINANCEKLINES, APIKEYPATH, Tool as tl
from view.VirtualAccount import VirtualAccount


"""
varaibles :
            - apiPublicKey
            - apiSecretKey
            - list_of_crypto



functions in  this file:
                        - init
                        - connect
                        - margin_buy_order
                        - margin_sell_order
                        - buyOrder
                        - sellOrder
                        - balance
                        - margin_balance_of
                        - order _quantity_of
                        - get_klines
                        
                        - coinPriceChange
                        - getCryptoList
                        - saveTrades_DB




"""


class Binance:

    def __init__(self):
        #try:
        
        self.apikeys: dict = tl.read_json(APIKEYPATH)  # get all key
        
        self.apiPublicKey: str = self.apikeys["public key"]  # public key
        self.apiSecretKey: str = self.apikeys["secret key"]  # secret key

        self.lastOrderWasBuy = False
        

        
        self.connect()  # connect to Binance
        #self.bdConnect()  # connect to database
        #self.saveBalances_BD()

        self.baseCoin: str = "BTC"
        self.timeframe: str = "15m"
        self.virtualAccount = VirtualAccount(baseCoin= self.baseCoin)
        #except:
        #    print("erreur de connexion")

        self.db = {'host' : 'localhost',
                   'user' : 'root',
                   'passwd' : 'Pl@isir6',
                   'database' : 'bot'}

        print(">>>connection a BINANCE effectue avec succes")
        

    def connect(self):
        while True:
            try:
                self.client = Client(self.apiPublicKey, self.apiSecretKey)

                break
            except:
                print("erreur de connexion\nretry...")

    def bdConnect(self):
        try:
            self.mydb = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='Pl@isir6',
                database='bot'
            )

        except:
            print("BD connection error")

    # placer un ordre d'achat
    def margin_buy_order(self, coin_to_trade: str):
        """A margin buy order"""

        # coinName: str = coin_to_trade.replace(self.baseCoin, '')
        order_quantity: int = self.orderQuantity(self.baseCoin)

        self.client.create_margin_order(
            symbol=coin_to_trade, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=order_quantity)

        self.saveTrades_DB(
            coin_to_trade=coin_to_trade,
            quantity=order_quantity,
            orderType="margin buy"
        )
        #self.saveBalances_BD()

    def margin_sell_order(self, coin_to_trade: str):
        """ A margin sell order 
        coin_to_trade .ex:BNBBTC, BTCUSDT
        """
        coinName: str = coin_to_trade.replace(self.baseCoin, '')
        order_quantity: int = self.orderQuantity(coinName)

        self.client.create_margin_order(
            symbol=coin_to_trade, side=SIDE_SELL, type=ORDER_TYPE_MARKET, quantity=order_quantity)

        self.saveTrades_DB(
            coin_to_trade=coin_to_trade,
            quantity=order_quantity,
            orderType="margin sell"
        )
        #self.saveBalances_BD()

    def buyOrder(self, coin_to_trade: str):
        """
        Market Buy Order
        coin_to_trade .ex:BNBBTC, BTCUSDT
        """
        """
        # coinName: str = coin_to_trade.replace(self.baseCoin, '')
        order_quantity: int = self.orderQuantity(self.baseCoin)

        self.client.order_market_buy(
            symbol=coin_to_trade, quantity=order_quantity)

        self.saveTrades_DB(
            coin_to_trade=coin_to_trade,
            quantity=order_quantity,
            orderType="market buy"
        )
        self.saveBalances_BD()
        """

        self.virtualAccount.virtualBuy(
            coin_to_trade=coin_to_trade,
            order_quantity=self.orderQuantity(self.baseCoin)
        )



    def sellOrder(self, coin_to_trade: str):
        """
        Market sell Order

        coin_to_trade .ex:BNBBTC, BTCUSDT
        """
        coinName: str = coin_to_trade.replace(self.baseCoin, '')
        """
        order_quantity: int = self.orderQuantity(coinName)

        self.client.order_market_sell(
            symbol=coin_to_trade, quantity=order_quantity)

        self.saveTrades_DB(
            coin_to_trade=coin_to_trade,
            quantity=order_quantity,
            orderType="market sell"
        )

        self.saveBalances_BD()"""
        coinInfo = Binance.coinPriceChange(coinName + self.baseCoin)
        coin_price = coinInfo['price']
        
        self.virtualAccount.virtualSell(
            coin_to_trade = coin_to_trade,
            order_quantity = self.orderQuantity(coinName),
            coinPrice = coin_price
        )

    def assetBalance(self, coin: str):
        """
        coin balance

        coin :ex:BTC,ETH
        """
        info = self.client.get_asset_balance(asset=coin)
        return info

    def orderQuantity(self, coin: str) :
        """
        parameters: -balance. ex: 20$
                    -coin. ex: BTC,ETH

        for use when buying

        return quantity(float)
        """
        if coin==self.baseCoin:
            # il determine la quantite a utiliser pour placer un ordre en analysant so prix
            mycursor = self.mydb.cursor()
            mycursor.execute(
                f"select Balance.quantity from Balance where Balance.coinName = {coin}")
            resultat = mycursor.fetchall()
            balance = resultat[0][0]

            coinInfo_USD = Binance.coinPriceChange(coin + 'USDT')
            coinInfo = Binance.coinPriceChange(coin + self.baseCoin)

            coin_price_usd = coinInfo_USD['price']
            coin_price = coinInfo['price']
            if coin == 'ETH':
                q = balance / coin_price
                q = float(str(q)[:5])
                return q
            elif coin != 'ETH':
                if coin_price_usd >= 5000:  # si le prix est superieur a 5000
                    q = balance / coin_price
                    q = float(str(q)[:6])
                    return q

                elif 50 <= coin_price_usd < 5000:  # si le prix est entre 50
                    q = balance / coin_price
                    q = float(str(q)[:5])
                    return q

                elif 16 <= coin_price_usd <= 49 or coin_price < 0.18:  # si le prix est entre 16 et 49
                    q = balance / coin_price
                    q = float(str(q)[:3])
                    return q

                elif 0.18 <= coin_price_usd <= 15:  # si le prix est entre 0 et 15
                    q = balance / coin_price
                    q = float(str(q)[:2])
                    return q

            # q c'est la quantite
        elif coin != self.baseCoin:
            mycursor = self.mydb.cursor()
            mycursor.execute(
                f"select quantity from Balance where coinName = {coin}")

            resultat = mycursor.fetchall()
            balance:float = resultat[0][0]

            return balance


    def getCryptoList(self) -> list:
        """
        return list of crypto from database
        """
        mycursor = self.mydb.cursor()
        mycursor.execute("select coinName from Coin ")
        myresult = mycursor.fetchall()
        listcrypto = []
        for i in myresult:
            listcrypto.append(i[0].upper() + self.baseCoin)  # get "bnb" and add basecoin and get BNBBTC or BNBUSDT
        print(">>>got the list of crypto")
        return listcrypto

    def saveTrades_DB(self, coin_to_trade: str, orderType: str, quantity: float):
        coinName = coin_to_trade.replace(self.baseCoin, '')
        """mycursor = self.mydb.cursor()

        mycursor.execute(
            f"insert into Trades(coinName,crypto,quantity,orderType,tradeTime) values({coinName},{coin_to_trade},{quantity},{orderType},{datetime.datetime.now()})")
        """
        requete = f"insert into Trades(coinName,crypto,quantity,orderType,tradeTime) values({coinName},{coin_to_trade},{quantity},{orderType},{datetime.datetime.now()})"
        tl.requestBD(requete=requete,kwargs=self.db)
        print(">>>Trade saved")

    def saveBalances_BD(self) -> None:
        accountInfo = self.client.get_account()
        #mycursor = self.mydb.cursor()
        #mycursor.execute("delete from Balance")

        for i in range(1,accountInfo['balances'].__len__()):
            value:dict = accountInfo['balances'][i]
            coin:str = value['asset']
            quantity:int = value['free']

            #mycursor.execute(f"insert into Balance(coinName,quantity) values({coin},{quantity})")
            requete = f"insert into Balance(coinName,quantity) values({coin},{quantity})"
            tl.requestBD(requete=requete, kwargs=self.db)

    
    def get_klines(self, coin_to_trade: str = "BNBBTC", interval: str = "2 days"):
        """
        Get the klines for the timeframe given and in interval given.
        timeframe ex:1m,5m,15m,1h,2h,6h,8h,12h,1d,1M,1w,3d

        Default timeframe = 15m
        Default interval = 2 days


        colums=["open_time","open_price","close_price","SMA_30","SMA_50","SMA_20","upper_band","lower_band"]

        stores the klines in a csv file
        """

        try:
            klines_list = self.client.get_historical_klines(
                coin_to_trade, self.timeframe, f"{interval} ago UTC")
            
            # changer timestamp en date
            for kline in klines_list:
                kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)

            klines = pd.DataFrame(klines_list)  # changer en dataframe
            # supprimer les collonnes qui ne sont pas necessaires
            klines.drop(columns=[6, 7, 8, 9, 10, 11], inplace=True)

            klines.columns = ['date', 'open', 'high', 'low',
                              'close', 'volume']  # renommer les colonnes

            # trier les indexes pour que 0 correspondents avec maintenant
            # klines.sort_index(ascending=False, inplace=True)

            # refaire les index
            # klines.reset_index(inplace=True)

            # supprimer un colonnes pas important
            # klines.drop(columns='index', inplace=True)

        
            klines.to_csv(BINANCEKLINES, index=False)
            # return klines
            print(">>>klines telecharger")

        except BinanceOrderException:
            print(BinanceOrderException)
        except BinanceAPIException:
            print(BinanceAPIException)

    @classmethod
    def coinPriceChange(coin_to_trade: str = "BNBBTC"):
        """
        Return a dict: { "price": coinPrice , "pricechange": coinPriceChange }
        """
        while True:
            try:
                sockete = f"wss://stream.binance.com:9443/ws/{coin_to_trade.lower()}@kline_1d"
                was = websocket.create_connection(sockete)

                json_result = was.recv()
                was.close()
                dict_result = json.loads(json_result)

                dict_result['k']['priceChange'] = tl.percent_change(float(dict_result['k']['o']),
                                                                      float(dict_result['k']['c']))

                b = {'price': float(dict_result['k']['c']), 'priceChange': float(
                    dict_result['k']['priceChange'])}
                break
            except:
                pass

        return b

    def cryptoToTrade(self):
        """
        Return a crypto to trade
        """
        self.list_of_crypto = self.getCryptoList()

        listLength = self.list_of_crypto.__len__()
        cryptoIndex = randint(0, listLength-1)
        cryptoToUse = self.list_of_crypto[cryptoIndex]

        return cryptoToUse
