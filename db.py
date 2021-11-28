import sqlite3 as db
import dbcreate


def connectDB():
    connection = db.connect('BarberBotDB.db')
    return connection


def dbstart():  # Попытка подключения к БД, создание таблиц
    try:
        connection = connectDB()
        print("Successfully connected to DB")
        cursor = connection.cursor()
        cursor.execute('SELECT name from sqlite_master where type= "table"')
        tables = cursor.fetchall()

        if not tables:
            dbcreate.createTables()
            cursor.execute('SELECT name from sqlite_master where type= "table"')
            tables = cursor.fetchall()
            print('-' * 20 + "\nTables created:", tables)
        else:
            print('-' * 20 + "\nTables:", tables)

    except Exception as e:
        print("Connect error: ", e)
