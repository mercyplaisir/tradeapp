import sqlite3
from src.controller.tools import DBSTORAGE


class sqliteDB:
    def requestDB(self,requete):
        con = sqlite3.connect(DBSTORAGE)
        mycursor = con.cursor()


        mycursor.execute(requete)
       
       #Save(commit) changes
        con.commit()
        con.close()
        return True


    def selectDB(self,requete):
        con = sqlite3.connect(DBSTORAGE)
        mycursor = mydb.cursor()

        mycursor.execute(requete)
        resultat = mycursor.fetchall()
        con.close()
        return resultat
