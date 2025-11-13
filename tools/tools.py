"""function tools
		"""
import time
from typing import Dict, List
import json

import ccxt

from tools.logs import logger_wrapper


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
@logger_wrapper(__name__,"getting current timestamp")
def now_timestamp() -> int:
		""" get current timestamp in milliseconds"""
		return int(round(time.time() * 1000))

def save(data):
		"""save json file

		Args:
				data (any): any
		"""
		with open('tradeapp/results/data.json','+w',encoding='utf-8') as f:
				return f.write(json.dumps(data))

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


@logger_wrapper(__name__,"getting nearby points")
def nearby_numbers(data:dict,nb:int|float,pick:int=0) -> Dict[str, float] | Dict[str, List[float]]:
		""""get nearby numbers from a list"""
		dd = []
		dt = data['supports_levels'] + data['resistance_levels']
		for d in dt:

				dd.append(abs(d-nb))
				dd.sort()
		# print('dd',dd)
		l = {i : abs(nb-i) for i in dt}
		rs:List[float] = []
		for d in dd:
				for key ,value in l.items():
						if value == d:
								if key not in rs:
										rs.append(key)
		if pick==0 or pick == 1:
				
			return {'support':rs[0]} if rs[0] in data['supports_levels'] else {'resistance':rs[0]}
		else:
			return {'support':rs[:pick]} if rs[:pick] in data['supports_levels'] else {'resistance':rs[:pick]}


def take_profit(price:float|int,percent:float)->float:
		""" calculate the take profit price given a price and a percent"""
		return price + (price*percent)

def stop_loss(price:float,percent:float)->float:
		"""calculate the stop loss price given a price and a percent"""
		return price - (price*percent)

def settings_loader()->Dict:
		"""load the settings from the settings.json file"""
		setting_file = "./settings.json"
		with open(file=setting_file,mode='r',encoding='utf-8') as f:
				data = json.load(f)
		return data
