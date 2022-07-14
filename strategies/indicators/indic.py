import pandas as pd
import btalib



def rsi( klines: pd.DataFrame , periode: int = 14)->pd.DataFrame:
    """create RSI indicator
    return: columns = ["rsi"] 
    """
    rsiInd = btalib.rsi(klines.copy(), period=periode)
    # rsiInd.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier
    return rsiInd.df

def sma(klines: pd.DataFrame, periode: int = 20 )->pd.DataFrame:
    """create SMA indicator
    return: columns = ["sma{period}"] 
    """
    sma = btalib.sma(klines.copy(), period=periode)
    sma.df.columns = [f"sma{periode}"]
    return sma.df

def bb( klines: pd.DataFrame, periode: int = 30 )->pd.DataFrame:
    """create BOLLINGER BANDS indicator
    return: columns = ["mid","top","bot"]
    """
    bb = btalib.bbands(klines, period=periode, devs=2.0)
    # bb.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier
    return bb.df

def macd( klines: pd.DataFrame )->pd.DataFrame:
    """create BOLLINGER BANDS indicator
    return: columns = ["macd","signal","histogram"]
    """
    macd = btalib.macd(klines.copy())

    return macd.df

def stochastic( klines: pd.DataFrame )->pd.DataFrame:
    """create STOCHASTIC indicator
    return: columns = ["k","d"]
    """
    stoch = btalib.stochastic(klines.copy())
    # stoch.df.to_csv(f"{KLINEPATH}", index=True, na_rep=0)  # enregistrer dans le fichier
    return stoch.df
