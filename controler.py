from re import S
import sqlite3
from sqlite3 import Error
from flask import g
import random

DB_NAME = 'Database.db'

def connect_db():
    try:
        if 'db' not in g:
            print('conexion a la base de datos')
            g.db = sqlite3.connect(DB_NAME)
        return g.db
    except Error:
        print(Error)

def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()

def add_user(email, name, user, password ):
    code_validation = random.randint(100000, 999999)

    try:
        db = connect_db()
        cursor = db.cursor()
        sql = 'INSERT INTO USERS(NAME, USER, EMAIL, PASSWORD, CODE_VALIDATION, ACCOUNT_VERIFICATE, ROLE) VALUES(?,?,?,?,?,?,?)'
        cursor.execute(sql, [name, user, email, password, code_validation, False, 'user'])
        db.commit()
        return True
    except:
        return False

def validate_user(username):
    try:
        db = connect_db()
        cursor = db.cursor()
        sql = 'SELECT * FROM USERS WHERE USER = ? OR EMAIL = ?'
        cursor.execute(sql, [username, username])
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            print(result)
            usuario = [
                    {
                    'id': result[0],
                    'NAME': result[1],
                    'USER': result[2],
                    'EMAIL': result[3],
                    'PASSWORD': result[4],
                    'CODE_VALIDATION': result[5],
                    'ACCOUNT_VERIFICATION': result[6],
                    'ROLE': result[7]
                    }
                ]
            return usuario
    except Error:
        print(Error)
        return False