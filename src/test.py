from dbcontroller.mysqlDB import mysqlDB

db =mysqlDB()

req = "select * from relationalcoin"
# req = "show tables"
resp = db.selectDB(req)
print(resp)