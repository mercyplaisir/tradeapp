
from dataclasses import dataclass

@dataclass
class Order:
    """_summary_
    """
    id:str
    symbol:str
    price:float
    amount:float
    datetime:str
    type:str
    side:str
    
    def info(self):
        return f"{self.symbol} bought at {self.price} on {self.datetime}"
    def save(self):
        pass
    def track(self):
        """
        for tracking an order
        """
