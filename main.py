
from tradeapp.exchanges.binancef.binanceFuture import (
    binance_future,
    get_bal_of,
    market_buy_order,
    klines_future,
    last_price,
    market_sell_order
)
from tradeapp.exchanges.binancef.models.timeframe import Timeframe
from tradeapp.exchanges.binancef.tools import nearby_numbers,take_profit,stop_loss
from tradeapp.exchanges.binancef.track import chart_track, track
from tradeapp.exchanges.binancef.models.candle import get_candle,Candle

from tools.telegram import Telegram
from tools.logs import create_logger
from tools.supandres import sup_res
from tools.img_generator import generate_image

from dotenv import load_dotenv


def main():
    notification = Telegram

    log = create_logger(__name__)

    load_dotenv()  # take environment variables from .env.

    #tp/sl
    tp = 0.05/100
    sl = 0.50/100


    # exchange
    ex = binance_future()
    #crypto to trade
    crypto = 'ETHUSDT'
    m = f"working with {crypto}"
    log.info(m)
    notification.send_message(m)

    leverage = 10
    balance = get_bal_of(ex=ex, crypto="USDT")
    # price
    price = last_price(crypto)

    # get klines for sup and res
    klines = klines_future(crypto, Timeframe.M15)

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
    chart_track(crypto,nearby_points)

    # if touch the points get the candle type
    candle = get_candle(crypto,Timeframe.H1)

    # place an order against the candle
    if candle == Candle.RED:
        market_buy_order(
            exchange= ex,
            symbol = crypto,
            quantity = (balance*leverage)/price,
            recvWindow = 5000,
        )
        lp = last_price(crypto)
        tp = take_profit(lp,tp)
        sl = stop_loss(lp,sl)
        # track for tp/sl
        track(crypto,tp,sl)
        # get out
        market_sell_order(
            exchange= ex,
            symbol = crypto,
            quantity = (balance*leverage)/price,
            recvWindow = 5000,
            isolated = True,
        )
    if candle == Candle.GREEN:
        market_sell_order(
            exchange= ex,
            symbol = crypto,
            quantity = (balance*leverage)/price,
            recvWindow = 5000,
            isolated = True,
        )
        lp = last_price(crypto)
        tp = take_profit(lp,tp)
        sl = stop_loss(lp,sl)
        # track for tp/sl
        track(crypto,tp,sl)
        # get out
        market_buy_order(
            exchange= ex,
            symbol = crypto,
            quantity = (balance*leverage)/price,
            recvWindow = 5000,
        )



if __name__ =="__main__":
    main()