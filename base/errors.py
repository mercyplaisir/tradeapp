"""Personnalized error"""



class CryptoPairDoesNotExist(Exception):
    def __init__(self,message) -> None:
        self.message = message

    def __str__(self) -> str:
        return 'CryptoPairDoesNotExist: %s' %self.message