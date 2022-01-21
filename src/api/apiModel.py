from abc import ABC,abstractmethod

class ApiModel(ABC):
    @abstractmethod
    def buy_order(self):
        pass
    @abstractmethod
    def sell_order(self):
        pass
    @abstractmethod
    def status():
        pass
    