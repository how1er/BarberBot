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
        barberId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        barberName VARCHAR(32) NOT NULL,
        price int NOT NULL DEFAULT 0,
        rating int DEFAULT 0
    );
    """)
    cursor.execute(query)
    connection.commit()

    query = ("""    
        CREATE TABLE Orders(
            orderId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            order_time datetime NOT NULL,
            chatId int DEFAULT NULL,
            barberId int NOT NULL,
            FOREIGN KEY(chatId) REFERENCES Clients(chatId),
            FOREIGN KEY(barberId) REFERENCES Barbers(barberId)
        );
        """)
    cursor.execute(query)
    connection.commit()

    query = ("""    
            INSERT INTO Barbers (BarberName, Price) VALUES ("Андрей", '900'), \
            ("Артем", '1000'), ("Азамат", '800');
            """)
    cursor.execute(query)
    connection.commit()