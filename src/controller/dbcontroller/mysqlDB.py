import mysql.connector


class mysqlDB:
    def __init__(self):
        self.db = {'host': 'localhost',
                   'user': 'root',
                   'passwd': 'Pl@isir6',
                   'database': 'tradeapp'}
        self.connected = False
        self.con = None  # for connection

    def requestDB(self, requete:str):
        self._connect()

        mycursor = self.con.cursor()
        mycursor.execute(requete)
        mycursor.close()

        self._disconnect()

    def selectDB(self, requete:str):
        self._connect()

        cursor = self.con.cursor()
        cursor.execute(requete)
        result:tuple = cursor.fetchall()
        cursor.close()

        self._disconnect()
        return result

    def _bdConnect(self, dbinfo: dict):
        try:
            self.con = mysql.connector.connect(**dbinfo)
            self.connected = True
            print(">>>connexion au DB effectue")

        except:
            print("BD connection error")

    def _connect(self):
        try:
            self._bdConnect(self.db)
        except Exception as e:
            print(e)

    def _disconnect(self):
        if self.connected:
            self.con.close()
            self.connected = False
