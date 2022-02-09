
from dataclasses import dataclass

from src.controller.dbcontroller.mysqlDB import mysqlDB

@dataclass()
class Order:
    """Binance Order Class"""
    database = mysqlDB()
    
    #orderDetails : dict
    orderId :int#= orderDetails['orderId']
    symbol :str#= orderDetails['symbol']
 
    side :str#= orderDetails['side']
    transactTime :int #= orderDetails['transactTime']
    status:str# = orderDetails['status']
    executedQty :str#= orderDetails['executedQty']
        
    def save(self):
        self.database.requestDB(f"insert into orders(orderId,symbol,type,side,transactTime,status,executedQty) values("
                                f"{self.orderId},{self.symbol},'market',{self.side},{self.transactTime},"
                                f"{self.status},{self.executedQty})")

    @staticmethod
    def get_all_orders():
        database = mysqlDB()
        results = database.selectDB(f"select * from orders")

        return results
