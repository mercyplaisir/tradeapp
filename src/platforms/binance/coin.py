"""Representation of a Coin"""

from dataclasses import dataclass, field


from src.dbcontroller.mysqlDB import mysqlDB
from src.platforms.binance.crypto import CryptoPair

@dataclass
class Coin(object):
    """
    Representation of a Coin
    """
    name: str
    database: mysqlDB = field(repr=False, init=False, default_factory=mysqlDB)

    def __post_init__(self):
        nn = self.database.selectDB("select fullname from Coin where shortname='" + self.name + "'")
        if len(nn) == 0:
            raise ValueError('the coin doens\'t exist in the database')

    @property
    def fullname(self):
        return self.database.selectDB("select fullname from Coin where shortname='" + self.name + "'")[0][0]

    def get_cryptopair_related(self) -> list[CryptoPair]:
        """ return all coins related quotecoins or basecoin"""
        coin_name = self.name

        quotecoin_shortnames: list[tuple[str]] = self.database.selectDB(
            "select quotecoin from relationalcoin where basecoin ='" + coin_name + "'")

        quotecoins: list[CryptoPair] = [CryptoPair(name[0] + coin_name) for name in quotecoin_shortnames]

        basecoin_shortname: list[tuple[str]] = self.database.selectDB(
            "select basecoin from relationalcoin where quotecoin ='" + coin_name + "'")

        basecoins: list[CryptoPair] = [CryptoPair(name[0] + coin_name) for name in basecoin_shortname]
        # return {'quotecoins': quotecoins, 'basecoins': basecoins}
        return basecoins + quotecoins

    def __str__(self):
        return f"{self.name}({self.fullname})"


if __name__ == '__main__':
    c = Coin("BTC")
    print(c.get_cryptopair_related())
