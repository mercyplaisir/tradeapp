"""Personnalized error"""



class CryptoPairDoesNotExist(Exception):
    """if the cryptopair not found in the databse"""
    
    
class CoinNotFound(Exception):
    """if the coin not found in the database"""