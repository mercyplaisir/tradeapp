    
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

from telegram.telegram import Telegram
from tools.logs import create_logger
from tools.supandres import sup_res
from tools.img_generator import generate_image
from tools.tools import settings_loader

def main():
    settings:dict = settings_loader()
    print(settings)
    notification = Telegram

    log = create_logger(__name__)


    #tp/sl
    tp = 0.05/100
    sl = 0.50/100


    # exchange
    ex = binance_future()
    #pair to trade
    crypto = settings['crypto']
    crypto_i_have = settings['crypto_i_have']

    pair = settings['pair']
          
    m = f"working with {crypto}"
    log.info(m)
    notification.send_message(m)

    leverage = 10
    balance = get_bal_of(ex=ex, crypto=crypto_i_have)
    notification.send_message(f'you have {balance} {crypto_i_have}')
    # price
    price = last_price(pair)

    # get klines for sup and res
    klines = klines_future(pair, Timeframe.M15)

    # get res and support
    points = sup_res(klines)

    # select points near the price to work on
    nearby_points = nearby_numbers(points,price,1)
    notification.send_message(f'target  {nearby_points}')
    
    # send image
    img = generate_image(data = klines,hlines = nearby_points)
    Telegram.send_image(img)

    # track
    # TODO make it recursive
    chart_track(pair,nearby_points)

    # if touch the points get the candle type
    candle = get_candle(pair,Timeframe.H1)

    # place an order against the candle
    if candle == Candle.RED:
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
        market_sell_order(
            exchange= ex,
            symbol = pair,
            quantity = (balance*leverage)/price,
            recvWindow = 5000,
            isolated = True,
        )
    if candle == Candle.GREEN:
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
        market_buy_order(
            exchange= ex,
            symbol = pair,
            quantity = (balance*leverage)/price,
            recvWindow = 5000,
        )



if __name__ =="__main__":
    main()