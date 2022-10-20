from re import S
import sqlite3
import random

DB_NAME = 'Database.db'

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    return conn

def add_user(email, name, user, password ):
    code_validation = random.randint(100000, 999999)

    try:
        db = connect_db()
        cursor = db.cursor()
        sql = 'INSERT INTO USERS(NAME, USER, EMAIL, PASSWORD, CODE_VALIDATION, ACCOUNT_VERIFICATE, ROLE) VALUES(?,?,?,?,?,?,?)'
        cursor.execute(sql, name, user, email, password, code_validation, False, 'user')
        db.commit()
        return True
    except:
        return False