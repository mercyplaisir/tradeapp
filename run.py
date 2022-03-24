
import time
import random


from exchanges import BinanceClient
from base import Coin,CryptoPair,Order
from common.tools import cout,interval_to_milliseconds,send_data

sleep_time = '5m'

with BinanceClient(testnet=True) as client:
    coin = Coin('USDT')
    cout("run method")
    while True:
        # get crypto related
        cryptopair_related: list = coin.get_cryptopair_related()

        # get all decision for each cryptopair
        cryptopair_decision = CryptoPair.study(cryptopair_related)
        if len(cryptopair_decision) == 0:
            cout(">>> No opportunity for trading")
            # cout(cryptopair_decision_uncleaned)

            sleep_time_sec = interval_to_milliseconds(sleep_time) / 1000
            time.sleep(sleep_time_sec)
        else:
            cryptopairs = list(cryptopair_decision.items())  # [("BNB""buy"))]
            cryptopairs_size = len(cryptopairs) - 1
            cout("opportunities on: ", cryptopair_decision)

            cryptopair_study: tuple[CryptoPair, str] = cryptopairs[
                random.randint(0, cryptopairs_size)
            ]  # ("BNB",("buy",3))
            cout(cryptopair_study)

            # time.sleep(20)

            choosen_cryptopair,order_type = cryptopair_study
            # pass order (the quantity is calculated in passing order)
            order_details = client.pass_order(
                cryptopair_name=choosen_cryptopair, order_type=order_type
            )
            order = Order(**order_details)
            new_coin = CryptoPair.replace(coin)

            

            # track order
            order.track_order()
            send_data(
                "post",
                "/all",
                profit=order.profit,
                coin=new_coin,
                cryptopair=choosen_cryptopair,
            )
