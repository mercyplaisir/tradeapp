""" Main file to run the trading bot"""

import os
from typing import Dict, List

from dotenv import load_dotenv,find_dotenv

from exchanges.binanceFuture import BinanceFuture

from tools.track import chart_track, track

from tools.models.candle import get_candle,Candle
from tools.models.timeframe import Timeframe

from tools.logs import create_logger

from tools.supandres import sup_res

from tools.img_generator import generate_image

from tools.tools import settings_loader
from tools.tools import nearby_numbers,take_profit,stop_loss

from telegram.telegram import TelegramChanel

load_dotenv(find_dotenv())

STABLECOIN = "USDT"

chanel_id = os.getenv('CHATID')
chanel_token = os.getenv('TOKEN')

api_key= os.getenv('BINANCEPUBLICKEY')
secret_key= os.getenv('BINANCEPRIVATEKEY')


settings:dict = settings_loader()
print(settings)


log = create_logger(__name__)

#tp/sl
TAKEPROFIT = 0.05/100
STOPLOSS = 0.50/100
LEVERAGE = 10

notification = TelegramChanel(name="money machine",token=chanel_token,chat_id=chanel_id)

# exchange
exchange = BinanceFuture(apikey=api_key,secretkey=secret_key)

def send_points_image(notification,points,pair,klines,support,resistance):
    img = generate_image(data = klines,hlines = points,title=pair,support=support,resistance=resistance)
    notification.send_image(img)


def main():
    """main function"""  
    crypto_i_have = settings['crypto_i_have'] # e.g USDC or BTC
    crypto_to_trade:list = settings['crypto_list']
    pair = settings['pair']
    last_coin = settings['crypto']

    if crypto_i_have != STABLECOIN:
        log.error('you can only trade with %s as quote currency',STABLECOIN)
        coin_balance= exchange.get_balance(last_coin)
        exchange.market_sell_order(
        exchange= exchange,
        symbol = crypto_i_have+STABLECOIN,
        quantity = coin_balance,#(balance*leverage)/price,
        recvWindow = 5000,
        isolated = True)

    balance = exchange.get_balance(STABLECOIN)
    if balance <=0:
        log.error('you have no %s to trade with',STABLECOIN)
        return
    
    notification.send_message(f'you have {balance} {STABLECOIN} to trade with')
    # price
    for crypto in crypto_to_trade: # ex: BTC,ETH
        log.info('trading pair %s',pair)
        pair = crypto+STABLECOIN

        # get klines for sup and res
        log.info('getting klines for %s',pair)
        klines = exchange.klines(pair, interval=Timeframe.M15)

        price = exchange.last_price(pair)

        # get res and support
        log.info('getting sup and res for %s',pair)
        points:Dict[str,List[float]] = sup_res(klines)

        # select support and resistance near the price to work on

        nearby_points = nearby_numbers(data=points,nb=price,pick=1)


        # send image
        notification.send_message(f'target  {points}')
        send_points_image(notification,points,pair,klines,support=points.get('support',[]),resistance=points.get('resistance',[]))

        # track if it
        # log.info('tracking %s on points %s',pair,nearby_points)
        # chart_track(pair,nearby_points)

        # if touch the points get the candle type
        candle = get_candle(pair,Timeframe.H1)

    # place an order against the candle
        if candle == Candle.RED:
            log.info('placing buy order for %s',pair)
            exchange.market_buy_order(
                symbol = pair,
                quantity = (balance*LEVERAGE)/price,
                recvWindow = 5000,
            )
            lp = exchange.last_price(pair)
            tp = take_profit(lp,TAKEPROFIT)
            sl = stop_loss(lp,STOPLOSS)
            # track for tp/sl
            track(pair,tp,sl)
            # get out
            log.info('placing sell order for %s',pair)
            exchange.market_sell_order(
                symbol = pair,
                quantity = (balance*LEVERAGE)/price,
                recvWindow = 5000,
                isolated = True,
            )
        elif candle == Candle.GREEN:
            log.info('placing sell order for %s',pair)
            lp = exchange.last_price(pair)
            tp = take_profit(lp,TAKEPROFIT)
            sl = stop_loss(lp,STOPLOSS)
            exchange.market_sell_order(
                symbol = pair,
                quantity = (balance*LEVERAGE)/price,
                recvWindow = 5000,
                isolated = True,
            )
            # track for tp/sl
            track(pair,tp,sl)
            # get out
            log.info('placing buy order for %s',pair)
            exchange.market_buy_order(
                symbol = pair,
                quantity = (balance*LEVERAGE)/price,
                recvWindow = 5000,
            )

def closing():
    """for closing the script
    """
    print("closing all connections")
    return

if __name__ =="__main__":
    try:
        main()
    except KeyboardInterrupt:
        closing()
