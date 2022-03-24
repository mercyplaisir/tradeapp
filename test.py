from base import CryptoPair
from exchanges import BinanceClient
import json

def get_cryptopair():

    with open('base/utils.json','r') as f:
        data = json.load(f)
        last_cryptopair_traded = data['tracked']['cryptopair']
        return CryptoPair(last_cryptopair_traded)
with BinanceClient() as client:
    cr = get_cryptopair()
    client.pass_order(cr,'sell')   
    print()
    #client._order_quantity()
    #('')
