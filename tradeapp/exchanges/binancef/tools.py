"""function tools
    """
from dataclasses import dataclass
from enum import Enum,auto
from typing import Dict, List
import json

import ccxt

class aobject(object):
    """Inheriting this class allows you to define an async __init__.

    So you can create objects by doing something like `await MyClass(params)`
    """
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        pass


def save(data):
    with open('tradeapp/results/data.json','+w') as f:
        f.write(json.dumps(data))

def fetch_cryptopairs(exchange: ccxt.Exchange) -> List[Dict]:
        """Get all crypto used in the exchange

        Returns:
            List[CryptoPair]: Cyptopair object
        """

        data = exchange.load_markets(True)
        # ccxt binance instance
        
        # only for spot trading
        save([data[cry]['info'] for cry in data if data[cry]["spot"] and data[cry]["active"]])
        return [data[cry]['info'] for cry in data if data[cry]["spot"] and data[cry]["active"]]
def nearby_numbers(dt:list,nb:int|float,pick:int=0):
  dd = []
  for d in dt:
    dd.append(abs(d-nb))
    dd.sort()
  print('dd',dd)
  l = {i : abs(nb-i) for i in dt}
  rs = []
  for d in dd:
    for key ,value in l.items():
      if value == d:
        if key not in rs:
          rs.append(key)
  if pick==0:
    return rs
  else:
    return rs[:pick]