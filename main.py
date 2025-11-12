    
from traceback import print_tb
from exchanges.binanceFuture import (
    binance_future,
    get_bal_of,
    market_buy_order,
    klines_future,
    last_price,
    market_sell_order   
)
from tools.models.timeframe import Timeframe
from tools.tools import nearby_numbers,take_profit,stop_loss
from tools.track import chart_track, track
from tools.models.candle import get_candle,Candle

from telegram.telegram import TelegramChanel
from tools.logs import create_logger
from tools.supandres import sup_res
from tools.img_generator import generate_image
from tools.tools import settings_loader

import os

from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

STABLECOIN = "USDC"


chanel_id = os.getenv('CHATID')
chanel_token = os.getenv('TOKEN')

settings:dict = settings_loader()
print(settings)


log = create_logger(__name__)


#tp/sl
tp = 0.05/100
sl = 0.50/100
leverage = 10

notification = TelegramChanel(name="money machine",token=chanel_token,chat_id=chanel_id)
# exchange
ex = binance_future()

def returnToBase(ex:ccxt.Exchange,crypto_i_have:str="USDT",last_coin:str="TRX"):
    log.error(f'you can only trade with {STABLECOIN} as quote currency')
    q= ex.get_bal_of(last_coin)
    market_sell_order(
        exchange= ex,
        symbol = crypto_i_have+STABLECOIN,
        quantity = q,#(balance*leverage)/price,
        recvWindow = 5000,
        isolated = True,
    )


def main():

    
    #pair to trade
    # crypto = settings['crypto'] 
    # m = f"working with {crypto}"
    crypto_i_have = settings['crypto_i_have'] # e.g USDC or BTC
    pairs_to_trade:list = settings['crypto_list']
    pair = settings['pair']
    last_coin = settings['crypto']

    if crypto_i_have != STABLECOIN:
        returnToBase()
        
          
    # log.info(m)
    # notification.send_message(m)

    balance = get_bal_of(ex=ex, crypto=crypto_i_have)
    notification.send_message(f'you have {balance} {crypto_i_have}')
    # price
    price = last_price(pair)

    # get klines for sup and res
    log.info(f'getting klines for {pair}')
    klines = klines_future(pair, Timeframe.M15)

    # get res and support
    log.info(f'getting sup and res for {pair}')
    points = sup_res(klines)

    # select points near the price to work on
    nearby_points = nearby_numbers(points,price,1)
    notification.send_message(f'target  {nearby_points}')
    
    # send image
    img = generate_image(data = klines,hlines = nearby_points)
    notification.send_image(img)

    # track
    log.info(f'tracking {pair} on points {nearby_points}')
    chart_track(pair,nearby_points)

    # if touch the points get the candle type
    candle = get_candle(pair,Timeframe.H1)

    # place an order against the candle
    if candle == Candle.RED:
        log.info(f'placing buy order for {pair}')
        market_buy_order(
            exchange= ex,
            symbol = pair,
            quantity = (balance*leverage)/price,
            recvWindow = 5000,
        )
        lp = last_price(pair)
        tp = take_profit(lp,tp)
        sl = stop_loss(lp,sl)
        # track for tp/sl
        track(pair,tp,sl)
        # get out
        log.info(f'placing sell order for {pair}')
        market_sell_order(
            exchange= ex,
            symbol = pair,
            quantity = (balance*leverage)/price,
            recvWindow = 5000,
            isolated = True,
        )
    if candle == Candle.GREEN:
        log.info(f'placing sell order for {pair}')
        market_sell_order(
            exchange= ex,
            symbol = pair,
            quantity = (balance*leverage)/price,
            recvWindow = 5000,
            isolated = True,
        )
        lp = last_price(pair)
        tp = take_profit(lp,tp)
        sl = stop_loss(lp,sl)
        # track for tp/sl
        track(pair,tp,sl)
        # get out
        log.info(f'placing buy order for {pair}')
        market_buy_order(
            exchange= ex,
            symbol = pair,
            quantity = (balance*leverage)/price,
            recvWindow = 5000,
        )

def closing():
    print("closing all connections")
    pass


if __name__ =="__main__":
    try:
        main()
    except KeyboardInterrupt:
        closing()