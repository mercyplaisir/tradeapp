import json
import numpy as np
import pandas as pd
from binance.client import Client
import e #contains the api and secret keys


client = Client(e.api_key, e.secret_key)


#get all the info of my  account
info = client.get_account()


# stock all balances in a json file
with open('./my_balances.json','w') as f:
    jsonString = json.dumps(info['balances'], indent= 4)
    f.write(jsonString)








