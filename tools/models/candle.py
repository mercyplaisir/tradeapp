from enum import Enum,auto
from websocket import create_connection
import json

from tools.models.timeframe import Timeframe

from tools.logs import logger_wrapper
class Candle(Enum):
    RED = auto()
    GREEN = auto()

    def __str__(self) -> str:
        return f'{self.name}'

logger_wrapper(__name__,"getting th candle")
def get_candle(pair:str,timeframe):
    base_url = "wss://fstream.binance.com:443/ws/"

    # last price trought continious kline
    # https://binance-docs.github.io/apidocs/futures/en/#continuous-contract-kline-candlestick-streams

    #<pair>_<contractType>@continuousKline_<interval>
    stream_name = f"{pair.lower()}" + "_" + "perpetual" + f"@continuousKline_{timeframe}"

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
    rs =  ws.recv()
    result = json.loads(rs)
    (_,_),(_,_),(_,_),(_,_),(_,_),(_,o),(_,c),(_,h),(_,l),(_,v),(_,_),(_,_),(_,_),(_,_),(_,_),(_,_) = result['k'].items()
    c = float(c) # last price
    o = float(o) # open price

    if o>c:
        return Candle.RED
    elif c>o:
        return Candle.GREEN
    
