from enum import Enum,auto


class Timeframe(Enum):
    M1 = '1m'
    M5 = '5m'
    M15 = '15m'
    M30 = '30m'
    H1 = '1h'
    H4 = '4h'
    DAY = '1d'
    WEEK = '1w'

    def __repr__(self) -> str:
        return  f'{self.value}'

    def __str__(self) -> str:
        return  f'{self.value}'
    def __eq__(self, __value: object) -> bool:
        return self.value==__value
    def __hash__(self) -> int:
        return hash(self.value)