from enum import StrEnum,auto


class Order_type(StrEnum):
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
    
class Order_side(StrEnum):
    BUY = auto()
    SELL = auto()

    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return  self.name