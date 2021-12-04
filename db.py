import sqlite3 as db
import dbcreate
import datetime

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


def insertClient(chatId, username):
    """
    Добавление нового пользователя в БД

    :param chatid: id пользователя
    :param username: username пользователя
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("INSERT INTO Clients (chatId, username) VALUES (" + str(chatId) + ", '" + str(username) + "');")
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
    query = ('INSERT INTO Barbers (username) VALUES (?);')
    cursor.execute(query,[username])
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
    query = """INSERT INTO 'Orders'
                          ('order_time', 'BarberId')
                          VALUES (?, ?);"""
    data_tuple = (order_time, BarberId)
    cursor.execute(query,data_tuple)
    connection.commit()
    connection.close()


def IsNewClient(chatId):
    """
    Проверка является ли пользователь новым

    :param chatId: id пользователя
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("SELECT chatId FROM Clients WHERE chatId = %s;" % chatId)
    cursor.execute(query)
    res = cursor.fetchall()
    connection.close()
    for i in res:
        if chatId == i[0]:
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
    query = ("SELECT count(*) FROM Orders WHERE Orders.BarberId = BarberId and Orders.order_time = order_time and "
             "Orders.chatId != NULL")
    cursor.execute(query)
    res = cursor.fetchall()
    connection.close()
    return res[0][0] != 1


def takeOrder(chatid, order_time, barberId):
    """
    Занять место за пользователем с id chatid
    :param chatid: id пользователя
    :return: 1 - success add
             0 - fail add
    """

    if isFreeOrder(order_time, barberId):
        connection = connectDB()
        cursor = connection.cursor()

        #query = "UPDATE Orders SET chatid = "+ str(chatid) +  " WHERE order_time = " + \
       #      str(order_time) + " and BarberId = " + str(BarberId) + ""
        query = """UPDATE Orders SET chatid = ? where order_time = ? and barberId = ?"""
        data_tuple = (chatid, order_time,barberId)
        cursor.execute(query, data_tuple)
        connection.commit()
        connection.close()
        return True

    return False


def clearBarbers():
    """
    Удаляем все строки таблицы Barbers
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("DELETE FROM Barbers")
    cursor.execute(query)
    connection.commit()
    connection.close()


def clearOrders():
    """
    Удаляем все строки таблицы Orders
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("DELETE FROM Orders")
    cursor.execute(query)
    connection.commit()
    connection.close()


def clearClients():
    """
    Удаляем все строки таблицы Clients
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("DELETE FROM Clients")
    cursor.execute(query)
    connection.commit()
    connection.close()



a = "fsdfds"
dt = datetime.datetime(2017, 3, 5, 12, 30, 10)
#insertOrder(dt,100)
print(connectDB().execute("select * from Clients").fetchall())
print(connectDB().execute("select * from Barbers").fetchall())
print(connectDB().execute("select * from Orders").fetchall())
print(isFreeOrder(dt,100))
print(takeOrder(999,dt,100))
print(isFreeOrder(dt,100))
print(connectDB().execute("select * from Orders").fetchall())
#clearOrders()
#print(connectDB().execute("select * from Orders").fetchall())
