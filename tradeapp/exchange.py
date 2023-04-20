"""representation of exchange
    """

from abc import ABC,abstractmethod
from typing import Dict,List

class Exchange(ABC):
    """representstion of an exchange

    Args:
        object (_type_): _description_
    """
    @abstractmethod
    def buy_order(self) -> Dict[str,str]:
        pass
    @abstractmethod
    def sell_order(self) -> Dict[str,str]:
        pass

    