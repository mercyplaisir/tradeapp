"""Representation of an Order object"""

import asyncio
import time
from dataclasses import dataclass

import requests
from binance import BinanceSocketManager, AsyncClient
from common import (
    TAKE_PROFIT,
    percent_change,
    URL,
)


endpoints = {"status": "/status", "history": "/history"}  # for order history


@dataclass
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

    def track_order(self):
        """Create a loop tracking the order until the TAKEPROFIT hitted"""
        order_symbol = self.symbol
        order_price = self.price
        buy_order = True if self.side == "BUY" else False

        async def main():
            client = await AsyncClient.create()
            socket_manager = BinanceSocketManager(client)
            # start any sockets here, i.e a trade socket
            kline = socket_manager.kline_socket(order_symbol)  # .trade_socket('BNBBTC')
            # then start receiving messages
            async with kline as tscm:
                while True:
                    response = await tscm.recv()
                    price = float(response["k"]["c"])

                    pourcentage_change = percent_change(float(order_price), price)

                    if (buy_order and pourcentage_change >= TAKE_PROFIT) or (
                        not buy_order and pourcentage_change >= -TAKE_PROFIT
                    ):
                        print("profit")
                        # release function
                        break
                    else:
                        print(
                            f"price:{price} - profit:{pourcentage_change}"
                            + " - still waiting..."
                        )
                        time.sleep(2.5)
            await client.close_connection()
            # return response

        while True:
            try:
                loop = asyncio.get_event_loop()

                loop.run_until_complete(main())
                break
            except asyncio.exceptions.TimeoutError:
                pass


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
# order.track_order()
# print(order)
