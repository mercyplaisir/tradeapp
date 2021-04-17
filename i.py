import Coinpaprika

import json

not_connected = True
while not_connected:
    try:
        api_client = Coinpaprika.Client()
        print("connected")
        not_connected = False
    except:
        print('not connected\nwait a second')

all_coins = api_client.coins()
coins = []
for all_coin in all_coins:
    
    coins.append(all_coin['id'])
print('la liste des crypto est pret')


a = []
for coin in coins:
    not_recupered = True
    while not_recupered:
        todays_OHLC = api_client.coins.today_OHLC(coin_id=coin)
        not_recupered = False
    
    for ii in todays_OHLC:
        ii.pop('time_open')
        ii.pop('time_close')
        ii.pop('volume')
        ii.pop('market_cap')
        ii.pop('high')
        ii.pop('low')
        x = ii['open']
        y= ii['close']
        ii['price change']= float(str(((y-x)/x)*100)[:4] )
        ii['coin_id']= coin
        a.append(ii)

print("info recuperer")
with open('./change.json','x') as f:
    jsonf=json.dumps(a, indent = 4)
    f.write(jsonf)