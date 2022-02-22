from dataclasses import dataclass

import requests

from src.platforms.binance import URL

endpoints = {"status": "/status", "history": "/history"}  # for order history


@dataclass()
class Order:
    """Representation of an Order passed by binance API

      {
    "symbol": "BTCUSDT",
    "orderId": 28,
    "orderListId": -1,# //Unless OCO, value will be -1
    "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
    "transactTime": 1507725176595,
    "price": "0.30000000",
    "origQty": "10.00000000",
    "executedQty": "10.00000000",
    "cummulativeQuoteQty": "10.00000000",
    "status": "FILLED",
    "timeInForce": "GTC",
    "type": "MARKET",
    "side": "SELL"
      }

    """

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
        """save by sending order to the assistant server"""
        self._send_request()

    def dict(self):
        """return dict object of all variable of the class"""
        return self.__dict__

    def _send_request(self):
        """send request to the server"""
        data = self.dict()
        history_url = URL + endpoints["history"]
        requests.post(history_url, data=data)


# d={
#   "symbol": "BTCUSDT",
#   "orderId": 28,
#   "orderListId": -1,# //Unless OCO, value will be -1
#   "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
#   "transactTime": 1507725176595,
#   "price": "0.30000000",
#   "origQty": "10.00000000",
#   "executedQty": "10.00000000",
#   "cummulativeQuoteQty": "10.00000000",
#   "status": "FILLED",
#   "timeInForce": "GTC",
#   "type": "MARKET",
#   "side": "SELL"
# }

# order=Order(**d)
# print(order.price)
