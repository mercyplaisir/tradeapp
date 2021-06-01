import pandas as pd
from binance.client import Client
from binance.enums import *
import datetime
import time
import json
import websocket




from tools import Tool



"""
functions in  this file:
                        -margin_buy_order
                        -margin_sell_order
                        - margin_balance_of
                        - order _quantity_of
                        - get_klines
                        - price_study
                        - minute15_trend
                        - minute5_trend
                        - coin_for_trade
                        - get_coin_price
                        - coinPriceChange




"""


class Binance:

    cryptoListe_filepath = './cryptoliste.json'

    @classmethod
    def set_list_of_crypto(cls):
        taille = Tool.input_int("entrer la taille du tableau")
        for i in range(taille):
            Binance.list_of_crypto[i] = Tool.input_str("entrer le crypto " +i+": ")
        

        print(Binance.list_of_crypto)



    def __init__(self):
        self.apikeys = Tool.read_json("./files/apikey.json")
        self.apiPublicKey = self.apikeys["public key"]
        self.apiSecretKey = self.apikeys["secret key"]
        self.baseCoin = 'BTC'

        self.connect()

    def connect(self):
        while True:
            try:
                self.client = Client(self.apiPublicKey, self.apiSecretKey)
                break
            except:
                pass


    def get_list_of_crypto(self):
        return Binance.list_of_crypto


    #placer un ordre d'achat
    def margin_buy_order(self, coin_to_trade: str, order_quantity: float):
        """A margin buy order"""
        self.client.create_margin_order(
            symbol=coin_to_trade, side=SIDE_BUY, type=ORDER_TYPE_MARKET, quantity=order_quantity)


    #placer un ordre de vente
    def margin_sell_order(self,coin_to_trade: str, order_quantity: float):
        """ A margin sell order """
        self.client.create_margin_order(
            symbol=coin_to_trade, side=SIDE_SELL, type=ORDER_TYPE_MARKET, quantity=order_quantity)


    #ecrire dans un fichier json




    def margin_balance_of(self, coin: str):
        """
        recuperer la balance d'un crypto
        """

        info = self.client.get_margin_account()
        for i in info['userAssets']:
            if coin == 'BTC':
                if i['asset'] == coin:
                    balance = float(str(i['free'])[:7])

            elif i['asset'] == coin:
                balance = (float(str(i['free'])[:5]))
        return balance


    def order_quantity_of(self, balance: float, coin: str):
        """
        permet d'avoir une quantite pour placer l'ordre
        """
        #il determine la quantite a utiliser pour placer un ordre en analysant so prix

        coin_price_usd = self.get_coin_price(coin + 'USDT')
        coin_price = self.get_coin_price(coin + self.baseCoin)
        if coin == 'ETH':
            q = balance / coin_price
            q = float(str(q)[:5])
        if coin != 'ETH':
            if coin_price_usd >= 5000:  # si le prix est entre 50 et 700
                q = balance / coin_price
                q = float(str(q)[:6])

            if 50 <= coin_price_usd:  # si le prix est entre 50 et 700
                q = balance / coin_price
                q = float(str(q)[:5])

            elif 16 <= coin_price_usd <= 49:  # si le prix est entre 16 et 49
                q = balance / coin_price
                q = float(str(q)[:3])

            elif 0.18 <= coin_price_usd <= 15:  # si le prix est entre 0 et 15
                q = balance / coin_price
                q = float(str(q)[:2])
            elif coin_price < 0.18:
                q = balance / coin_price
                q = float(str(q)[:3])
        return q  # q c'est la quqntite


    def get_klines(self, coin_to_trade: str, timeframe: str, interval: str):
        """
        Get the klines for the timeframe given and in interval given.
        timeframe ex:1m,5m,15m,1h,2h,6h,8h,12h,1d,1M,1w,3d

        """

        try:
            klines_list = self.client.get_historical_klines(
                coin_to_trade, timeframe, f"{interval} ago UTC")

            #changer timestamp en date
            for kline in klines_list:
                kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)

            klines = pd.DataFrame(klines_list)  # changer en dataframe
            # supprimer les collonnes qui ne sont pas necessaires
            klines.drop(columns=[2, 3, 5, 6, 7, 8, 9, 10, 11], inplace=True)

            klines.columns = ['open_time', 'open_price',
                            'close_price']  # renommer les colonnes

            #creer un SMA_30
            klines['SMA_30'] = klines.iloc[:, 1].rolling(window=15).mean()

            #creer un SMA50
            klines['SMA_50'] = klines.iloc[:, 1].rolling(window=30).mean()

            #calculate sma20
            klines['SMA_20'] = klines.iloc[:, 1].rolling(window=20).mean()

            # calculate the standar deviation
            klines['rstd'] = klines.iloc[:, 1].rolling(window=20).std()

            klines['upper_band'] = klines['SMA_20'] + 2 * klines['rstd']
            #klines['upper_band'] = upper_band.rename(columns={symbol: 'upper'})
            klines['lower_band'] = klines['SMA_20'] - 2 * klines['rstd']
            #klines['lower_band'] = lower_band.rename(columns={symbol: 'lower'})

            #klines = klines.join(upper_band).join(lower_band)

            #trier les indexes pour que 0 correspondents avec maintenant
            klines.sort_index(ascending=False, inplace=True)

            #refaire les index
            klines.reset_index(inplace=True)

            #supprimer un colonnes pas important
            klines.drop(columns=['index', 'rstd'], inplace=True)

            return klines

        except:
            print('no klines')

        return klines


    def price_study(coin_to_trade: str, klines: pd.DataFrame, advanced: bool, coinPrice: float):
        """
        study made on klines(dataframe)
        """
        if not advanced:

            a = []
            for n in range(0, 3):
                if float(klines.loc[n]['close_price']) > float(klines.loc[n]['SMA_20']) and float(klines.loc[n]['open_price']) > float(klines.loc[n]['SMA_20']):
                    y = True
                    a.append(y)
                else:
                    y = False
                    a.append(y)
            j = 0
            for i in a:
                if i == True:
                    j += 1
                else:
                    break
            if j == 4:
                bool_answer = True
            else:
                bool_answer = False
    #-------------------------------------------------------------------------------

        elif advanced:
            #SMA20                      close price du 1er bougie arriere    openprice du 2eme bougie arriere     openprice du 1er bougie arriere     close price du 2eme bougie arriere
            if float(klines.loc[0]['SMA_20']) > float(klines.loc[1]['close_price']) > float(klines.loc[2]['open_price']) > float(klines.loc[1]['open_price']) >= float(klines.loc[2]['close_price']):
                if float(klines.loc[2]['open_price']) <= Tool.percent_calculator(float(klines.loc[1]['close_price']), -2):
                    bool_answer = True
            else:
                bool_answer = False

        return bool_answer


    def minute15_trend(self,coin_to_trade: str, coinPrice: float):
        """
        tendance d'un crypto dans un timeframe de 1heure



        """
        up_trend = False
        try:
            klines = self.get_klines(coin_to_trade, '15m', '1 day')

            up_trend = self.price_study(coin_to_trade, klines, False, coinPrice)

            if up_trend:
                print('uptrend for 15min')
            else:
                print('no trend for 15min')

        except:
            up_trend = False

        return up_trend


    def minute5_trend(self,coin_to_trade: str, coinPrice: float):
        """
        tendance d'un crypto dans un timeframe de 1heure
        """

        up_trend = False
        try:
            klines = self.get_klines(coin_to_trade, '5m', '1day')

            up_trend = self.price_study(coin_to_trade, klines, True, coinPrice)

            if up_trend:
                print('uptrend for 5min')
            else:
                print('no trend for 5min')
        except:
            up_trend = False
        return up_trend


    traded_crypto = []  # liste des crypto deja trader


    def coin_for_trade(self):
        """
        fonction pour recuperer le coin for trade et son price change
        """
        redo_search = True

        while redo_search:

            print('\n')
            print(str(datetime.datetime.now()).split(' ')[1])

            nonePickedUp = True

            for n in range(0, (len(Binance.list_of_crypto)-1)):

                coin = Binance.list_of_crypto[n]

                coin_to_trade = coin + self.baseCoin

                if coin not in Binance.traded_crypto:

                    print(coin_to_trade)

                    dictInfo = self.coinPriceChange(coin_to_trade)

                    coinPrice = dictInfo['price']
                    price_change = dictInfo['priceChange']

                    print(coin_to_trade, ' : ', dictInfo)
                    #up_trend = minute15_trend(coin_to_trade,coinPrice) #tendance pour 15min

                    price_5min = self.minute5_trend(
                        coin_to_trade, coinPrice)  # price trick

                    #if up_trend and price_5min :
                    if price_5min:
                        redo_search = False
                        nonePickedUp = False

                        print('got it')
                        b = {'coin to trade': coin_to_trade,
                            'price change': price_change}
                        return b
                        break
                    print('-----------------------------')

                elif coin in Binance.traded_crypto:
                    continue

                # delete the list if traded the half of the list
                if len(Binance.traded_crypto) >= (len(Binance.list_of_crypto)//2):
                    Binance.traded_crypto.clear()

            if nonePickedUp:
                time.sleep(10)


    #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-----_-_-_-_-_-_-_-_-_-_-


    def coinPriceChange(self,coin_to_trade):
        """Return percent variation price of the the crypto in 24hour roll"""
        while True:
            try:
                sockete = f"wss://stream.binance.com:9443/ws/{coin_to_trade.lower()}@kline_1d"
                was = websocket.create_connection(sockete)

                json_result = was.recv()
                was.close()
                dict_result = json.loads(json_result)

                dict_result['k']['priceChange'] = Tool.percent_change(float(dict_result['k']['o']), float(dict_result['k']['c']))

                print('coinPriceChange')
                b = {'price': float(dict_result['k']['c']), 'priceChange': float(
                    dict_result['k']['priceChange'])}
                break
            except:
                pass

        return b

    
    def get_coin_price(self, coin_to_trade):
        while True:
            try:
                sockete = f"wss://stream.binance.com:9443/ws/{coin_to_trade.lower()}@kline_1m"
                was = websocket.create_connection(sockete)

                json_result = was.recv()
                was.close()
                dict_result = json.loads(json_result)

                print('coinPrice')
                break
            except:
                pass

        return float(dict_result['k']['c'])  # close price






