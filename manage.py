from exchange.binanceApi import BinanceClient
from base import CryptoPair
#run file

with BinanceClient() as client:
    client.run()
