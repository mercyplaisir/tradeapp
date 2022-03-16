from exchanges import BinanceClient
from base import CryptoPair
#run file

with BinanceClient(testnet=True) as client:
    client.run()
