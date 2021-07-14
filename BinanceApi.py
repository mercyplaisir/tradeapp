import datetime
import json

import pandas as pd
import websocket
from binance.client import Client
from binance.enums import *
from binance.exceptions import *

from tools import Tool, FILESTORAGE

"""
functions in  this file:
                        -margin_buy_order
                        -margin_sell_order
                        - margin_balance_of
                        - order _quantity_of
                        - get_klines
                        
                        - coin_for_trade
                        - get_coin_price
                        - coinPriceChange

                        - set_list_of_crypto
                        - get_list_of_crypto
                        - connect





"""




CRYPTOLIST = 'cryptoliste.json'

APIKEYPATH = '.files/apikey.json'

class Binance:
    baseCoin = 'BTC'




    def __init__(self):
        try:
            self.apikeys = Tool.read_json(APIKEYPATH)
            self.apiPublicKey = self.apikeys["public key"]
            self.apiSecretKey = self.apikeys["secret key"]

            # self.liste_of_crypto = self.set_list_of_crypto()
            # you = {"id": self.apikeys, "basecoin": self.baseCoin}

            self.connect()
            # self.set_list_of_crypto()
        except:
            print("erreur de connexion")

    def connect(self):
        while True:
            try:
                self.client = Client(self.apiPublicKey, self.apiSecretKey)

                break
            except:
                print("erreur de connexion\nretry...")


    # placer un ordre d'achat
    def margin_buy_order(self, coin_to_trade: str, order_quantity: float):
        """A margin buy order"""
        self.client.create_margin_order(
            symbol=coin_to_trade, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=order_quantity)

    # placer un ordre de vente
    def margin_sell_order(self, coin_to_trade: str, order_quantity: float):
        """ A margin sell order """
        self.client.create_margin_order(
            symbol=coin_to_trade, side=SIDE_SELL, type=ORDER_TYPE_MARKET, quantity=order_quantity)

    def margin_balance_of(self, coin: str)->float:
        """
        *parameters:- coin. ex:BTC,ETH
        *return margin balance
        """

        info = self.client.get_margin_account()
        for i in info['userAssets']:
            if coin == 'BTC':
                if i['asset'] == coin:
                    balance = float(str(i['free'])[:7])
                    return balance
            elif i['asset'] == coin:
                balance = (float(str(i['free'])[:5]))
                return balance

    def order_quantity_of(self, balance: float, coin: str)-> float:
        """
        parameters: -balance. ex: 20$
                    -coin. ex: BTC,ETH

        return quantity(float)
        """
        # il determine la quantite a utiliser pour placer un ordre en analysant so prix

        coinInfo_USD = Binance.coinPriceChange(coin + 'USDT')
        coinInfo_BTC = Binance.coinPriceChange(coin + self.baseCoin)

        coin_price_usd = coinInfo_USD['price']
        coin_price = coinInfo_BTC['price']
        if coin == 'ETH':
            q = balance / coin_price
            q = float(str(q)[:5])
            return q
        if coin != 'ETH':
            if coin_price_usd >= 5000:  # si le prix est entre 50 et 700
                q = balance / coin_price
                q = float(str(q)[:6])
                return q

            if 50 <= coin_price_usd:  # si le prix est entre 50 et 700
                q = balance / coin_price
                q = float(str(q)[:5])
                return q

            elif 16 <= coin_price_usd <= 49:  # si le prix est entre 16 et 49
                q = balance / coin_price
                q = float(str(q)[:3])
                return q

            elif 0.18 <= coin_price_usd <= 15:  # si le prix est entre 0 et 15
                q = balance / coin_price
                q = float(str(q)[:2])
                return q
            elif coin_price < 0.18:
                q = balance / coin_price
                q = float(str(q)[:3])
                return q
        # q c'est la quqntite

    def get_klines(self, coin_to_trade: str = "BNBBTC", timeframe: str = "15m", interval: str = "2 days"):
        """
        Get the klines for the timeframe given and in interval given.
        timeframe ex:1m,5m,15m,1h,2h,6h,8h,12h,1d,1M,1w,3d

        Default timeframe = 15m
        Default interval = 2 days


        colums=["open_time","open_price","close_price","SMA_30","SMA_50","SMA_20","upper_band","lower_band"]

        stores the klines in a csv file
        """
        print(1)
        try:
            klines_list = self.client.get_historical_klines(
                coin_to_trade, timeframe, f"{interval} ago UTC")
            print(2)
            # changer timestamp en date
            for kline in klines_list:
                kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)

            klines = pd.DataFrame(klines_list)  # changer en dataframe
            # supprimer les collonnes qui ne sont pas necessaires
            klines.drop(columns=[2, 3, 5, 6, 7, 8, 9, 10, 11], inplace=True)

            klines.columns = ['open_time', 'open_price',
                              'close_price']  # renommer les colonnes

            # trier les indexes pour que 0 correspondents avec maintenant
            klines.sort_index(ascending=False, inplace=True)

            # refaire les index
            klines.reset_index(inplace=True)

            # supprimer un colonnes pas important
            klines.drop(columns=['index', 'rstd'], inplace=True)

            print(3)
            klines.to_csv(f"{FILESTORAGE}/klines.csv")
            # return klines

        except BinanceOrderException:
            print(BinanceOrderException)
        except BinanceAPIException:
            print(BinanceAPIException)


    @staticmethod
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

                dict_result['k']['priceChange'] = Tool.percent_change(float(dict_result['k']['o']),
                                                                      float(dict_result['k']['c']))

                b = {'price': float(dict_result['k']['c']), 'priceChange': float(
                    dict_result['k']['priceChange'])}
                break
            except:
                pass

        return b


    traded_crypto = []  # liste des crypto deja trader
   
"""
    def coin_for_trade(self):
        \"""
        fonction pour recuperer le coin for trade et son price change
        \"""
        redo_search = True

        while redo_search:

            print('\n')
            print(str(datetime.datetime.now()).split(' ')[1])

            nonePickedUp = True

            cryptos = Tool.read_json(CRYPTOLIST)
            for n in range(0, (len(cryptos) - 1)):

                coin = cryptos[n]

                coin_to_trade = coin + self.baseCoin

                if coin not in Binance.traded_crypto:

                    print(coin_to_trade)

                    dictInfo = self.coinPriceChange(coin_to_trade)

                    coinPrice = dictInfo['price']
                    price_change = dictInfo['priceChange']

                    print(coin_to_trade, ' : ', dictInfo)
                    # up_trend = minute15_trend(coin_to_trade,coinPrice) #tendance pour 15min

                    price_5min = minute5_trend(
                        coin_to_trade, coinPrice)  # price trick

                    # if up_trend and price_5min :
                    if price_5min:
                        redo_search = False
                        nonePickedUp = False

                        print('got it')
                        b = {'coin to trade': coin_to_trade,
                             'price change': price_change}
                        break
                    print('-----------------------------')

                elif coin in Binance.traded_crypto:
                    continue

                # delete the list if traded the half of the list
                if len(Binance.traded_crypto) >= (len(cryptos) // 2):
                    Binance.traded_crypto.clear()

            if nonePickedUp:
                time.sleep(10)
        return b
"""
# -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-----_-_-_-_-_-_-_-_-_-_-
