from getpass import getpass
from mysql.connector import connect, Error
import smtplib

def send_email(chocolateid,message):
    body = message+"\n"
    for x in chocolateid:
        body=body+x+"\n"
    
    subject="Following chocolates in your database needs attention"
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login("dbprojectcs322@gmail.com","")
        msg=f'Subject:{subject}\n\n{body}'
        smtp.sendmail('dbprojectcs322@gmail.com','dbprojectcs322@gmail.com',msg)
        

def show_table():
    select_chocolates_query = "SELECT * FROM Chocolates"
    cursor = connection.cursor() 
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
    cursor = connection.cursor() 
    cursor.execute(Delet_Chocolate_query)
    connection.commit()

def delete_from_Ingredients(chocolateid):
    Delet_Chocolate_query = """
    DELETE  FROM Ingredients
    WHERE ChocolateId = "%d"
    """ % (int(chocolateid))
    print("Running")
    cursor = connection.cursor() 
    cursor.execute(Delet_Chocolate_query)
    connection.commit()

def delete_from_Reviews(chocolateid):
    Delet_Chocolate_query = """
    DELETE  FROM Reviews
    WHERE ChocolateId = "%d"
    """ % (int(chocolateid))
    print("Running")
    cursor = connection.cursor() 
    cursor.execute(Delet_Chocolate_query)
    connection.commit()

def Delete_Expired_Chocolates():
    Get_expired_chocolateId= "SELECT ChocolateID from Chocolates WHERE ExpiryDate<=now() + INTERVAL 1 DAY"
    cursor = connection.cursor()
    cursor.execute(Get_expired_chocolateId)
    result = cursor.fetchall()
    f=open('expired.txt','w')
    message="Chocolates with following id have expired:"
    chocolateid=[]
    for res in result:
        f.write(str(res[0]))
        f.write("\n")
        chocolateid.append(str(res[0]))
        delete_from_Ingredients(res[0])
        delete_from_Chocolates(res[0])
        delete_from_Reviews(res[0])
    f.close()
    send_email(chocolateid,message)

def Deletion_basedon_lastDateBought():
    Get_date= "SELECT ChocolateID from Chocolates WHERE LastDateBought<=now() - INTERVAL 1 YEAR"
    cursor = connection.cursor()
    cursor.execute(Get_date)
    result = cursor.fetchall()
    f=open('lastDateBought.txt','w')
    for res in result:
        f.write(str(res[0]))
        f.write("\n")
        delete_from_Ingredients(res[0])
        delete_from_Chocolates(res[0])
        delete_from_Reviews(res[0])
    f.close()

""" try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database="Chocolates_Info",
    ) as connection:
        #show_table()
        Delete_Expired_Chocolates()
        #Deletion_basedon_lastDateBought()
        #Deletion_basedon_lastStockUpdate()
except Error as e:
    print(e) """
connection=connect(host="localhost",user=input("Enter username: "),password=getpass("Enter password: "),database="Chocolates_Info") 
#show_table()
Delete_Expired_Chocolates()
#Deletion_basedon_lastDateBought()
#Deletion_basedon_lastStockUpdate()