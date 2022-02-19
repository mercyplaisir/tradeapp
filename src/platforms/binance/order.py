from dataclasses import dataclass

import requests

from src.dbcontroller.mysqlDB import mysqlDB

URL = "any.url.com"
endpoints = {
    'status': '/status',
    'history': '/history'  # for order history
}


@dataclass()
class Order:
    """Binance Order Class"""
    database = mysqlDB()

    # orderDetails : dict
    symbol: str
    orderId: int
    orderListId: int
    clientOrderId: str
    transactTime: int
    price: str
    origQty: str
    executedQty: str
    cummulativeQuoteQty: str
    status: str
    timeInForce: str
    type: str
    side: str

    def save(self):
        self.database.requestDB(f"insert into orders(orderId,symbol,type,side,transactTime,status,executedQty) values("
                                f"{self.orderId},{self.symbol},'market',{self.side},{self.transactTime},"
                                f"{self.status},{self.executedQty})")
        self.send_request()

    @staticmethod
    def get_all_orders():
        database = mysqlDB()
        results = database.selectDB(f"select * from orders")

        return results

    def dict(self):
        return self.__dict__

    def send_request(self):
        data = self.dict()
        history_url = URL + endpoints['history']
        requests.post(history_url, data=data)
