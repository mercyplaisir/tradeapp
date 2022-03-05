from indicators import Study
from base import CryptoPair

cr = CryptoPair('BNBBTC')

print(Study.decision(cr.get_klines()))