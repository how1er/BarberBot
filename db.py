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


def Barber_list_price():
    """
    Вывод списка барберов с их ценами
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT BarberName, Price FROM Barbers"
    cursor.execute(query)
    barbers = cursor.fetchall()
    connection.close()
    return barbers


def check_new_client(chatid):
    """
    Проверка является ли пользователь новым
    :param chatid: id пользователя
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("SELECT chatId FROM Clients WHERE chatId = %s;" % chatid)
    cursor.execute(query)
    res = cursor.fetchall()
    connection.close()
    for i in res:
        if chatid == i[0]:
            return False
    return True
