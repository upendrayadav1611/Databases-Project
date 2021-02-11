from getpass import getpass
from mysql.connector import connect, Error

def show_table():
    select_chocolates_query = "SELECT * FROM Chocolates"
    with connection.cursor() as cursor:
        cursor.execute(select_chocolates_query)
        result = cursor.fetchall()
        for row in result:
            print(row)

def delete_from_Chocolates(chocolateid):
    Delet_Chocolate_query = """
    DELETE  FROM Chocolates
    WHERE ChocolateId = "%d"
    """ % (int(chocolateid))
    print("Running")
    with connection.cursor() as cursor:
        cursor.execute(Delet_Chocolate_query)
        connection.commit()

def delete_from_Ingredients(chocolateid):
    Delet_Chocolate_query = """
    DELETE  FROM Ingredients
    WHERE ChocolateId = "%d"
    """ % (int(chocolateid))
    print("Running")
    with connection.cursor() as cursor:
        cursor.execute(Delet_Chocolate_query)
        connection.commit()

def delete_from_Reviews(chocolateid):
    Delet_Chocolate_query = """
    DELETE  FROM Reviews
    WHERE ChocolateId = "%d"
    """ % (int(chocolateid))
    print("Running")
    with connection.cursor() as cursor:
        cursor.execute(Delet_Chocolate_query)
        connection.commit()

def Delete_Expired_Chocolates():
    Get_expired_chocolateId= "SELECT ChocolateID from Chocolates WHERE ExpiryDate<=now() + INTERVAL 1 DAY"
    with connection.cursor() as cursor:
        cursor.execute(Get_expired_chocolateId)
        result = cursor.fetchall()
        for res in result:
            delete_from_Ingredients(res[0])
            delete_from_Chocolates(res[0])
            delete_from_Reviews(res[0])

def Deletion_basedon_lastDateBought():
    Get_date= "SELECT ChocolateID from Chocolates WHERE LastDateBought<=now() - INTERVAL 1 YEAR"
    with connection.cursor() as cursor:
        cursor.execute(Get_date)
        result = cursor.fetchall()
        for res in result:
            delete_from_Ingredients(res[0])
            delete_from_Chocolates(res[0])
            delete_from_Reviews(res[0])

try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database="Chocolates_Info",
    ) as connection:
        #show_table()
        Delete_Expired_Chocolates()
        Deletion_basedon_lastDateBought()
        Deletion_basedon_lastStockUpdate()
except Error as e:
    print(e)