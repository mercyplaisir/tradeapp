"""
represent pair
"""
from typing import Dict, Protocol,Any

from tradeapp.exchange import Exchange


class Crypto:
    def __init__(self,name:str,ex: Exchange) -> None:
        self.name = name
        self.ex = ex
    @property
    def balance(self) -> float|int:
        return self._balance[0]
    @property
    def locked(self) -> float|int:
        pass
    @property
    def total(self) -> float|int:
        pass
    def _balance(self):
        data:Dict[str,float|int] = self.get_balance()
        free,used,total = data.values()
        return free,used,total
    
    def get_balance(self)->Dict:
        return self.ex.fetch_balance(currency=self.name)


class CryptoPair:
    """
    represent a crypto Pair 
    ex:'BTCUSDT' - BTC/USDT
    base currency ↓
                BTC / USDT
                ETH / BTC
                DASH / ETH
                        ↑ quote currency
    """
    def __init__(self,exchange:Exchange, kwargs:Dict) -> None:
        """
            Args:
                details (Dict): 
                {   "symbol": "ETHBTC",
                    "status": "TRADING",
                    "baseAsset": "ETH",
                    "baseAssetPrecision": "8",
                    "quoteAsset": "BTC",
                    "quotePrecision": "8",
                    "quoteAssetPrecision": "8",
                    "baseCommissionPrecision": "8",
                    "quoteCommissionPrecision": "8"
                }
        """
        assert kwargs['symbol'] , "symbol name not provided"
        
        self.exchange: Exchange = exchange
        self.__dict__.update(kwargs)
    
    def get_symbol(self):
        return self.symbol
    def get_baseAsset(self):
        return Crypto(self.baseAsset,ex=self.exchange)
    def get_quoteAsset(self):
        return Crypto(self.quoteAsset,ex=self.exchange)
    def buy_order(self) ->None :
        """buy order

        Returns:
            Dict[str, str]: order details
        """
        amount = self.get_quoteAsset().balance/self.get_price()
        
        self.ex.create_market_buy_order(
            symbol = self.get_symbol(),
            amount = round(amount,self.baseAssetPrecision)
            )
    def sell_order(self) -> None :
        """sell order

        Returns:
            Dict[str, str]: order details
        """
        amount = self.get_baseAsset().balance
        
        self.ex.create_market_sell_order(
            symbol = self.get_symbol(),
            amount = round(amount,self.quoteAssetPrecision)
        )
    
    @classmethod
    def _fetch_all_cryptopairs(cls, exchange:Exchange) :
        """Get all crypto used in the exchange

        Returns:
            List[CryptoPair]: Cyptopair object
        """
    
        
        data = exchange.load_markets(True)
        # only for spot trading
        return [CryptoPair(cry, exchange) for cry in data if cry['spot'] and cry['active']] 
        

    