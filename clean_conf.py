import requests

url = "http://localhost:5000/tradeapp/all"

data = {'errors':{'type':'','value':''}}
r=requests.post(url,data=data)