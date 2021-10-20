
import time
import os

import websockets

from src.api.binanceApi import Binance
from src.model.Indicators.study import Study

#=========initialize binance connection==========
client = Binance()

#================================================
while True:
    #============study price===========
    crypto = client.cryptoToTrade()
    study= Study(crypto)

    decision = study.Decision()

    if decision == 'buy' and not client.lastOrderWasBuy :
        client.buyOrder(coin_to_trade=crypto)

    elif decision == 'sell' and client.lastOrderWasBuy :
        client.sellOrder(crypto)
        client.lastOrderWasBuy = False
        
    elif decision == 'wait':
        pass
    #client.PLcalculator()

    time.sleep(120)



# import sys
# import subprocess
# xx = subprocess.run(["cat","/home/mercy/Github/tradeapp/README.md"],
#                     capture_output=True,
#                     text=True)
# #xx = subprocess.run(["ls"],capture_output=True,text=True)
# print(xx.stdout)









