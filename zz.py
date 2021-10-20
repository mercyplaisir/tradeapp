import json


class nana:

    @property
    def coin(self):
        with open(f"coin.json",'r') as f:
            self._coin =  json.load(f)
        return self._coin
    @coin.setter
    def coin(self,newvalue):
        with open(f"coin.json",'w') as f:
            newvalue =  json.dumps(newvalue)
            f.write(newvalue)
        self._coin = newvalue

cc = nana()

cc.coin = 'BTC'
print(cc.coin)





