"""base Classes for strategies"""
from abc import ABC,abstractmethod

class Strategie(ABC):
    """Abstract parent class for strategies"""
    @classmethod @abstractmethod
    def decision(cls):
        """return decision of the strategies"""

    def __add__(self,other):
        assert isinstance(other,Strategie), "can not perfom addition on type %s"%type(other)
        """adding two strategies return they decision"""
