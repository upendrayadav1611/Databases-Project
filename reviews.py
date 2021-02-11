from textblob import TextBlob
from getpass import getpass
from mysql.connector import connect, Error
from datetime import date

def show_database():
    show_db_query = "SHOW DATABASES"
    with connection.cursor() as cursor:
        cursor.execute(show_db_query)
        for db in cursor:
            print(db)

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

def show_Reviews():
    show_table_query = "SELECT * FROM Reviews"
    with connection.cursor() as cursor:
     cursor.execute(show_table_query)
     result = cursor.fetchall()
     for row in result:
         print(row)

def reset():
    delete_query_2 = "DELETE FROM Ingredients"
    delete_query_1 = "DELETE FROM Chocolates"
    with connection.cursor() as cursor:
        cursor.execute(delete_query_1)
        cursor.execute(delete_query_2)
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

def update_Reviews_table(ChocolateId, Review):
    if TextBlob(Review).sentiment.polarity > 0:
        Sentiment = 1
    else:
        if TextBlob(Review).sentiment.polarity == 0:
            Sentiment = 0
        else:
            Sentiment = -1
    insert_Reviews_query = """
    INSERT INTO Reviews(ChocolateId, Review, Sentiment)
    VALUES
        ("%d","%s","%d")
    """ % (int(ChocolateId), Review, int(Sentiment))
    
    with connection.cursor() as cursor:
        cursor.execute(insert_Reviews_query)
        connection.commit()

def update_Chocolates_table(ChocolateId, Review):
    show_table_query = """
    SELECT NegativeReviewsCount,PositiveReviewsCount 
    FROM Chocolates
    WHERE ChocolateId = "%d"
    """ % (int(ChocolateId))
    negative_review_count = 1
    positive_review_count = 1
    with connection.cursor() as cursor:
     cursor.execute(show_table_query)
     result = cursor.fetchall()
     print(result)
     for res in result:
        negative_review_count = res[0]
        positive_review_count = res[1]
    if TextBlob(Review).sentiment.polarity > 0:
        review = 1
        positive_review_count = positive_review_count + 1
        update_Chocolates_table_query = """
        UPDATE Chocolates
        SET PositiveReviewsCount = "%d"
        WHERE ChocolateId = "%d"
        """ % (positive_review_count,int(ChocolateId))
        with connection.cursor() as cursor:
            cursor.execute(update_Chocolates_table_query)
            connection.commit()
    elif TextBlob(Review).sentiment.polarity < 0: 
        review = -1
        negative_review_count = negative_review_count + 1
        update_Chocolates_table_query = """
        UPDATE Chocolates
        SET NegativeReviewsCount = "%d"
        WHERE ChocolateId = "%d"
        """ % (negative_review_count, ChocolateId)
        with connection.cursor() as cursor:
            cursor.execute(update_Chocolates_table_query)
            connection.commit()
    if positive_review_count + negative_review_count > 11:
        if positive_review_count == 0:
            return 1000
        else: 
            return negative_review_count/positive_review_count
    else: 
        return 0

def delete_review_table(ChocolateId):
    delete_query = """
    DELETE FROM Reviews where ChocolateId = "%d"
    """ % (ChocolateId)
    with connection.cursor() as cursor:
        cursor.execute(delete_query)
        connection.commit()

def delete_review_Ingredients(ChocolateId):
    delete_query = """
    DELETE FROM Ingredients where ChocolateId = "%d"
    """ % (ChocolateId)
    with connection.cursor() as cursor:
        cursor.execute(delete_query)
        connection.commit()

def delete_review_Chocolates(ChocolateId):
    delete_query = """
    DELETE FROM Chocolates where ChocolateId = "%d"
    """ % (ChocolateId)
    with connection.cursor() as cursor:
        cursor.execute(delete_query)
        connection.commit()

def add_review():
    ChocolateId = int(input("Enter the ChocolateId: "))
    Review = input("Enter the review: ")
    update_Reviews_table(ChocolateId, Review)
    ratio = update_Chocolates_table(ChocolateId, Review)
    if ratio > 10:
        delete_review_table(ChocolateId)
        delete_review_Ingredients(ChocolateId)
        delete_review_Chocolates(ChocolateId)

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
        add_review()
        show_Chocolates()
        show_Ingredients()
        show_Reviews()
except Error as e:
    print(e)