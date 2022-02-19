from src.platforms.binance import Binance

#run file
with Binance() as client:
    client.run()
