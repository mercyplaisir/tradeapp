"""Base representation of all classes"""
from abc import ABC,abstractmethod

class Exchange(ABC):
    """Abstract base class of all exchanges"""
    @abstractmethod
    def buy_order(self,*args,**kwargs):
        """for buy order"""
    @abstractmethod
    def sell_order(self,*args,**kwargs):
        """for sell order"""
    
    #turning into a context manager to track
    # when it goes down
    @abstractmethod
    def __enter__(self):
        """enter function for the context manager"""
    @abstractmethod
    def __exit__(self,*args,**kwargs):
        """exit function """