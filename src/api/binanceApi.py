import asyncio
import datetime
import json
import random
import time
from pathlib import Path


import pandas as pd
import requests
from binance import AsyncClient
from binance.client import Client


from src.controller.dbcontroller.mysqlDB import mysqlDB
from src.controller.tools import BINANCEKLINES, Tool as tl
from src.model.Indicators.study import Study
from src.api.apiModel import ApiModel


"""
class BinanceWebsocket:

    def coinPriceInfo(self, cryptopair: str = None) -> dict[str, float]:
        \"""
        Return a dict: { "price": coinPrice , "pricechange": coinPriceChange }
        \"\"\"

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
"""

class Binance(ApiModel):#(Study, BinanceWebsocket):
    PATH = str(Path(__file__).resolve().parent)
    """__all__ = ['PLcalculator','assetBalance', 'buyOrder', 'coinPriceChange',
               'connect', 'cryptoToTrade', 'getCryptoList',
               'get_klines', 'orderQuantity',
               'saveBalances_BD', 'saveTrades_DB', 'sellOrder']"""

    def __init__(self, publickey: str = None, secretkey: str = None, coin: str = None):
        super().__init__()

        self.apiPublicKey: str = publickey  # public key
        self.apiSecretKey: str = secretkey  # secret key
        # self.client = None  # instance of Binance

        self.lastOrderWasBuy = False

        self.client = self.connect()  # connect to Binance

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
                client = Client(self.apiPublicKey, self.apiSecretKey)

                print(">>>connection a BINANCE effectue avec succes")
                break
            except Exception:
                print("erreur de connexion\nretry...")
        return client

    def buy_order(self, cryptopair: str):
        """
        Market Buy Order
        cryptopair .ex:BNBBTC, BTCUSDT
        """

        # coinName: str = cryptopair.replace(self.coin, '')
        order_quantity: float = self.orderQuantity(cryptopair)

        orderDetails: dict = self.client.order_market_buy(
            symbol=cryptopair, quantity=order_quantity)

        order = Order(orderDetails)
        order.save()
        self.lastOrderWasBuy = True
        print(f">>>Buy Order passed for {cryptopair}")

    def sell_order(self, cryptopair: str):
        """
        Market sell Order

        cryptopair .ex:BNBBTC, BTCUSDT
        """
        # coinName: str = cryptopair.replace(self.coin, '')

        order_quantity: float = self.orderQuantity(cryptopair)

        orderDetails: dict = self.client.order_market_sell(
            symbol=cryptopair, quantity=order_quantity)
        order = Order(orderDetails)
        order.save()
        """self.saveTrades_DB(
            cryptopair=cryptopair,
            quantity=order_quantity,
            orderType="market sell"
        )

        self.saveBalances_BD()"""

        self.lastOrderWasBuy = False
        print(">>>Sell Order passed")

    def assetBalance(self, coin: str):
        """
        coin balance

        coin :ex:BTC,ETH
        """
        info = self.client.get_asset_balance(asset=coin)
        return info

    def orderQuantity(self, cryptopair: str):
        """
                parameters: -balance. ex: 20$
                            -coin. ex: BTC,ETH

                for use when buying

                return quantity(float)
                """
        balance = self.balance  # balance of the crypto i possess
        if cryptopair.endswith(self.coin):
            basecoin = cryptopair.replace(self.coin, '')
            coin = basecoin

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
        else:

            return balance

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

    @property
    def balance(self):
        return float(self.client.get_asset_balance(self.coin))

    # _________________________________________________________________________
    # _________________________________________________________________________
    # _______________FOR VIRTUAL ONLY______________________________________________________
    # _______________STILL TESTING __________________________________________
    # _________________________________________________________________________
    # _________________________________________________________________________
    # _________________________________________________________________________

    def passOrder(self, cryptopair: str):
        cryptopair = cryptopair
        basecoin_or_quotecoin = self._basecoin_or_quotecoin(cryptopair=cryptopair, coin=self.coin)
        # price = self._get_price(cryptopair=cryptopair)
        # coin_for_order = self._getBasecoin_cryptopair(cryptopair)
        # quantity = self.orderQuantity(cryptopair)

        if basecoin_or_quotecoin == 'quotecoin':
            # BNBBTC from btc to bnb you buy
            """self._buyOrder(
                quantity=quantity,
                coin_for_order=coin_for_order,
                action='buy',
                price=price
            )"""
            self.buyOrder(cryptopair)
        elif basecoin_or_quotecoin == 'basecoin':

            # BNBBTC from bnb to btc you sell
            """self._sellOrder(
                quantity=quantity,
                coin_for_order=coin_for_order,
                action='sell',
                price=price
            )"""
            self.sellOrder(cryptopair)

    def _buyOrder(self, **kwargs):
        """Virtual buy"""
        # modify 'virtualbalance' table
        # create new balance for the new crypto
        self.database.requestDB(
            f"UPDATE virtualbalance SET Balance = {kwargs['quantity']} where shortname = {kwargs['coin_for_order']} ")
        # delete balance on crypto i use to hold
        self.database.requestDB(f"UPDATE virtualbalance SET Balance = {0} where shortname = {self.coin} ")
        # modify 'virtualtrade' table
        self.database.requestDB(
            f"insert into virtualtrade(basecoin ,quotecoin,ordertype,quantity,tradetime) values(f'"
            f"{kwargs['coin_for_order']}','{self.coin}','{kwargs['action']}',"
            f"'{kwargs['quantity']}','{str(datetime.datetime.now())}') ")
        # swap crypto
        self.coin = kwargs["coin_for_order"]

    def _sellOrder(self, **kwargs):
        """Virtual sell"""
        # modify 'virtualbalance' table
        # create new balance for the new crypto
        self.database.requestDB(
            f"UPDATE virtualbalance SET Balance = {kwargs['quantity']} where shortname = {kwargs['coin_for_order']} ")
        # delete balance on crypto i use to hold
        self.database.requestDB(f"UPDATE virtualbalance SET Balance = {0} where shortname = {self.coin} ")
        # modify 'virtualtrade' table
        self.database.requestDB(
            f"insert into virtualtrade(basecoin ,quotecoin,ordertype,quantity,tradetime) values(f'"
            f"{kwargs['coin_for_order']}','{self.coin}','{kwargs['action']}',"
            f"'{kwargs['quantity']}','{str(datetime.datetime.now())}') ")
        # swap crypto
        self.coin = kwargs["coin_for_order"]

    def _getcoinsrelated(self, coin: str):
        # return all coins related quotecoins or basecoin

        infos = self.database.selectDB("select quotecoin from relationalcoin where basecoin ='" + coin + "'")
        basecoins = [info[0] for info in infos]

        infos = self.database.selectDB("select basecoin from relationalcoin where quotecoin ='" + coin + "'")
        quotecoins = [info[0] for info in infos]

        return {'quotecoins': quotecoins, 'basecoins': basecoins}

    def _get_crypto_pair_related(self, coin: str = None):
        cryptoinfo = self.database.selectDB(
            "select cryptopair from relationalcoin where basecoin ='" + coin + "'or quotecoin='" + coin + "'")

        cryptoinfo = [crypto[0] for crypto in cryptoinfo]
        return list(dict.fromkeys(cryptoinfo))

    def _getBasecoin_cryptopair(self, cryptopair):
        # sqlcon = mysqlDB()
        nn = self.database.selectDB(f"select  basecoin from relationalcoin where cryptopair='" + cryptopair + "'")
        if isinstance(nn, list) and len(nn) != 0:
            return nn[0][0]
        elif len(nn) == 0:
            return 'result not found'

    def _getQuotecoin_cryptopair(self, cryptopair):
        # sqlcon = mysqlDB()
        nn = self.database.selectDB(f"select  quotecoin from relationalcoin where cryptopair='" + cryptopair + "'")
        if isinstance(nn, list) and len(nn) != 0:
            return nn[0][0]
        elif len(nn) == 0:
            return 'result not found'

    @staticmethod
    def _basecoin_or_quotecoin(cryptopair: str = None, coin: str = None):
        if cryptopair.startswith(coin):

            return 'basecoin'
        elif cryptopair.endswith(coin):

            return 'quotecoin'

    def _get_many_klines(self, cryptopairs: list) -> dict[str, str]:
        """kline response:
            [
              [
                1499040000000,      // Open time
                "0.01634790",       // Open
                "0.80000000",       // High
                "0.01575800",       // Low
                "0.01577100",       // Close
                "148976.11427815",  // Volume
                1499644799999,      // Close time
                "2434.19055334",    // Quote asset volume
                308,                // Number of trades
                "1756.87402397",    // Taker buy base asset volume
                "28.46694368",      // Taker buy quote asset volume
                "17928899.62484339" // Ignore.
              ]
            ]
        """
        kline_uri = "https://api.binance.com/api/v3/klines"
        data = {
            # "symbol":'BNBBTC',
            "interval": self.timeframe,
            # "startTime": '1 day ago'
            # "endTime"
            "limit": 100
        }
        cryptoklines = {}
        for cryptopair in cryptopairs:
            data['symbol'] = cryptopair
            klines_list = requests.get(url=kline_uri, params=data).json()

            for kline in klines_list:
                kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)
                kline[6] = datetime.datetime.fromtimestamp(kline[6] / 1e3)
            klines = pd.DataFrame(klines_list)  # changer en dataframe
            # supprimer les collonnes qui ne sont pas necessaires
            klines.drop(columns=[6, 7, 8, 9, 10, 11], inplace=True)

            klines.columns = ['date', 'open', 'high', 'low',
                              'close', 'volume']  # renommer les colonnes

            cryptoklines = {cryptopair: klines}

        return cryptoklines

    def _crypto_study(self, klines: dict) -> dict[str, str]:
        """study cryptopair with it's klines"""
        cryptopairs = list(klines.keys())

        results = {}  # {'BNBBTC':'buy'}
        for cryptopair in cryptopairs:
            decision = self.Decision(klines[cryptopair])
            results[cryptopair] = decision
        return results

    def _cleaner(self, study: dict) -> dict[str, str]:
        cryptopairs = list(study.keys())

        results = {}
        for cryptopair in cryptopairs:
            # when i possess ETH
            # ETHBTC must be a 'sell'
            if (cryptopair.startswith(self.coin) and study[cryptopair] == 'sell') or (
                    cryptopair.endswith(self.coin) and study[cryptopair] == 'buy'
            ):
                results[cryptopair] = study[cryptopair]
        return results

    def run(self):

        while True:
            # get crypto related
            cryptopair_related: list = self._get_crypto_pair_related(coin=self.coin)

            # get all klines for each cryptopair
            klines: dict = self._get_many_klines(cryptopair_related)

            # get cryptopair with they study results
            cryptopairs_study_unclean = self._crypto_study(klines)

            # clean the cryptopairs_study dict so we only have
            # possible trades
            cryptopairs_study = self._cleaner(cryptopairs_study_unclean)

            if len(cryptopairs_study) == 0:
                time.sleep(int(self.timeframe.replace('m', '')) * 5)
            else:
                cryptopairs = list(cryptopairs_study.keys())
                # choose a crypto pair
                cryptopair = cryptopairs[random.randint(0, len(cryptopairs) - 1)]

                # pass order (the quantity is calculated in passing order)
                self.passOrder(cryptopair)

                # set new coin
                self.coin = cryptopair.replace(self.coin, '')

                time.sleep(int(self.timeframe.replace('m', '')) * 5)


    def status(self):
        """send status to to the server """
        pass







class Order:
    """Binance Order Class"""
    def __init__(self, orderDetails: dict):
        self.database = mysqlDB()
        assert isinstance(orderDetails, dict)

        self.orderId = orderDetails['orderId']
        self.symbol = orderDetails['symbol']
        self.type = orderDetails['type']
        self.side = orderDetails['side']
        self.transactTime = orderDetails['transactTime']
        self.status = orderDetails['status']
        self.executedQty = orderDetails['executedQty']

    def save(self):
        self.database.requestDB(f"insert into orders(orderId,symbol,type,side,transactTime,status,executedQty) values("
                                f"{self.orderId},{self.symbol},{self.type},{self.side},{self.transactTime},"
                                f"{self.status},{self.executedQty})")

    @staticmethod
    def get_all_orders():
        database = mysqlDB()
        results = database.selectDB(f"select * from orders")

        return results
