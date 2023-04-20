"""
represent pair
"""
from typing import Dict

class CryptoPair(object):
    """
    represent a crypto Pair 
    ex:'BTCUSDT' - BTC/USDT
    """
    def __init__(self, details:Dict) -> None:
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
        assert details['symbol'] , "symbol name not provided"
        self.__dict__.update(details)
