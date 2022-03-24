import mysql.connector


class MysqlDB:
    """MySql Database controller"""
    def __init__(self):
        self.db = {'host': 'localhost',
                   'user': 'root',
                   'passwd': 'Pl@isir6',
                   'database': 'tradeapp',#}
                   'auth_plugin':'mysql_native_password'}
        self.connected = False
        self.con = None  # for connection

    def request(self, request:str):
        self._connect()

        mycursor = self.con.cursor()
        mycursor.execute(request)
        mycursor.close()

        self._disconnect()

    def select(self, request:str):
        self._connect()
        if not self.connected:
            raise ValueError("Not Connected")
        cursor = self.con.cursor()
        cursor.execute(request)
        result:tuple = cursor.fetchall()
        cursor.close()

        self._disconnect()
        return result

    def _bdConnect(self, dbinfo: dict):
        self.con = mysql.connector.connect(**dbinfo)
        self.connected = True
        #print(">>>connexion au DB effectue")

        

    def _connect(self):
        self._bdConnect(self.db)
        

    def _disconnect(self):
        if self.connected:
            self.con.close()
            self.connected = False
