import csv
import json
import time
import datetime
import math





def percent_calculator(x:float,y:str):
    z=x+((x*y)/100)
    return z
def percent_change(original_number:float,new_number:float):
    z = ((new_number-original_number)/original_number)*100
    return z



i=0.0003742
x = percent_calculator(i,-2)

#y=percent_change(i,)

y = percent_change(i,0.0003781)
   


print(x)
print(y)


v= datetime.datetime.timestamp(datetime.datetime.now())

print(type(v))




from binance.websockets import BinanceSocketManager
from twisted.internet import reactor

# init and start the WebSocket
bsm = BinanceSocketManager(client)
conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', btc_trade_history)
bsm.start()


# stop websocket
bsm.stop_socket(conn_key)

# properly terminate WebSocket
reactor.stop()

#print(y)

