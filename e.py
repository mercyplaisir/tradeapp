

import os

api_key= os.environ.get('binance_apikey')
secret_key= os.environ.get('binance_secretkey')

class Keys:
    @classmethod
    def api_key(cls):
        return api_key

    @classmethod
    def secret_key(cls):
        return secret_key
    










