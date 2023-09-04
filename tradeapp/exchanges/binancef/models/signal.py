from enum import Enum,auto


class Signal(Enum):
    BUY = auto()
    SELL = auto()
    
    def __str__(self) -> str:
        return f'{self.name.lower}'
