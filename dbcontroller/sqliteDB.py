import sqlite3
from pathlib import Path
from typing import Any, List, Tuple, Union

#db file
DB_STORAGE: str = str(Path('dbcontroller/appDB.db').resolve())


class SqliteDB:

    def request(self, request:str ):
        """for sending a request to the database 
        specially for request : DELETE,UPDATE,INSERT"""
        con = sqlite3.connect(DB_STORAGE)
        cursor = con.cursor()


        cursor.execute(request)

        # Save(commit) changes
        con.commit()
        con.close()
        return True

    def select(self, request:str )->Union[List,Any]:
        """for selecting in the database
        specially for request : SELECT"""
        con = sqlite3.connect(DB_STORAGE)
        cursor = con.cursor()

        cursor.execute(request)
        result = cursor.fetchall()
        con.close()
        return result


