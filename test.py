
from src.dbcontroller.mysqlDB import mysqlDB
from src.platforms.binance import Coin
# from  src.platforms.binance.elee import Coin

# # db =mysqlDB()

# req = "select * from relationalcoin"
# # req = "show tables"
# resp = db.selectDB(req)
# print(resp)

coin = Coin('BTC')

print(coin)

