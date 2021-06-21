import json
from tools import FILESTORAGE, Tool as tl


FILEPATH = "virtualaccount.json"


class VirtualAccount:

    def __init__(self):
        dict = tl.read_json(FILEPATH)

        self.usd_balance = dict["usd_balance"]
        #self.btc_amount = 0
        self.btc_balance = dict["btc_balance"]
        #self.btc_price = 0
        #self.bought_btc_at = 0
        #self.last_transaction_was_sell = False;

    
