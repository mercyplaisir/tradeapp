import json
from base import Coin
from dbcontroller import DbEngine

def get_coin_data():
    """just for view"""
    all_coins = Coin.get_all_coins()

    data: dict = {coin.name: coin.get_cryptopair_related() for coin in all_coins}

    data = {n: [str(l) for l in ll] for n, ll in data.items()}

    nn = json.dumps(data)
    with open("coindata.json", "w") as f:
        f.write(nn)

# SELECT cryptopair FROM relationalcoin WHERE basecoin or quotecoin not in (SELECT shortname from Coin)

def clean_database():
    db = DbEngine()
    requete = "DELETE  FROM relationalcoin WHERE basecoin not in (SELECT shortname from Coin)"
    db.requestDB(requete= requete)

# get_coin_data()