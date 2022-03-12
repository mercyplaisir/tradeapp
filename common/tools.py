"""
got some useful math formula
"""
import asyncio
from decimal import Decimal
import time
from typing import Type, Union, Optional, Dict
import dateparser
import math
import pytz
from datetime import datetime

import requests
from binance import BinanceSocketManager,AsyncClient
# from base.order import Order

# from dbcontroller import DbEngine
# from base import Coin

TAKE_PROFIT = 0.5
STOP_LOSS = 0.5

TIMEFRAME: str = "15m"

URL = "https://tradeappapiassistant.herokuapp.com/tradeapp"

STATUS_ENDPOINT = "/status"
HISTORY_ENDPOINT = "/history"


# db = DbEngine()

def percent_calculator(number: float, percentage: float) -> float:
    """
    return z = z + z*x/100
    ex: 100 + 2% =102
    """
    z = number + ((number * percentage) / 100)
    return z

def percent_change(original_number: float, new_number: float) -> int:
    """
    percent variation between two numbers
    ex: 100 and 98 -> -2%
    """
    z = ((new_number - original_number) / original_number) * 100
    return z


def send_data( method, endpoint,**kwargs):
        """send requested data to the assistant API"""
        methods = {"get": requests.get,
        "post": requests.post,
        "put": requests.put,
        "delete": requests.delete}
        caller = methods[method]
        url = URL+endpoint
        
        caller(url,data=kwargs)



def date_to_milliseconds(date_str: str) -> int:
    """Convert UTC date to milliseconds

    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/

    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    """
    # get epoch value in UTC
    epoch: datetime = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d: Optional[datetime] = dateparser.parse(date_str, settings={'TIMEZONE': "UTC"})
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


def interval_to_milliseconds(interval: str) -> Optional[int]:
    """Convert a Binance interval string to milliseconds

    :param interval: Binance interval string, e.g.: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w

    :return:
         int value of interval in milliseconds
         None if interval prefix is not a decimal integer
         None if interval suffix is not one of m, h, d, w

    """
    seconds_per_unit: Dict[str, int] = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60,
    }
    try:
        return int(interval[:-1]) * seconds_per_unit[interval[-1]] * 1000
    except (ValueError, KeyError):
        return None


def round_step_size(quantity: Union[float, Decimal], step_size: Union[float, Decimal]) -> float:
    """Rounds a given quantity to a specific step size

    :param quantity: required
    :param step_size: required

    :return: decimal
    """
    precision: int = int(round(-math.log(step_size, 10), 0))
    return float(round(quantity, precision))


def convert_ts_str(ts_str):
    if ts_str is None:
        return ts_str
    if type(ts_str) == int:
        return ts_str
    return date_to_milliseconds(ts_str)



# def get_coin_data():
#     """just for view"""
#     all_coins = Coin.get_all_coins()

#     data: dict = {coin.name: coin.get_cryptopair_related() for coin in all_coins}

#     data = {n: [str(l) for l in ll] for n, ll in data.items()}

#     nn = json.dumps(data)
#     with open("coindata.json", "w") as f:
#         f.write(nn)

# SELECT cryptopair FROM relationalcoin WHERE basecoin or quotecoin not in (SELECT shortname from Coin)

# def clean_database():
    
#     requete = "DELETE  FROM relationalcoin WHERE basecoin not in (SELECT shortname from Coin)"
#     db.requestDB(requete= requete)

def cout(*args):
    now = datetime.time(datetime.now())
    time_info = f'time -> {now}'
    print(f'{args} \t {time_info}')



def track_order(order):
        """Create a loop tracking the order until the TAKEPROFIT hitted"""
        order_symbol = order.symbol
        order_price = order.price
        buy_order = True if order.side == "BUY" else False

        cout(f'orderPrice:{order_price}')
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
                    # cout(response)

                    pourcentage_change = percent_change(float(order_price), price)

                    profit_in_buy = buy_order and pourcentage_change >= TAKE_PROFIT
                    profit_in_sell = not buy_order and -pourcentage_change >= TAKE_PROFIT
                    
                    profit = profit_in_buy or profit_in_sell

                    loss_in_buy = buy_order and -pourcentage_change >=  STOP_LOSS
                    loss_in_sell = not buy_order and pourcentage_change >= STOP_LOSS

                    loss = loss_in_buy or loss_in_sell

                    if profit or loss :
                        cout("tracking ended")
                        order.profit_change(pourcentage_change)
                        break
                    else:
                        cout(
                            f"price:{price} - profit:{round(pourcentage_change,2)} - all time profit : {round(order.profit,2)}"
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

