from websocket import create_connection
import json
import time

from tools.logs import logger_wrapper,create_logger



@logger_wrapper(__name__,"track for a tp/sl")
def track(pair:str,tp:float,sl:float,buy:float=True):
    base_url = "wss://fstream.binance.com:443/ws/"

    # last price trought continious kline
    # https://binance-docs.github.io/apidocs/futures/en/#continuous-contract-kline-candlestick-streams

    #<pair>_<contractType>@continuousKline_<interval>
    stream_name = f"{pair}" + "_" + "perpetual" + "@continuousKline_5m"

    subscribe_params = {
    "method": "SUBSCRIBE",
    "params":
    [
    stream_name
    ],
    "id": 2
    }


    ws = create_connection(base_url + stream_name)
    print("connection created")

    #subscribe
    ws.send(json.dumps(subscribe_params))
    print("subscribed")

    while True:
        # print("redo")
        rs =  ws.recv()
        result = json.loads(rs)
        # print(result)
        try : 
            (_,_),(_,_),(_,_),(_,_),(_,_),(_,o),(_,c),(_,h),(_,l),(_,v),(_,_),(_,_),(_,_),(_,_),(_,_),(_,_) = result['k'].items()
            c = float(c)

            # print(f"{i} Received {c}")
            print(c)
            if (buy and c>=tp) or (not buy and c<=tp): 
                ws.close()
                return 'Profit'
            elif (buy and c<=sl) or (not buy and c>=sl):
                ws.close()
                return 'Loss'
            time.sleep(0.3)
        
        except KeyError as e:
            print(f"{e},retry ...")
            time.sleep(0.2)