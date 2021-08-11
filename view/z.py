from random import randint
import datetime
import sys
sys.path.append(sys.path[0] +'/..')

import pandas as pd
from view.tools import BINANCEKLINES, Tool, APIKEYPATH
from view.VirtualAccount import VirtualAccount


x = Tool.read_json(APIKEYPATH)
y= pd.read_csv(BINANCEKLINES)



print(APIKEYPATH)
print(x)


