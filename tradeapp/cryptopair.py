"""
represent pair
"""
from typing import Dict, List,Protocol,Any, Self

from tradeapp.protocols import Exchange
from tradeapp.tools import OrderType

class Crypto:
    def __init__(self,name:str,ex: Exchange) -> None:
        self.name = name
        self.ex = ex
    @property
    def balance(self) -> float|int:
        return self._balance()[0]
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
    def __init__(self,exchange: Exchange, kwargs:Dict) -> None:
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
    def load_cryptopair_from(cls,data:Dict[Exchange,List[dict]]) :
        """create Cryptopairs instance using list of data given

        Args:
            data (List[dict]): _description_

        Returns:
            _type_: _description_
        """
        assert len(data)>0 , "data can't be empty" 
        exchange = list(data.keys())[0]
        return [CryptoPair(kwargs=d) for d in data.values()]

    def __str__(self) -> str:
        return f"looking at {self.get_symbol()} \n "