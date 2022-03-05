from exchange.binanceApi import BinanceClient

#run file

with BinanceClient() as client:
    print(client.coin)
