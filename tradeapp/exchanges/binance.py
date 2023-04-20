from typing import Dict,List
import os

import ccxt

from tradeapp.cryptopair import CryptoPair
from exchange import Exchange

class Binance(Exchange):
    
    def __init__(self) -> None:
        keys = self._get_keys()
        self.ex = ccxt.binance(keys) # exchange instance of ccxt
    
    def buy_order(self) -> Dict[str, str]:
        """buy order

        Returns:
            Dict[str, str]: order details
        """
        # TODO implement a buy order 
    def sell_order(self) -> Dict[str, str]:
        """sell order

        Returns:
            Dict[str, str]: order details
        """
        # TODO implement a sell order
    def _get_keys(self) ->Dict[str,str]:
        """Binance keys

        Returns:
            Dict[str,str]: keys
        """
        return {
            'public_key': os.getenv('BINANCEPUBLICKEY'),
            'private_key' : os.getenv('BINANCEPRIVATEKEY')
        }
    
    
    
    def _fetch_cryptopairs(self) -> List[CryptoPair]:
        """Get all crypto used in the exchange

        Returns:
            List[CryptoPair]: Cyptopair object
        """
        res = []
        data = self.ex.load_markets(True)
        for crypto in data:
            crypto_data:Dict = crypto['info']
            #create cryptopair instance
            cry: CryptoPair = CryptoPair(crypto_data)
            #append in list
            if cry.status == 'TRADING':
                res.append(cry)
        return res

    