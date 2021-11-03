import asyncio
import json
import requests
import time
import datetime
import pandas as pd

cryptos = 'BNBBTC'#, 'ETHUSDT', 'BTCUSDT', 'DOGEUSDT'] * 6
data = {
    # "symbol":'BNBBTC',
    "interval": '15m',
    # "startTime": '1 day ago'
    # "endTime"
    "limit":100
}
main = "https://api.binance.com{}"
klines = "/api/v3/klines"
test = "/api/v3/ping"
results = []


starttime = time.time()



data['symbol']=cryptos
klines_list = requests.get(url=main.format(klines),params=data).json()
for kline in klines_list:
    kline[0] = datetime.datetime.fromtimestamp(kline[0] / 1e3)
    kline[6] = datetime.datetime.fromtimestamp(kline[6] / 1e3)
klines = pd.DataFrame(klines_list)  # changer en dataframe
# supprimer les collonnes qui ne sont pas necessaires
klines.drop(columns=[6, 7, 8, 9, 10, 11], inplace=True)

klines.columns = ['date', 'open', 'high', 'low',
                  'close', 'volume']  # renommer les colonnes

print(time.time() - starttime)
print({cryptos:klines})


# print(cc)

# print(datetime.datetime.strptime('1 day ago'))
