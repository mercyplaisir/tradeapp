import datetime
from websocket import create_connection
import json
import time
import pandas as pd

from tools.logs import logger_wrapper,create_logger
from exchanges.binanceFuture import klines_future

import threading

rsi_period = 25


def get_rsi(df:pd.DataFrame, lookback):
    
    close = df.copy(deep=True)['close']
    # print(close)
    ret = close.diff()
    up = []
    down = []
    for i in range(len(ret)):
        if ret[i] < 0:
            up.append(0)
            down.append(ret[i])
        else:
            up.append(ret[i])
            down.append(0)
    up_series = pd.Series(up)
    down_series = pd.Series(down).abs()
    up_ewm = up_series.ewm(com = lookback - 1, adjust = False).mean()
    down_ewm = down_series.ewm(com = lookback - 1, adjust = False).mean()
    rs = up_ewm/down_ewm
    rsi = 100 - (100 / (1 + rs))
    rsi_df = pd.Series(rsi,name='rsi')
    
    rsi_df = pd.DataFrame(rsi).rename(columns = {0:'rsi'}).set_index(close.index)
    # rsi_df = rsi_df.dropna()
    # rsi_df.to_csv('rsi.csv',mode='x')
    # print(rsi_df)
    # return rsi_df[3:]
    column_name='rsi'
    try:
        df.drop(['level_0','rsi'],axis=1,inplace=True)
    except KeyError:
        pass
    df.insert(7,"rsi",rsi_df,True)
    
    return df



def append_df(df:pd.DataFrame,data:dict,deep:bool=True):
    """"""
    
    # print(data)
    df2 = pd.DataFrame([data])
    # df_copy.append(data,ignore_index=True)
    df3 = pd.concat([df,df2])
    df3.reset_index(inplace=True)
    # df3.to_csv('d3.csv',mode='w+')
    return df3

@logger_wrapper(__name__,"track rsi")
def track(pair:str,timeframe:str='15m') -> dict:
    base_url = "wss://fstream.binance.com:443/ws/"

    # kline
    # https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-streams

    # <symbol>@kline_<interval>
    stream_name = f"{pair.lower()}" + f"@kline_{timeframe}"

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

    klines = klines_future(pair,timeframe)
    while True:
        # print("redo")
        
        rs =  ws.recv()

        result = json.loads(rs)

        # print(result)
        try : 
            (_,t_o),(_,t_c),(_,_),(_,_),(_,_),(_,_),(_,o),(_,c),(_,h),(_,l),(_,v),(_,_),(_,k),(_,_),(_,_),(_,_),(_,_) = result['k'].items()
            # print('done')
            # break
            o,c,h,l,v = float(o),float(c),float(h),float(l),float(v)
            
            data = {"open":o,"high":h,"low":l,"close":c}
            if k : #if candle close
                klines = append_df(klines,data) 
                df = get_rsi(klines,rsi_period)
                # print(df)
                df.to_csv(f'data_{pair}.csv',mode='w+')
                print(df.iloc[[-1]].get(['close','rsi']))
        except KeyError as e:
            print(f"{e},retry ...")
            time.sleep(1)

def run_wthread():
    pairs = ['ETHUSDT','TRXUSDT','BTCUSDT']
    timeframe= '1m'
    threads:list[threading.Thread] =[]
    for pair in pairs:
        t = threading.Thread(target=track,kwargs={'pair':pair,'timeframe':timeframe})
        t.daemon =True
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def main():

    run_wthread()
    # pair = 'TRXUSDT'
    # timeframe= '1m'
    # track(pair,timeframe)

if __name__=='__main__':
    main()