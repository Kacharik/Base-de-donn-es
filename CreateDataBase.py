from os import name
import sys
from mysql.connector import connect, Error

def create_connection():
    """
    Connect to the database server.
    :return: connection : the connection
    """
    try:
        
        connection = connect(
            host="localhost",
            user="root",    #input("Enter username: ")"",
            password="BIGKARTH",#input("Enter password: "),
        )
        print("Connection successful")
        return connection

    except Error as e:
        print(e)
def createDb(connection, ddlPath):    # le chemein vers la db
    """
    cette fonction cree la database  avec les
    donnees dans la ddl 
    @params : 
        connection qui fait le lien entre la db et le code
        python et 
        le chemein vers la db

    """
    with open(ddlPath, "r") as f:       #ouverture en lecture uniquement
        create_tables = f.read()          #charge toute un chaine de charactere
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_tables)       #creation des tables dans le database     
            print("Database created successfully!")
    except Error as e:
        print(e)
def main(ddlPath):
    """
    la fonction main creer la connexion entre 
    la base de donnees et 
    creer les table vides dans la db (database)
    """
    createDb(create_connection(), ddlPath)


ddl ="BDD_DDL.sql"
main(ddl)