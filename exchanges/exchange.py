from typing import Any


class Exchange:
    """ 
    Base class for exchange interactions
    
    """
    def buy_order(self,*args, **kwargs)->Any:
        """send a buy order"""
        return
    def sell_order(self,*args, **kwargs)->Any:
        """send a sell order"""
        return
    def fetch_cryptopairs(self,*args, **kwargs)->Any:
        """fetch all available crypto pairs"""
        return
    def klines(self,*args, **kwargs)->Any:
        """query klines/candles data"""
        return
    def last_price(self,*args, **kwargs)->Any:
        """fetch last price of a given pair"""
        return
    def get_balance(self,*args, **kwargs)->Any:
        """fetch balance of a given crypto"""
        return
    def place_order(self,*args, **kwargs)->Any:
        """place an order"""
        return
    def cancel_order(self,*args, **kwargs)->Any:
        """cancel an order"""
        return
    def order_status(self,*args, **kwargs)->Any:
        """fetch order status"""
        return
    def fetch_open_orders(self,*args, **kwargs)->Any:
        """fetch all open orders"""
        return
    def limit_order(self,*args, **kwargs)->Any:
        """send a limit order"""
        return
    def limit_buy_order(self,*args, **kwargs)->Any:
        """send a limit buy order"""
        return
    def limit_sell_order(self,*args, **kwargs)->Any:
        """send a limit sell order"""
        return
