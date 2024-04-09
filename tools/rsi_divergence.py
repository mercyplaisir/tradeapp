from exchanges.binanceFuture import klines_future
from indicator.rsi import get_rsi

def main():
    pair = 'ethusdt'
    timeframe = '5m'
    klines_5m = klines_future(pair,timeframe)



if __name__ == 'main':
    main()