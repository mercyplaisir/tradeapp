from src.api.binanceApi import Binance

# =========initialize binance connection==========
client = Binance()
client.client.order_market_buy()
client.run()
