import os

import ccxt


def binance() -> ccxt.Exchange:
    keys = {
        'public_key': os.getenv('BINANCEPUBLICKEY'),
        'private_key' : os.getenv('BINANCEPRIVATEKEY')
    }
    ex = ccxt.binance(keys)
    return ex