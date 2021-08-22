import mysql.connector




class mysqlDB:
    def __init__(self):
        self.db = {'host': 'localhost',
                   'user': 'root',
                   'passwd': 'Pl@isir6',
                   'database': 'bot'}
        self.connected = True

        
        
    def _bdConnect(self,**kwargs):
        try:
            self.con = mysql.connector.connect(**kwargs)
            print(">>>connexion au DB effectue")

        except:
            print("BD connection error")
    
    def _connect(self):
        self.bdConnect(self.db)
    def _disconnect(self):
        if self.connected:
            self.con.close()
        

    def requestDB(self,requete):
        self._connect()

        mycursor = self.con.cursor()
        mycursor.execute(requete)
        mycursor.close()
        
        self._disconnect()

        
    def selectDB(self,requete):
        self._connect()
        
        cursor = self.con.cursor()
        cursor.execute(requete)
        result = cursor
        cursor.close()

        self._disconnect()
        return result
    

