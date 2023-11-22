
import sqlite3

__PATH = 'database/library.db'
#__PATH = 'database\library.db'


def getDB():
    db = sqlite3.connect(__PATH)
    return db


def closeConnection(db):
    # ...
    db.close()


def query(sql):
    db = getDB()
    cursor = db.cursor()

    result = cursor.execute(sql)
    result = result.fetchall()
    
    db.commit()
    closeConnection(db)
    return result