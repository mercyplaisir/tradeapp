import datetime
import json
from tools import FILESTORAGE, Tool as tl

from BinanceApi import Binance as bnc


FILEPATH = "virtualaccount.json"


"""
{
    "usd_balance": 80,
    "btc_balance": 0,
    "bnb_balance": 100
}
"""

class VirtualAccount:

    def __init__(self):
        self.dicte:dict = tl.read_json(FILEPATH)

        self.usdtBalance:float = self.dicte["usdt_balance"]
        self.btcBalance:float = self.dicte["btc_balance"]
        self.have_usdt = True
         



    def setUsdtBalance(self, usdBalance:float):
        self.dicte["usd_balance"] = usdBalance
        tl.rewrite_json(FILEPATH,self.dicte)
    
    def getUsdBalance(self):
        self.dicte: dict = tl.read_json(FILEPATH)
        self.usdtBalance: float = self.dicte["usdt_balance"]
        return self.usdtBalance
    
    def setBtcBalance(self, btcBalance):
        self.dicte["btc_balance"] = btcBalance
        tl.rewrite_json(FILEPATH, self.dicte)

    def getBtcBalance(self):
        self.dicte: dict = tl.read_json(FILEPATH)
        self.btcBalance: float = self.dicte["btc_balance"]
        return self.usdBalance

    def virtualBuy(self, coin_to_trade: str, order_quantity:float):
        coinName = coin_to_trade.replace(self.baseCoin, '')
        self.dicte[f"{coinName}_balance"] = order_quantity
        tl.rewrite_json(FILEPATH,self.dicte)
        self.have_usdt = False

        self.saveTrades_DB(
            coin_to_trade=coin_to_trade,
            quantity=order_quantity,
            orderType="market buy"
        )
        pass

    def virtualSell(self, coin_to_trade: str, order_quantity: float):
        coinName = coin_to_trade.replace(self.baseCoin, '')
        if not self.have_usdt:
            self.have_usdt = True
            
            coin = bnc.coinPriceChange(coin_to_trade)
            self.dicte["usdt_balance"] = order_quantity * coin["price"]

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

    
