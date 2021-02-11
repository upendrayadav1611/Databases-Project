from getpass import getpass
from mysql.connector import connect, Error

def show_database():
    show_db_query = "SHOW DATABASES"
    with connection.cursor() as cursor:
        cursor.execute(show_db_query)
        for db in cursor:
            print(db)

def create_database():
    create_db_query = "CREATE DATABASE Chocolates_Info"
    with connection.cursor() as cursor:
        cursor.execute(create_db_query)

def create_chocolate_table():
    create_chocolate_table_query = """
    CREATE TABLE Chocolates(
        ChocolateId INT  PRIMARY KEY,
        ChocolateName VARCHAR(100),
        Quantity INT,
        LastStockUpdate DATE,
        LastDateBought DATE,
        ExpiryDate DATE,
        NegativeReviewsCount INT,
        PositiveReviewsCount INT
    )
    """
    with connection.cursor() as cursor:
        cursor.execute(create_chocolate_table_query)
        connection.commit()
try:
    with connect(
        host="localhost",
        user="",
        password="",
        database="Chocolates_Info",
    ) as connection:
        #show_database()
        #create_database()
        create_chocolate_table()
except Error as e:
    print(e)