import json

from src.api.virtualbinance import VirtualClient
from src.api.sensitive import BINANCE_PRIVATE_KEY,BINANCE_PUBLIC_KEY


#init client
client = VirtualClient(publickey=BINANCE_PUBLIC_KEY,
                        secretkey=BINANCE_PRIVATE_KEY)

#coin in possession
client.coin = 'BTC'

while True:
    pass
