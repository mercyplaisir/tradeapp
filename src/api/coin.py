"""Representation of a Coin"""

from dataclasses import dataclass, field

from src.controller.dbcontroller.mysqlDB import mysqlDB


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

    def getcoinsrelated(self) -> dict[str, list]:
        """ return all coins related quotecoins or basecoin"""
        coin = self.name

        quotecoin_shortnames: list[list[str]] = self.database.selectDB("select quotecoin from relationalcoin" + ""
                                                                       + " where basecoin ='" + coin + "'")
        quotecoins: list[str] = [coin+Coin(name[0]).name for name in quotecoin_shortnames]

        basecoin_shortname: list[list[str]] = self.database.selectDB(
            "select basecoin from relationalcoin where quotecoin ='" + coin + "'")

        basecoins: list[str] = [Coin(name[0]).name+coin for name in basecoin_shortname]
        # return {'quotecoins': quotecoins, 'basecoins': basecoins}
        return basecoins + quotecoins

    def __str__(self):
        return f"{self.name}({self.fullname})"

if __name__ == '__main__':

    c = Coin("BTC")
    print(c.getcoinsrelated())
