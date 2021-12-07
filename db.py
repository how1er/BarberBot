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
        # clearTable('Orders')
        barbers = Barber_list_price()
        year = datetime.datetime.today().year
        month = datetime.datetime.today().month
        day = datetime.datetime.today().day
        start = datetime.datetime(year, month, day, 8)
        end = datetime.datetime(year, month, day, 18)
        all_data = columnLists('Orders')
        if len(all_data) == 0:
            for day in range(7):
                for barberId, BarberName, Price in barbers:
                    fillOrders(str(barberId), start, end)
                start += datetime.timedelta(days=1)
                end += datetime.timedelta(days=1)


    except Exception as e:
        print("Connect error: ", e)


def db_update():  # Ежедневное добавление заказов
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
        # clearTable('Orders')
        barbers = Barber_list_price()
        year = datetime.datetime.today().year
        month = datetime.datetime.today().month
        day = datetime.datetime.today().day
        start = datetime.datetime(year, month, day, 8) + datetime.timedelta(days=7)
        end = datetime.datetime(year, month, day, 18) + datetime.timedelta(days=7)
        for barberId, BarberName, Price in barbers:
            fillOrders(str(barberId), start, end)


    except Exception as e:
        print("Connect error: ", e)


def insertClient(chatId, username=''):
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


def insertBarber(barberName, price=500):
    """
    Добавление нового барбера

    :param barberName: имя барбера в БД
    :param price: цена за работу
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = ("INSERT INTO Barbers (barberName, price) VALUES ('" + str(barberName) + "', '" + str(price) + "');")
    cursor.execute(query)
    connection.commit()
    connection.close()


def insertOrder(order_time, barberId):
    """
    Добавление нового заказа в БД

    :param barberId: id барбера
    :param order_time: время заказа
    :return:
    """

    connection = connectDB()
    cursor = connection.cursor()
    query = ("INSERT INTO Orders (order_time, barberId) VALUES ('" + str(order_time) + "', '" + str(barberId) + "');")
    cursor.execute(query)
    connection.commit()
    connection.close()


def isNewClient(chatId):
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


def isFreeOrder(order_time, barberId):
    """
    Проверка - занято ли место

    :param BarberId: id барбера
    :param order_time: время заказа
    :return: True - в сободное место
             False - занятое место
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = """SELECT chatId FROM Orders WHERE Orders.order_time = ? and Orders.barberId = ? and chatId IS NULL"""
    params_tuple = (order_time, barberId)
    cursor.execute(query, params_tuple)
    res = cursor.fetchall()
    connection.close()
    return len(res) != 0


def History(chatId):
    """
    Вывод истории заказов

    :param chatId: id пользователя
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = """SELECT barberName, order_time, rating FROM Orders JOIN Barbers USING (barberId) 
    WHERE chatId = ? ORDER BY order_time DESC"""
    cursor.execute(query, (chatId,))
    res = cursor.fetchall()
    connection.close()
    return res


def takeOrder(chatid, order_time, barberId):
    """
    Занять место за пользователем с id chatid, и добавить его в таблицу клиентов, если это новый клиент
    :param chatid: id пользователя
    :return: 1 - success add
             0 - fail add
    """

    if isFreeOrder(order_time, barberId):
        connection = connectDB()
        cursor = connection.cursor()
        query0 = "SELECT orderId, order_time FROM Orders where order_time = ? and barberId = ?"
        data_tuple0 = (order_time, barberId)
        res = cursor.execute(query0, data_tuple0).fetchall()
        res_str = ""
        for orderId, order_time in res:
            res_str = str(orderId)
        connection.commit()
        query = """UPDATE Orders SET chatid = ? where order_time = ? and barberId = ?"""
        data_tuple = (chatid, order_time, barberId)
        cursor.execute(query, data_tuple)
        connection.commit()
        connection.close()
        if isNewClient(chatId=chatid):
            insertClient(chatId=chatid)
        return res_str

    return False


def update_mark(orderId, Mark):
    """
    Занести оценку в бд
    :param orderId: id заказа
    :param Mark: оценка
    :return:
    """

    connection = connectDB()
    cursor = connection.cursor()
    data_tuple = (Mark, orderId)
    query = """UPDATE Orders SET rating = ? where orderId = ?"""
    cursor.execute(query, data_tuple)
    connection.commit()
    connection.close()


def clearTable(table_name):
    """
    Удаляем все строки таблицы table_name
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = """DELETE FROM """ + str(table_name)
    cursor.execute(query)
    connection.commit()
    connection.close()


def columnLists(table_name):
    """
    Посмотреть записи таблицы table_name
    :param: table_name: название таблицы
    :return: list of tables columns
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = """select * from """ + str(table_name)
    res = cursor.execute(query).fetchall()
    for i in res:
        print(i)
    connection.close()
    return res


def Barber_list_price():
    """
    Вывод списка барберов с их ценами
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT barberId, BarberName, Price FROM Barbers"
    cursor.execute(query)
    barbers = cursor.fetchall()
    connection.close()
    return barbers


def Barber_mark(barberId):
    """
    Вывод средней оценки барбера
    :param: table_name: название таблицы
    :return:
    """
    connection = connectDB()
    cursor = connection.cursor()
    query = "SELECT barberId, AVG(rating) FROM Orders WHERE rating <> 0 and barberId = ? GROUP BY barberId"
    cursor.execute(query, (barberId,))
    marks = cursor.fetchall()
    connection.close()
    return marks


def fillOrders(barberId, start, end, step=1):
    """
    Создаёт заказы для барбера с iD = barberId
    :param: barberId: id барбера
    :type: int
    :param start: время начало работы
    :type: datetime.datetime
    :param end: время конца работы
    :type: datetime.datetime
    :param step: время с которым будет ставить заказы, в часах
    :type: datetime.datetime
    :return:
    """
    delta_t = datetime.timedelta(hours=step)
    ordered_time = start
    while ordered_time < end:
        insertOrder(ordered_time, barberId=barberId)
        ordered_time += delta_t


def barberFreeTime(barberId, years_day):
    """
    Возвращает список свободных мест для записи
    :param barberId: id барбера
    :param years_day: день года
    :type: datetime.datetime(year, month, day)
    :return: список времени
    """
    time_start = datetime.datetime(years_day.year, years_day.month, years_day.day, 0, 0)
    time_end = datetime.datetime(years_day.year, years_day.month, years_day.day, 0, 0) + datetime.timedelta(1)

    connection = connectDB()
    cursor = connection.cursor()
    query = """select order_time from Orders where  ? <= order_time and order_time < ? 
                                                        and barberId = ? and chatId is NULL """
    params_tuple = (str(time_start), str(time_end), barberId)
    res = cursor.execute(query, params_tuple).fetchall()
    cursor.close()

    return res
