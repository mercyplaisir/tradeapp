import io
import mplfinance as mpf
from tools.logs import logger_wrapper

import pandas as pd

@logger_wrapper(__name__,"generating image")
def generate_image(**kwargs) -> io.BytesIO:
        
        df = kwargs['data']
        df = df.set_index('open time')
        #print([True for ind in data.index if ind in [l[0] for l in levels]].count(False))
        df.index = pd.to_datetime(df.index/1000)
        print(df.index)
        buf = io.BytesIO()
        mydpi = 100
        settings = dict(
            data = df    ,
            type='candle',
            mav=(50,200),
            volume=False,
            figratio=(16,9),
            figsize =(1280/mydpi,720/mydpi), 
            figscale=0.8,
            savefig=dict(fname=buf,dpi=mydpi),#,pad_inches=1000),
            scale_padding=0.2)

        # levels_plot = mpf.make_addplot(levels,color='#606060')
        kwargs.update(settings)
        # mpf.plot(data.iloc[:,-10:],**kwargs,style='binance',hlines= levels)
        mpf.plot(**kwargs,style='binance')
        buf.seek(0)
        return buf
