"""binance public and private key"""
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

BINANCE_PUBLIC_KEY = os.getenv('BINANCEPUBLICKEY')
BINANCE_PRIVATE_KEY = os.getenv('BINANCEPRIVATEKEY')

BINANCE_PUBLIC_KEY_TEST = 'CGYXsNhqyez6qeamoTGeHDchajN7eiMEFiDWwnMjUTcqbhSLSVv2bf52UM9iMC6e'
BINANCE_PRIVATE_KEY_TEST = 'Xn5AYyAC5F6XUOmpjvn0xPF4xYmqHqp8GhujWiQCeJG3jCbV4Q4YrB6vHnDeDVvs'

# print(BINANCE_PUBLIC_KEY+'\n'+BINANCE_PRIVATE_KEY)