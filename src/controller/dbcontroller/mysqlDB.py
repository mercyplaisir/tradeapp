import mysql.connector




class mysqlDB:
    def __init__(self):
        db = {'host': 'localhost',
                   'user': 'root',
                   'passwd': 'Pl@isir6',
                   'database': 'bot'}
        self.bdConnect(db)
        
    def bdConnect(self,**kwargs):
        try:
            self.mydb = mysql.connector.connect(**kwargs)
            print(">>>connexion au DB effectue")

        except:
            print("BD connection error")

    def requestDB(self,requete):
        mycursor = self.mydb.cursor()
        mycursor.execute(requete)

        
    def selectDB(self,requete):
        mycursor = self.mydb.cursor()
        mycursor.execute(requete)
        return mycursor
    

