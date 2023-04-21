from typing import Any, Dict,List,Protocol
import os

import ccxt

from exchange import Exchange
from tradeapp.order import OrderType

class CryptoType(Protocol):
    def get_symbol(self) -> str:
        ...
    

class Binance(Exchange):
    
    def __init__(self,balance:float) -> None:
        keys = self._get_keys()
        self.balance:float = balance
        self.ex = ccxt.binance(keys) # exchange instance of ccxt
     
    
    def _get_keys(self) ->Dict[str,str]:
        """Binance keys

        Returns:
            Dict[str,str]: keys
        """
        return {
            'public_key': os.getenv('BINANCEPUBLICKEY'),
            'private_key' : os.getenv('BINANCEPRIVATEKEY')
        }
    
    
    
    def _fetch_cryptopairs(self) -> List[CryptoType]:
        """Get all crypto used in the exchange

        Returns:
            List[CryptoPair]: Cyptopair object
        """
    
        
        data = self.ex.load_markets(True)
        # only for spot trading
        return [CryptoType(cry,exchange = self) for cry in data if cry['spot'] and cry['active']] 
        
        

    