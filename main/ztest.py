import btalib as bt
import pandas as pd
from tools import Tool, FILESTORAGE
from BinanceApi import Binance


df = pd.read_csv(f"{FILESTORAGE}/klines.csv", index_col=0)


Binance.set_list_of_crypto()
