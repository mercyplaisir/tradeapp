"""binance public and private key"""
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

BINANCE_PUBLIC_KEY = os.getenv('BINANCEPUBLICKEY')
BINANCE_PRIVATE_KEY = os.getenv('BINANCEPRIVATEKEY')

# print(BINANCE_PUBLIC_KEY+'\n'+BINANCE_PRIVATE_KEY)