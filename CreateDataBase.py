from os import name
import sys
from mysql.connector import connect, Error

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
            for result in cursor.execute(create_tables, multi=True):  # Execute multiple statements
                pass
            connection.commit()
            
    except Error as e:
        print(e)
