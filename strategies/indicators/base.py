from typing import Protocol

class Indicator(Protocol):
    """Abstract class of an indicator"""

    @classmethod
    def create_indicator(cls,*args):
        """create the indicator"""
        pass

    @classmethod
    def price_study(cls,*args):
        """study the given price"""
        pass



