import sqlite3

DBSTORAGE: str = f'./appDB.db'


class SqliteDB:

    def requestDB(self, requete):
        con = sqlite3.connect(DBSTORAGE)
        mycursor = con.cursor()


        mycursor.execute(requete)

        # Save(commit) changes
        con.commit()
        con.close()
        return True

    def selectDB(self, requete):
        con = sqlite3.connect(DBSTORAGE)
        mycursor = con.cursor()

        mycursor.execute(requete)
        resultat = mycursor.fetchall()
        con.close()
        return resultat


if __name__=='__main__':
    con = SqliteDB()
    res = con.selectDB("select * from Coin")
    print(res)
