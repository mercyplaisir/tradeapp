from tradeapp.protocols import Exchange
from tradeapp.exchanges.binance import Binance 

BALANCE = 100

def main():
    ex:Exchange = Binance(balance=BALANCE)
    