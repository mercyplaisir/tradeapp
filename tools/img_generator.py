import io
import mplfinance as mpf
from tools.logs import logger_wrapper

import pandas as pd

@logger_wrapper(__name__,"generating image")
def generate_image(**kwargs) -> io.BytesIO:
        
        df = kwargs['data']
        df = df.set_index('open time')
        #print([True for ind in data.index if ind in [l[0] for l in levels]].count(False))
        df.index = pd.to_datetime(df.index)
        # print(df.index)
        # Prepare support/resistance horizontal lines (hlines) for mplfinance
        # Accept formats:
        # - kwargs['levels'] = [ (price, 'support'|'resistance'), ... ] or [ {'price':p,'type':'support'}, ... ]
        # - kwargs['supports'] = [p1, p2, ...]
        # - kwargs['resistances'] = [p1, p2, ...]
        levels = kwargs.pop('levels', None)
        supports = kwargs.pop('supports', None)
        resistances = kwargs.pop('resistances', None)

        hlines = None
        if levels:
            prices = []
            colors = []
            for lvl in levels:
                # support for dict or tuple/list or plain number
                if isinstance(lvl, dict):
                    price = lvl.get('price') or lvl.get('level')
                    ltype = lvl.get('type', '')
                elif isinstance(lvl, (list, tuple)) and len(lvl) >= 2:
                    price, ltype = lvl[0], lvl[1]
                else:
                    price = lvl
                    ltype = ''

                prices.append(price)
                lt = str(ltype).lower()
                if lt.startswith('s'):
                    colors.append('#00aa00')  # green for support
                elif lt.startswith('r'):
                    colors.append('#ff3333')  # red for resistance
                else:
                    colors.append('#606060')  # default grey

            hlines = dict(hlines=prices, colors=colors, linewidths=1, linestyle='--', alpha=0.8)
        elif supports or resistances:
            prices = []
            colors = []
            for p in (supports or []):
                prices.append(p); colors.append('#00aa00')
            for p in (resistances or []):
                prices.append(p); colors.append('#ff3333')
            if prices:
                hlines = dict(hlines=prices, colors=colors, linewidths=1, linestyle='--', alpha=0.8)

        buf = io.BytesIO()
        mydpi = 100
        settings = dict(
            data = df    ,
            type='candle',
            mav=(50,200),
            volume=False,
            figratio=(16,9),
            figsize =(1920/mydpi,1080/mydpi), 
            figscale=0.8,
            savefig=dict(fname=buf,dpi=mydpi),#,pad_inches=1000),
            scale_padding=0.2)

        # levels_plot = mpf.make_addplot(levels,color='#606060')
        kwargs.update(settings)
        # attach hlines (if any) and plot
        if hlines:
            kwargs.update({'hlines': hlines})
        mpf.plot(**kwargs,style='binance')
        buf.seek(0)
        return buf
