"""
represent pair
"""
from __future__ import annotations
import io
from typing import Dict, List, Protocol 


import pandas as pd
import numpy as np
import mplfinance as mpf



from tradeapp.exchanges.binancef.tools import Signal
from tradeapp.exchanges.binancef.tools import Timeframe
from tradeapp.exchanges.binancef.tools import Trend
from tradeapp.exchanges.binancef.tools import OrderType
from tradeapp.exchanges.binancef.tools import aobject

from tradeapp.models import Crypto
from tools.logs import create_logger

log = create_logger(__name__)

class Exchange(Protocol):
    """
    """
    async def load_markets(reload:bool=False) -> None:
        ...
    async def market(symbol:str) -> Dict:
        ...
    async def create_order(*args, **kwargs) -> None:
        ...
    async def fetch_ohlcv(*args, **kwargs) -> None:
        ...

class CryptoPair(aobject):
    """
    represent a crypto Pair
    ex:'BTCUSDT' - BTC/USDT
    base currency ↓
                BTC / USDT
                ETH / BTC
                DASH / ETH
                        ↑ quote currency
    """
    async def __init__(self, exchange: Exchange, symbol:str) -> None:
        """
        Args:
            details (Dict):
            {   "symbol": "ETHBTC",
                "status": "TRADING",
                "baseAsset": "ETH",
                "baseAssetPrecision": "8",
                "quoteAsset": "BTC",
                "quotePrecision": "8",
                "quoteAssetPrecision": "8",
                "quoteAssetPrecision": "8",
                "quoteCommissionPrecision": "8"
            }
        """
        assert symbol, "symbol name not provided"
        log.info(f'creating {symbol}')
        self.exchange = exchange
        self.symbol = symbol
        await self._generate_data()
        self.log =create_logger(f'cryptopair:{self.symbol}')
        
    def __str__(self) -> str:
        return f"{self.baseAsset}/{self.quoteAsset}"

    async def _check(self):
        if not self.exchange.symbols:
            await self.exchange.load_markets(True)
        cond = self.symbol in  self.exchange.symbols
        assert cond, "symbol not available in the exchange try another one"
    
    
    async def _generate_data(self):
        await self._check()
        data =  self.exchange.market(symbol= self.symbol)
        for key in data['info']:
            setattr(self,key,data['info'][key])
        

    @property
    async def trend(self):
        """return the trend

        Returns:
            Trend ( object): the trend object
        """
        self.log.info('get trend')
        return await self.get_trend()

    async def get_base_asset(self):
        """return the base asset as crpto object

        """
        return Crypto(self.baseAsset, ex=self.exchange)

    async def get_quoteAsset(self):
        """return the quote asset as Crypto object"""
        return Crypto(self.quoteAsset, ex=self.exchange)

    async def buy_order(self) -> None:
        """buy order

        Returns:
            Dict[str, str]: order details
        """
        self.log.info('executing buy order')
        amount = await self.get_quoteAsset().balance / self.get_price()

        order_data = await self.exchange.create_order(
            symbol=self.symbol(),
            type=OrderType.MARKET,
            side=Signal.BUY,
            amount=round(amount, self.baseAssetPrecision),
        )
        return  order_data

    async def sell_order(self) -> None:
        """sell ordPer

        Returns:
            Dict[str, str]: order details
        """
        self.log.info('executing sell order')
        balance = await self.get_base_asset().balance
        order_data = await self.exchange.create_order(
            symbol=self.symbol(),
            type=OrderType.MARKET,
            side=Signal.SELL,
            amount=round(balance, self.quoteAssetPrecision),
        )
        return  order_data

    async def get_ohlc(self, timeframe=Timeframe.DAY):
        """
        getting price data
        """
        self.log.info(f'get ohlc data')
        data = await self.exchange.fetch_ohlcv(
            symbol=self.symbol,
            timeframe=timeframe,
        ) 
        data = pd.DataFrame(
            data, columns=["Time", "Open", "High", "Low", "Close", "Volume"]
        )
        data["Time"] = pd.to_datetime(data["Time"], unit="ms")
        # change index to time column
        data = data.set_index("Time")
        self.log.info(f'got the ohlc data')
        return  data

    

    async def get_support_and_resistance(
        self, timeframe: Timeframe = Timeframe.DAY, s_r:bool = True
    ) -> Dict[str, List[float | int]]:
        """return resistance and support on given data

        Args:
            df (pd.DataFrame): contains ohlc of given crypto
        """
        # method 1: fractal candlestick pattern
        # determine bullish fractal
        df: pd.DataFrame = await self.get_ohlc(timeframe=timeframe)

        def is_support(df, i):
            cond1 = df["Low"][i] < df["Low"][i - 1]
            cond2 = df["Low"][i] < df["Low"][i + 1]
            cond3 = df["Low"][i + 1] < df["Low"][i + 2]
            cond4 = df["Low"][i - 1] < df["Low"][i - 2]
            return cond1 and cond2 and cond3 and cond4

        # determine bearish fractal
        def is_resistance(df, i):
            cond1 = df["High"][i] > df["High"][i - 1]
            cond2 = df["High"][i] > df["High"][i + 1]
            cond3 = df["High"][i + 1] > df["High"][i + 2]
            cond4 = df["High"][i - 1] > df["High"][i - 2]
            return cond1 and cond2 and cond3 and cond4

        # a list to store resistance and support levels
        levels = []
        # to make sure the new level area does not exist already
        def is_far_from_level(value, levels, df):
            ave = np.mean(df["High"] - df["Low"])
            return np.sum([abs(value - level) < ave for  level in levels]) == 0

        high_low = {"resistances": [], "supports": []}
        for i in range(2, df.shape[0] - 2):
            if is_support(df, i):
                low = df["Low"][i]

                if is_far_from_level(low, levels, df):
                    levels.append( low)
                    high_low["supports"].append(low)
            elif is_resistance(df, i):
                high = df["High"][i]
                if is_far_from_level(high, levels, df):
                    levels.append( high)
                    high_low["resistances"].append(high)
        if not s_r:
            return levels
        return high_low

    async def get_trend(self, timeframe=Timeframe.DAY) -> Trend:
        """give the trend of the current stock

        Args:
            df (pd.DataFrame): contains ohlc data of given crypto
        """
        # data
        df = await self.get_ohlc(timeframe=timeframe)
        sma_size = 200
        # Get the trend of the market by using sma200
        # Get list of 5 last closed price
        price: List[float] = df["Close"][-5:].to_list()
        # calculate sma
        df[f"SMA_{sma_size}"] = df["Close"].rolling(window=sma_size).mean()
        sma_value: List[float] = df[f"SMA_{sma_size}"][-5:].to_list()
        # condition
        cond = price > sma_value
        if cond:
            return Trend.UPTREND
        return Trend.DOWNTREND
    
    async def generate_image(self) -> io.BytesIO:
        self.log.info('generating image')
        data = await self.get_ohlc()
        levels = await self.get_support_and_resistance(s_r=False)
        #print([True for ind in data.index if ind in [l[0] for l in levels]].count(False))
        buf = io.BytesIO()
        mydpi = 100
        kwargs = dict(
            type='candle',
            mav=(50,200),
            volume=True,
            figratio=(16,9),
            figsize =(1280/mydpi,720/mydpi), 
            figscale=0.8,
            savefig=dict(fname=buf,dpi=mydpi),#,pad_inches=1000),
            scale_padding=0.2)

        # levels_plot = mpf.make_addplot(levels,color='#606060')
        
        mpf.plot(data.iloc[:,-10:],**kwargs,style='binance',hlines= levels)
        buf.seek(0)
        return buf
    
    async def __ainit__(self, exchange: Exchange, symbol:str) -> None:
        assert symbol, "symbol name not provided"
        log.info(f'creating {symbol}')
        self.exchange = exchange
        self.symbol = symbol
        await self._generate_data()
        self.log =create_logger(f'cryptopair:{self.symbol}')
        

