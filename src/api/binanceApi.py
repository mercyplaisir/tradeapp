import asyncio
import datetime
import json
from pathlib import Path
from random import randint

import pandas as pd
from binance import AsyncClient
from binance.client import Client

from src.controller.dbcontroller.mysqlDB import mysqlDB
from src.controller.tools import BINANCEKLINES, Tool as tl


class BinanceWebsocket:

    def coinPriceInfo(self, cryptopair: str = None) -> dict[str, float]:
        """
        Return a dict: { "price": coinPrice , "pricechange": coinPriceChange }
        """

        async def main():
            client = await AsyncClient.create()
            klines = await client.get_klines(symbol=cryptopair, interval='1d')
            await client.close_connection()
            kline = klines[-1]  # today's klines

            kline[0] = str(datetime.datetime.fromtimestamp(int(kline[0] / 1000)))  # open date
            kline[6] = str(datetime.datetime.fromtimestamp(int(kline[6] / 1000)))  # close date
            return {'price': float(kline[4]), 'priceChange': tl.percent_change(float(kline[1]), float(kline[4]))}

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(main())


class Binance(BinanceWebsocket):
    PATH = str(Path(__file__).resolve().parent)
    """__all__ = ['PLcalculator','assetBalance', 'buyOrder', 'coinPriceChange',
               'connect', 'cryptoToTrade', 'getCryptoList',
               'get_klines', 'orderQuantity',
               'saveBalances_BD', 'saveTrades_DB', 'sellOrder']"""

    def __init__(self, publickey: str = None, secretkey: str = None, coin: str = None):
        super().__init__()
        # try:
        # get all key
        # self.apikeys: dict = tl.read_json(APIKEYPATH)

        self.apiPublicKey: str = publickey  # public key
        self.apiSecretKey: str = secretkey  # secret key
        self.client = None  # instance of Binance

        self.lastOrderWasBuy = False

        self.connect()  # connect to Binance

        self._coin: str = coin  # coin that i possess in initialization
        # assert coin , "coin can't be empty"

        self.timeframe: str = "15m"

        # except:
        #    print("erreur de connexion")

        self.database = mysqlDB()
        print(">>>Initialisation terminee")

        self.boughtAt = 0
        self.soldAt = 0

    def connect(self):
        while True:
            try:
                self.client = Client(self.apiPublicKey, self.apiSecretKey)

                print(">>>connection a BINANCE effectue avec succes")
                break
            except Exception:
                print("erreur de connexion\nretry...")

    def buyOrder(self, cryptopair: str):
        """
        Market Buy Order
        cryptopair .ex:BNBBTC, BTCUSDT
        """

        # coinName: str = cryptopair.replace(self.coin, '')
        order_quantity: int = self.orderQuantity(self.coin)

        self.client.order_market_buy(
            symbol=cryptopair, quantity=order_quantity)

        self.saveTrades_DB(
            cryptopair=cryptopair,
            quantity=order_quantity,
            orderType="market buy"
        )
        self.saveBalances_BD()

        self.lastOrderWasBuy = True
        print(">>>Buy Order passed")

    def sellOrder(self, cryptopair: str):
        """
        Market sell Order

        cryptopair .ex:BNBBTC, BTCUSDT
        """
        coinName: str = cryptopair.replace(self.coin, '')

        order_quantity: int = self.orderQuantity(coinName)

        self.client.order_market_sell(
            symbol=cryptopair, quantity=order_quantity)

        self.saveTrades_DB(
            cryptopair=cryptopair,
            quantity=order_quantity,
            orderType="market sell"
        )

        self.saveBalances_BD()

        self.lastOrderWasBuy = False
        print(">>>Sell Order passed")

    def assetBalance(self, coin: str):
        """
        coin balance

        coin :ex:BTC,ETH
        """
        info = self.client.get_asset_balance(asset=coin)
        return info

    def orderQuantity(self, coin: str):
        """
        parameters: -balance. ex: 20$
                    -coin. ex: BTC,ETH

        for use when buying

        return quantity(float)
        """
        if coin != self.coin:
            # il determine la quantite a utiliser pour placer un ordre en analysant so prix
            # mycursor = self.mydb.cursor()
            # mycursor.execute(
            #    f"select quantity from Balance where coinName = {coin}")

            requete = f"select quantity from Balance where coinName = {self.coin}"
            resultat = self.database.selectDB(requete)
            balance: float = resultat[0]

            coin_price_usd = self._get_price(coin + 'USDT')  # prix en dollar
            coin_price = self._get_price(coin + self.coin)  # prix avec le quotecoin
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
        elif coin == self.coin:
            # mycursor = self.mydb.cursor()
            # mycursor.execute(
            #    f"select quantity from Balance where coinName = {coin}")

            requete = f"select quantity from Balance where coinName = {coin}"
            resultat = self.database.selectDB(requete)
            balance: float = resultat[0]

            return balance

    def saveTrades_DB(self, cryptopair: str, orderType: str, quantity: float):
        coinName = cryptopair.replace(self.coin, '')
        """mycursor = self.mydb.cursor()

        mycursor.execute(
            f"insert into Trades(coinName,crypto,quantity,orderType,tradeTime) values({coinName},{cryptopair},{quantity},{orderType},{datetime.datetime.now()})")
        """
        requete = f"insert into Trades(coinName,crypto,quantity,orderType,tradeTime) values({coinName},{cryptopair},{quantity},{orderType},{datetime.datetime.now()})"
        self.database.requestDB(requete)

        print(">>>Trade enregistre")

    def saveBalances_BD(self) -> None:
        accountInfo = self.client.get_account()
        # mycursor = self.mydb.cursor()
        # mycursor.execute("delete from Balance")

        for i in range(1, accountInfo['balances'].__len__()):
            value: dict = accountInfo['balances'][i]
            coin: str = value['asset']
            quantity: int = value['free']

            # mycursor.execute(f"insert into Balance(coinName,quantity) values({coin},{quantity})")
            requete = f"insert into Balance(coinName,quantity) values({coin},{quantity})"
            self.database.requestDB(requete)

        print(">>>Balances saved")

    def get_klines(self, cryptopair: str = "BNBBTC", interval: str = "2 days"):
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
                cryptopair, self.timeframe, f"{interval} ago UTC")

            # changer timestamp en date
            for kline in klines_list:
                kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)

            klines = pd.DataFrame(klines_list)  # changer en dataframe
            # supprimer les collonnes qui ne sont pas necessaires
            klines.drop(columns=[6, 7, 8, 9, 10, 11], inplace=True)

            klines.columns = ['date', 'open', 'high', 'low',
                              'close', 'volume']  # renommer les colonnes
            klines.to_csv(BINANCEKLINES, index=False)
            # return klines
            print(">>>klines telecharger")

        except Exception as e:
            print(e)

    def cryptoToTrade(self):
        """
        Return a crypto to trade
        """
        self.list_of_crypto = self.getCryptoList()

        listLength = self.list_of_crypto.__len__()
        cryptoIndex = randint(0, listLength - 1)
        crypto_to_Use = self.list_of_crypto[cryptoIndex]

        print(">>>liste recuperer")
        return crypto_to_Use

    def PLcalculator(self):
        """
        PROFIT/LOSS calculator
        """
        if not self.lastOrderWasBuy:
            return tl.percent_change(self.boughtAt, self.soldAt)

    def closingApi(self):
        """
        #For an exception that could stop the running process
        #so it can close smoothly before quiting"""

        pass

    def _get_price(self, cryptopair: str = None):
        return self.coinPriceInfo(cryptopair)['price']

    def _get_price_change(self, cryptopair: str = None):
        return self.coinPriceInfo(cryptopair)['priceChange']

    @property
    def coin(self):
        with open(f"{self.PATH}/coin.json", 'r') as f:
            self._coin = json.load(f)
        return self._coin

    @coin.setter
    def coin(self, newvalue):
        with open(f"{self.PATH}/coin.json", 'w') as f:
            newvalue = json.dumps(newvalue)
            f.write(newvalue)
        self._coin = newvalue
