"""function tools
    """
from dataclasses import dataclass
from enum import Enum,auto
from typing import Dict, List
import json

import ccxt

class OrderType(Enum):
    MARKET = auto()
    LIMIT = auto()

    def __str__(self) -> str:
        return f'{self.name}'
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    def __hash__(self) -> int:
        return hash(self.name)

class Signal(Enum):
    BUY = auto()
    SELL = auto()
    
    def __str__(self) -> str:
        return f'{self.name.lower}'


class Trend(Enum):
    UPTREND = auto()
    DOWNTREND = auto()
    
    def __str__(self) -> str:
        return f'{self.name}'
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name
    def __hash__(self) -> int:
        return hash(self.name)

class Timeframe(Enum):
    M1 = '1m'
    M5 = '5m'
    M15 = '15m'
    M30 = '30m'
    H1 = '1h'
    H4 = '4h'
    DAY = '1d'
    WEEK = '1w'

    def __repr__(self) -> str:
        return  f'{self.value}'

    def __str__(self) -> str:
        return  f'{self.value}'
    def __eq__(self, __value: object) -> bool:
        return self.value==__value
    def __hash__(self) -> int:
        return hash(self.value)

def save(data):
    with open('tradeapp/results/data.json','+w') as f:
        f.write(json.dumps(data))

def fetch_cryptopairs(exchange: ccxt.Exchange) -> List[Dict]:
        """Get all crypto used in the exchange

        Returns:
            List[CryptoPair]: Cyptopair object
        """

        data = exchange.load_markets(True)
        # ccxt binance instance
        
        # only for spot trading
        save([data[cry]['info'] for cry in data if data[cry]["spot"] and data[cry]["active"]])
        return [data[cry]['info'] for cry in data if data[cry]["spot"] and data[cry]["active"]]


