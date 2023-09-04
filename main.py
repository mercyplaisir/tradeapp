
from tradeapp.exchanges.binancef.binanceFuture import (
    binance_future,
    get_bal_of,
    market_buy_order,
)

from tools.telegram import Telegram


from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

#crypto to trade
crypto = 'BTCUSDT'
# exchange
ex = binance_future()
# get klines
# get res and support
# select points near the price to work on
# track
# if touch the points get the candle type
# place an order against the candle


leverage = 10
balance = get_bal_of(ex=ex, crypto="USDT")
crypto_price = ex.fetch_ticker("BTCUSDT")["last"]
market_buy_order(
    exchange= ex,
    symbol = 'BTCUSDT',
    quantity = (balance*leverage)/crypto_price,
    recvWindow = 5000,
)
# market_sell_order(
#     exchange= ex,
#     symbol = 'BTCUSDT',
#     quantity = (balance*leverage)/crypto_price,
#     recvWindow = 5000,
#     isolated = True,
# )
print(balance)

# print(ex.fetch_ticker('BTCUSDT')['last'])

Telegram.send_message("hello")
# async def main():
#     # #profit
#     # PROFIT = 2
#     # CRYPTO_I_OWN = 'USDT'
#     # #implement exchange
#     # exchange:ccxt.Exchange = binance()

#     # # get related crypto to the one i one
#     # mycrypto =  await Crypto( CRYPTO_I_OWN,exchange)
#     # crypto_related = await mycrypto.get_cryptopair_related()
#     # # create cryptopairs objects
#     # cryptos = await asyncio.gather(*[CryptoPair(exchange,sym) for sym in crypto_related])

#     # # put them on strategy
#     # awaitables = [asyncio.create_task(follow_trend_strat_spot(crypto)
#     # ) for crypto in cryptos[:20]]
#     # cryptos_signal = await asyncio.gather(*awaitables)

#     # await exchange.close()
#     # -------------------------------------
#     ex = await binance_future()
#     balance =  ex.fetch_balance()
#     print(balance['total'])
#     Telegram.send_message(balance['total'])
# if __name__ == '__main__':
#     asyncio.run(main())