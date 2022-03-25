
import time
import random
from typing import List, Union


from exchanges import BinanceClient
from base import Coin,CryptoPair,Order
from common.tools import cout,interval_to_milliseconds,send_data

sleep_time = '5m'

def main(client: BinanceClient,data:Union[List[CryptoPair],CryptoPair]):
    """"""
    # get all decision for each cryptopair
    cryptopair:CryptoPair = CryptoPair.study(data)
    if cryptopair is None:
        cout(">>> No opportunity for trading")
        cout(data)
        sleep_time_sec = interval_to_milliseconds(sleep_time) / 1000
        time.sleep(sleep_time_sec)

        return
    cout("opportunities on: ", cryptopair)
    order_details = client.pass_order(
                cryptopair_name=cryptopair, order_type=cryptopair.decision
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
    cryptopair=cryptopair,
    )

crypto = 'BTCUSDT'

with BinanceClient(testnet=True) as client:
    coin = Coin('USDT')
    cout("run method")
    while True:
        # get crypto related
        cryptopair_related: list = coin.get_cryptopair_related()
        crypto_for_use = CryptoPair(crypto)

        main(client,crypto_for_use)
