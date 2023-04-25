import ccxt
import time

from tradeapp.protocols import Strategy
# Define the exchange and trading parameters
exchange = ccxt.kraken()
symbol = 'BTC/USD'
spread = 0.05
amount = 1

# Connect to the exchange and retrieve the order book
exchange.load_markets()
orderbook = exchange.fetch_order_book(symbol)

# Calculate the bid and ask prices
bid = orderbook['bids'][0][0] if len(orderbook['bids']) > 0 else None
ask = orderbook['asks'][0][0] if len(orderbook['asks']) > 0 else None
spread_decimal = spread / 100
if bid and ask:
    mid_price = (bid + ask) / 2
    buy_price = mid_price - mid_price * spread_decimal
    sell_price = mid_price + mid_price * spread_decimal

    # Place limit orders
    buy_order = exchange.create_limit_buy_order(symbol, amount, buy_price)
    sell_order = exchange.create_limit_sell_order(symbol, amount, sell_price)

    print('Buy order placed:', buy_order)
    print('Sell order placed:', sell_order)

# Wait for the order to fill
time.sleep(10)

# Cancel the open orders
exchange.cancel_order(buy_order['id'], symbol)
exchange.cancel_order(sell_order['id'], symbol)

class Market_MAker(Strategy):
    def __init__(self) -> None:
        pass