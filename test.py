import json
from base.cryptopair import Coin
from dbcontroller import DbEngine

def get_coin_data():
    """just for view"""
    all_coins = Coin.get_all_coins()

    data: dict = {coin.name: coin.get_cryptopair_related() for coin in all_coins}

    data = {n: [str(l) for l in ll] for n, ll in data.items()}

    nn = json.dumps(data)
    with open("coindata.json", "w") as f:
        f.write(nn)


get_coin_data()