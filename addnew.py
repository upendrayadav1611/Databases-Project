from getpass import getpass
from mysql.connector import connect, Error
from datetime import date

def show_database():
    show_db_query = "SHOW DATABASES"
    with connection.cursor() as cursor:
        cursor.execute(show_db_query)
        for db in cursor:
            print(db)

def update_Chocolates_table(ChocolateId, ChocolateName, Quantity, LastStockUpdate, LastDateBought, ExpiryDate, NegativeReviewsCount, PositiveReviewsCount):
    insert_Chocolates_query = """
    INSERT INTO Chocolates(ChocolateId, ChocolateName, Quantity, LastStockUpdate, LastDateBought, ExpiryDate, NegativeReviewsCount, PositiveReviewsCount)
    VALUES
        ("%d","%s","%d","%s","%s","%s","%d","%d")
    """ % (ChocolateId, ChocolateName, Quantity, LastStockUpdate, LastDateBought, ExpiryDate, NegativeReviewsCount, PositiveReviewsCount)
    
    with connection.cursor() as cursor:
        cursor.execute(insert_Chocolates_query)
        connection.commit()

def update_Ingredients_table(Ingredients, id):
    for ingredient in Ingredients:
        print(ingredient)
        insert_Ingredients_query = """
        INSERT INTO Ingredients(IngredientName, ChocolateId)
        VALUES
            ("%s","%d")
        """ % (ingredient, int(id))
    
        with connection.cursor() as cursor:
            cursor.execute(insert_Ingredients_query)
            connection.commit()

def get_id():
    id_file = open('id_file.txt', 'r')
    id = id_file.read()
    print("Id successfully retrieved")
    print(id)
    id_file.close()
    return id
    
def update_id(id):
    id_file = open('id_file.txt','w')
    id_file.write(str(id))
    print("Id successfully updated")
    id_file.close()

def add_new_entry():
    ChocolateName = input("Enter chocolate name: ")
    id = get_id()
    ChocolateId = int(id)
    Quantity = int(input("Enter quantity: "))
    if Quantity < 1:
        print("Enter at least one chocolate")
        exit(0)
    LastStockUpdate = date.today()
    LastDateBought = date.today()
    ExpiryDate = input("Enter expiry date: ")
    NegativeReviewsCount = 0
    PositiveReviewsCount = 0 
    Ingredients = []
    IngredientCount = int(input("Enter count of ingredients: "))
    for count in range(IngredientCount):
        print("Enter IngredientName ")
        IngredientName = input()
        Ingredients.append(IngredientName)
     
    for ingredient in Ingredients:
        print(ingredient)
    update_Chocolates_table(ChocolateId, ChocolateName, Quantity, LastStockUpdate, LastDateBought, ExpiryDate, NegativeReviewsCount, PositiveReviewsCount)
    update_Ingredients_table(Ingredients, id)
    id = int(id)
    update_id(id+1)
    
def create_file():
    id_file = open('id_file.txt','w')
    id_file.write('2')
    id_file.close()

def show_Chocolates():
    show_table_query = "SELECT * FROM Chocolates"
    with connection.cursor() as cursor:
     cursor.execute(show_table_query)
     # Fetch rows from last executed query
     result = cursor.fetchall()
     for row in result:
         print(row)

def show_Ingredients():
    show_table_query = "SELECT * FROM Ingredients"
    with connection.cursor() as cursor:
     cursor.execute(show_table_query)
     # Fetch rows from last executed query
     result = cursor.fetchall()
     for row in result:
         print(row)

def reset():
    delete_query_2 = "DELETE FROM Ingredients"
    delete_query_1 = "DELETE FROM Chocolates"
    delete_query_3 = "DELETE FROM Reviews"
    with connection.cursor() as cursor:
        cursor.execute(delete_query_1)
        cursor.execute(delete_query_2)
        cursor.execute(delete_query_3)
        connection.commit()
    create_file()


def delete_ingredient_Chocolates_query(ids_to_delete):
    print("Gonna delete in delete_ingredient_Chocolates_query")
    for ids in ids_to_delete: 
        delete_query = """
        DELETE FROM Chocolates where ChocolateId = "%d"
        """ % (ids)
        with connection.cursor() as cursor:
            cursor.execute(delete_query)
            connection.commit()
    print("Successfully deleted :)")
    show_Chocolates()
    show_Ingredients()


def delete_ingredient_query(ingredient):
    select_ingredient_query = """
    SELECT * FROM Ingredients
    WHERE IngredientName = "%s"
    """ % (ingredient)
    with connection.cursor() as cursor:
        cursor.execute(select_ingredient_query)
        result = cursor.fetchall()
        ids_to_delete = []
        for res in result:
            print(res[1])
            ids_to_delete.append(res[1])
            print(res)
    response = input("Are you sure you want to delete this ingredient (y/n): ")
    if(response == "y"):
        print("Gonna delete in delete_ingredient_query")
        for ids in ids_to_delete:
            delete_query = """
            DELETE FROM Ingredients where ChocolateId = "%d"
            """ % (ids)
            with connection.cursor() as cursor:
                cursor.execute(delete_query)
                connection.commit()
        print("Successfully deleted :)")
        delete_ingredient_Chocolates_query(ids_to_delete)
        show_Chocolates()
        show_Ingredients()




def delete_ingredient():
    ingredient = input("Enter ingredient to delete: ")
    delete_ingredient_query(ingredient)

try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database="Chocolates_Info",
    ) as connection:
        #reset()
        #create_file()
        show_Chocolates()
        show_Ingredients()
        #add_new_entry()
        delete_ingredient()
        show_Chocolates()
        show_Ingredients()
except Error as e:
    print(e)