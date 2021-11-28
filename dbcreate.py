import sqlite3 as db


def createTables():

    connection = db.connect("BarberBotDB.db")
    cursor = connection.cursor()
    query = ("""
            CREATE TABLE Clients(
            chatId int PRIMARY KEY,
            username VARCHAR(32) NOT NULL
            );
            """)
    cursor.execute(query)
    connection.commit()
    query = ("""    
    CREATE TABLE Barbers(
        BarberId INTEGER PRIMARY KEY AUTOINCREMENT,
        Price int NOT NULL,
        Rating int NOT NULL,
        OrderCount int NOT NULL
    );
    """)
    cursor.execute(query)
    connection.commit()

    query = ("""    
        CREATE TABLE Orders(
            OrderId INTEGER PRIMARY KEY AUTOINCREMENT,
            chatId int NOT NULL,
            barberId int NOT NULL,
            Price int NOT NULL,
            FOREIGN KEY(chatId) REFERENCES Clients(chatId)
            FOREIGN KEY(barberId) REFERENCES Barbers(barberId)
        );
        """)
    cursor.execute(query)
    connection.commit()
