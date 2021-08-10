import datetime

from BinanceApi import Binance as bnc

from .tools import FILEPATH, Tool as tl


"""
{
    "USDT": 80,
    "BTC": 0,
    "BNB": 100
}
"""


class VirtualAccount:

    def __init__(self,baseCoin:str):
        self.dicte: dict = tl.read_json(FILEPATH)
        self.baseCoin = baseCoin

    def setBalance(self, coin: str, balance: float):
        """
        Parameters:

        -coin: str. ex:BTC
        -balance: float
        """
        self.dicte[f"{coin}"] = balance
        tl.rewrite_json(FILEPATH, self.dicte)

    def getBalance(self, coin: str):
        """
        Parameters:

        -coin: str. ex:BTC
        """
        self.dicte: dict = tl.read_json(FILEPATH)
        balance: float = self.dicte[f"{coin}"]
        return balance

    def virtualBuy(self, coin_to_trade: str, order_quantity: float):
        coinName = coin_to_trade.replace(self.baseCoin, '')
        
        self.dicte[f"{coinName}"] = order_quantity
        self.dicte[f"{self.baseCoin}"] = 0

        tl.rewrite_json(FILEPATH, self.dicte)
        

        self.saveTrades_DB(
            coin_to_trade=coin_to_trade,
            quantity=order_quantity,
            orderType="market buy"
        )
        pass

    def virtualSell(self, coin_to_trade: str, order_quantity: float,coinPrice:float):
        coinName = coin_to_trade.replace(self.baseCoin, '')
    
        self.dicte[f"{self.baseCoin}"] = order_quantity * coinPrice
        self.dicte[f"{coinName}"] = self.dicte[f"{coinName}"] - order_quantity

        tl.rewrite_json(FILEPATH, self.dicte)

        self.saveTrades_DB(
            coin_to_trade=coin_to_trade,
            quantity=order_quantity,
            orderType="market sell"
        )
        pass

    def saveTrades_DB(self, coin_to_trade: str, orderType: str, quantity: float):
        coinName = coin_to_trade.replace(self.baseCoin, '')
        mycursor = self.mydb.cursor()

        mycursor.execute(
            f"insert into Trades(coinName,crypto,quantity,orderType,tradeTime) values({coinName},{coin_to_trade},{quantity},{orderType},{datetime.datetime.now()})")
