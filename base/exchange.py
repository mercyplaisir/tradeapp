from abc import ABC,abstractmethod

from base import CryptoPair

class Exchange(ABC):
    """Base class for exchange object"""
    API_URL:str
    @abstractmethod
    def _buy_order(self,cryptopair:CryptoPair):
        """for placing a buy order"""
    @abstractmethod
    def client(self):
        """return client of the exchange object"""
        