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


def insertClient(chatid, username):
    """
    Добавление нового пользователя в БД

    :param chatid: id пользователя
    :param username: username пользователя
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("INSERT INTO Clients (chatid, username) VALUES (" + str(chatid) + ", '" + str(username) + "');")
    cursor.execute(query)
    connection.commit()
    connection.close()


def insertBarber(username):
    """
    Добавление нового барбека

    :param username: username барбера в БД
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("INSERT INTO Barbers (username) VALUES (" + str(username) + ");")
    cursor.execute(query)
    connection.commit()
    connection.close()


def insertOrder(order_time, BarberId):
    """
    Добавление нового заказа в БД

    :param BarberId: id барбера
    :param order_time: время заказа
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("INSERT INTO Orders (order_time, BarberId) VALUES "
             + str(order_time)+", "+ str(BarberId) +");" )
    cursor.execute(query)
    connection.commit()
    connection.close()


def IsNewClient(chatid):
    """
    Проверка является ли пользователь новым

    :param chatid: id пользователя
    :return: 
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("SELECT chatid FROM Clients WHERE chatid = %s;" % chatid)
    cursor.execute(query)
    res = cursor.fetchall()
    connection.close()
    for i in res:
        if chatid == i[0]:
            return False
    return True


def isFreeOrder(order_time, BarberId):
    """
    Проверка - занято ли место

    :param BarberId: id барбера
    :param order_time: время заказа
    :return: True - всободное место
             False - занятое место
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("SELECT count(*) FROM Clients WHERE Clients.BarberId = BarberId and Clients.order_time = order_time and "
             "Clients.chatId != NULL")
    cursor.execute(query)
    res = cursor.fetchall()
    connection.close()
    return res[0] != 1


def takeOrder(chatid, order_time, BarberId):
    """
    Занять место за пользователем с id chatid
    :param chatid: id пользователя
    :return: 1 - success add
             0 - fail add
    """

    if isFreeOrder(order_time, BarberId):
        connection = connectDB()
        cursor = connection.cursor()
        query = "UPDATE Orders SET Orders.chatid = "+ str(chatid) +  "WHERE Orders.order_time = " + \
             str(order_time) + " and Orders.BarberId = " + (BarberId)

        cursor.execute(query)
        connection.commit()
        connection.close()
        return 1

    return 0