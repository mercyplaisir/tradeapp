import sqlite3
from src.controller.tools import DBSTORAGE


class sqliteDB:
    def requestDB(self,requete):
        mydb = sqlite3.connect(DBSTORAGE)
        mycursor = mydb.cursor()

        mycursor.execute(requete)
        
        mydb.close()
        return True


    def selectDB(self,requete):
        mydb = sqlite3.connect(DBSTORAGE)
        mycursor = mydb.cursor()

        mycursor.execute(requete)
        resultat = mycursor.fetchall()
        mydb.close()
        return resultat