from random import randint
import datetime
import sys
sys.path.append(sys.path[0]+'/../..')

import pandas as pd
from src.view.tools import BINANCEKLINES, Tool, APIKEYPATH
from src.view.VirtualAccount import VirtualAccount

from src.model.Indicators import *

x = Tool.read_json(APIKEYPATH)
y= pd.read_csv(BINANCEKLINES)



print(APIKEYPATH)
print(x)



r = Macd()
s = Rsi()

i = Bollingerbands()
j = Stochastic()

k = Sma()


print(r.priceStudy(),s.priceStudy(),i.priceStudy(),j.priceStudy(),k.priceStudy())
