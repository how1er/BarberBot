import sqlite3 as db


def createTables():

    connection = db.connect("BarberBotDB.db")
    cursor = connection.cursor()
    query = ("""
            CREATE TABLE Clients(
            chatId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            username VARCHAR(32) NOT NULL
            );
            """)
    cursor.execute(query)
    connection.commit()

    query = ("""    
    CREATE TABLE Barbers(
        BarberId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username VARCHAR(32) NOT NULL,
        min_price int NOT NULL DEFAULT 0,
        Rating int DEFAULT 0
    );
    """)
    cursor.execute(query)
    connection.commit()

    query = ("""    
        CREATE TABLE Orders(
            OrderId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            order_time datetime NOT NULL,
            chatId int DEFAULT NULL,
            barberId int NOT NULL,
            Price int NOT NULL DEFAULT 0,
            FOREIGN KEY(chatId) REFERENCES Clients(chatId),
            FOREIGN KEY(barberId) REFERENCES Barbers(barberId)
        );
        """)
    cursor.execute(query)
    connection.commit()
