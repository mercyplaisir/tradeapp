from typing import Dict
from typing import List
import asyncio

import ccxt

from tradeapp.models.cryptopair import Crypto, CryptoPair
from tradeapp.exchanges.exchanges import binance
from tradeapp.strategy.strategy import follow_trend_strat_spot

from tradeapp.tools import fetch_cryptopairs
from tradeapp.tools import Signal

from tradeapp.telegram import Telegram

from dotenv import load_dotenv 

load_dotenv()  # take environment variables from .env.

async def main():
    #profit
    PROFIT = 2
    CRYPTO_I_OWN = 'USDT'
    #implement exchange
    exchange:ccxt.Exchange = binance()
    
    # get related crypto to the one i one
    mycrypto =  await Crypto( CRYPTO_I_OWN,exchange)
    crypto_related = await mycrypto.get_cryptopair_related()
    # create cryptopairs objects 
    cryptos = await asyncio.gather(*[CryptoPair(exchange,sym) for sym in crypto_related])

    # put them on strategy
    awaitables = [asyncio.create_task(follow_trend_strat_spot(crypto)
    ) for crypto in cryptos[:20]]
    cryptos_signal = await asyncio.gather(*awaitables)
    # # select the one with buy signal
    # cryptos_with_buy = [crypto for crypto in cryptos_signal if cryptos_signal[crypto]==Signal.BUY]
    
    # send them to telegram
    print(cryptos_signal)
    # print({cryptos[i]:cryptos_signal[i]} for i in range(len(cryptos)))
    # Telegram.send_message("\n".join(crypto_related))
        # Telegram.send_image(crypto.generate_image())
    await exchange.close()
if __name__ == '__main__':
    asyncio.run(main())