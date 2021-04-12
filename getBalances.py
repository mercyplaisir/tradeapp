import json
import numpy as np
import pandas as pd
from binance.client import Client
import e #contains the api and secret keys


#boucle pour se connecter
disconnected = True
while disconnected:
    try :
        client = Client(e.api_key, e.secret_key)
        print("vous etes connecter")
        disconnected = False
        connected = True
    except:
        print("impossible de se connecter\nveuillez patientez")

#boucle pour recuperer les infos        
get_info_error = True
while get_info_error:
    #get all the info of my  account
    try:

        info = client.get_account()
        print('info recuperer')
        get_info_error = False
        get_info = True
    except:
        print('impossible de recuperer les infos')


#create a dataframe that store and study the balances
balance_dataframe= pd.DataFrame(info['balances'])


#sort the portfolio by the quantity
balance_dataframe.sort_values('free',ascending= False, inplace= True)
print('balance is read')

