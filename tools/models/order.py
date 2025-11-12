from enum import StrEnum,auto


class OrderType(StrEnum):
    LIMIT = auto()
    MARKET = auto()
    STOP = auto()
    TAKE_PROFIT = auto()
    STOP_MARKET = auto()
    TAKE_PROFIT_MARKET = auto()
    TRAILING_STOP_MARKET = auto()
    
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return  self.name
    
class OrderSide(StrEnum):
    """_summary_

    Args:
        StrEnum (_type_): _description_

    Returns:
        _type_: _description_
    """
    BUY = auto()
    SELL = auto()

    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return  self.name