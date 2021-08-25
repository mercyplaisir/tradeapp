
import time
import sys
sys.path.append(sys.path[0]+'/../..')


from src.controller.BinanceApi import Binance
from src.model.Indicators.study import Study

#=========initialize binance connection==========
client = Binance()

study= Study(crypto)
#================================================


while True:

    while True:
        #============study price===========
        crypto = client.cryptoToTrade()

        decision = study.Decision()
        
        if decision == 'buy' and not lastOrderWasBuy :
            client.buyOrder(coin_to_trade=crypto)
            break
         elif decision == 'sell' and client.lastOrderWasBuy:
             client.sellOrder(crypto)
             client.lastOrderWasBuy = False
             break
        elif decision == 'wait':
            pass
        client.PLcalculator()
    time.sleep(120)






