
import pandas as pd
import json

with open('./test.json','r+')as f:
    x=json.load(f)

for i in x:
    if i['coin']:
        print(i['hello'])
