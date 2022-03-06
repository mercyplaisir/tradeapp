from exchange.binanceApi import BinanceClient
from base import CryptoPair
#run file

with BinanceClient() as client:
    cr = CryptoPair('NEARUSDT')
    client._pass_order(cr,'sell')
