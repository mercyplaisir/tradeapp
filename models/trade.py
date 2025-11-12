from dataclasses import dataclass

from typing import Protocol

class SymbolProtocol(Protocol):
    ...

class Trade(dataclass):
    symbol:SymbolProtocol
    ENTRY: float
    TP: float
    SL: float
    Quantity: float
    Side: str