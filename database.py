
import sqlite3

__PATH = 'database/library.db'
#__PATH = 'database\library.db'


def getDB():
    db = sqlite3.connect(__PATH)
    return db


def closeConnection(db):
    # ...
    db.close()


def query(sql, params=None):
    try:
        db = getDB()
        cursor = db.cursor()

        if params:
            result = cursor.execute(sql, params)
        else:
            result = cursor.execute(sql)
        
        result = result.fetchall()
        
        db.commit()
        closeConnection(db)
        return result
    except Exception as e:
        print(f"DB ERROR: {e}")
    finally:
        closeConnection(db)