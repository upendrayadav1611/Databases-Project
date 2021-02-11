from getpass import getpass
from mysql.connector import connect, Error

def show_table():
    select_chocolates_query = "SELECT * FROM Chocolates"
    with connection.cursor() as cursor:
        cursor.execute(select_chocolates_query)
        result = cursor.fetchall()
        for row in result:
            print(row)

def Delete_Expired_Chocolates():
    Delet_Chocolate_query = "DELETE FROM Chocolates WHERE ExpiryDate<now()"
    print("Running")
    with connection.cursor() as cursor:
        cursor.execute(Delet_Chocolate_query)
        connection.commit()

try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database="Chocolates_Info",
    ) as connection:
        show_table()
        #Delete_Expired_Chocolates()
except Error as e:
    print(e)