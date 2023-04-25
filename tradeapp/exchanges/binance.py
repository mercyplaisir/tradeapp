from typing import Any, Dict,List,Protocol
import os

import ccxt

from tradeapp.protocols import Exchange

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
    
    
    
    def fetch_cryptopairs(self) -> List[Dict]:
        """Get all crypto used in the exchange

        Returns:
            List[CryptoPair]: Cyptopair object
        """
    
        
        data = self.ex.load_markets(True)
        #ccxt binance instance
        exchange = self.ex
        # only for spot trading
        return {exchange : [cry for cry in data if cry['spot'] and cry['active']]} 
        
        

    