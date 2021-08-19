import sys
sys.path.append(sys.path[0]+'/../..')


from src.controller.dbcontroller import sqliteDB

db = sqliteDB()

resultat = db.selectDB("select * from Coin where Coin.coinName = 'DOGE'")


print(resultat)