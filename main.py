from typing import Dict
from typing import List

import ccxt

from tradeapp.cryptopair import CryptoPair
from tradeapp.exchanges.exchanges import binance
from tradeapp.strategy.strategy import follow_trend_strat_spot

from tradeapp.tools import fetch_cryptopairs
from tradeapp.tools import Signal

from tradeapp.telegram import Telegram

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

#profit
PROFIT = 2
#implement exchange
exchange:ccxt.Exchange = binance()
# get crypto to work with
cryptos_data:List = fetch_cryptopairs(exchange=exchange)
cryptos = [CryptoPair(exchange=exchange,kwargs=data) for data in cryptos_data ]

# put them on strategy
cryptos_signal = {crypto:follow_trend_strat_spot(crypto) for crypto in cryptos[10:]}
# select the one with buy signal
cryptos_with_buy = [crypto for crypto in cryptos_signal if cryptos_signal[crypto]==Signal.BUY]
# send them to telegram
Telegram.send_message(str(cryptos_with_buy))