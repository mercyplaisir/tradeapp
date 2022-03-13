import sys
from base import Coin

name = sys.argv[1]
coin = Coin(name)
cryptopair_related: list = coin.get_cryptopair_related()

cryptopair_decision_uncleaned = {
                cryptopair: cryptopair.decision() for cryptopair in cryptopair_related
            }

print(cryptopair_decision_uncleaned)