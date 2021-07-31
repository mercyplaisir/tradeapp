import sys
import time

from btalib.indicators.stochastic import stochastic


from BinanceApi import Binance
sys.path.append("..")
from Indicators.study import Study

#=========initialize binance connection==========
client = Binance()
#================================================

while True:

    while True:
        #============study price===========
        crypto = client.cryptoToTrade()

        study= Study(crypto)

        decision = study.Decision()

        if decision == 'buy':
            client.buyOrder(coin_to_trade=crypto)
            client.lastOrderWasBuy = True
            break
        elif decision == 'sell' and client.lastOrderWasBuy:
            client.sellOrder(crypto)
            client.lastOrderWasBuy = False
            break
        elif decision == 'wait':
            pass

    while True:
        decisionAfter = study.Decision()
        if decisionAfter == 'buy' and not client.lastOrderWasBuy:
            client.buyOrder(coin_to_trade=crypto)
            client.lastOrderWasBuy = True
            break
        elif decisionAfter == 'sell' and client.lastOrderWasBuy:
            client.sellOrder(crypto)
            client.lastOrderWasBuy = False
            break
        elif decisionAfter == 'wait':
            pass





