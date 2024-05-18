import mysql
from mysql.connector import connect, Error
from mysql.connector.errors import IntegrityError 
from datetime import datetime

##########################""
def create_connection():
    """
    Create a connection to the MySQL database.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="BIGKARTH",     # METTEZ VOS IDENTIFIANTS
            database="FastFood"
        )
        print("Connection successful")
        return connection
    except Error as e:
        print(f"Error during connection: {e}")
        return None

#################################################################################################
# OTHER FUNCTIONS
################################################################################################
def sql_get_id(connection, table, id, column, value):
    """
    Create an SQL request to get an id of a row in a table.
    :param connection: the connection to the db
    :param table: the name of the table to get an id
    :param column: the name of the column of the table
    :param value: the value to check
    :return: id or None
    """
    cursor = connection.cursor()
    sql = f"SELECT {id} FROM {table} WHERE {column} = (%s)"
    try:
        #print(sql, (value,))
        cursor.execute(sql, (value,))
        result = cursor.fetchall()
    except mysql.connector.IntegrityError as e:
        connection.rollback()
        if e.errno == 1062:
            print(f"Duplicate entry: {value}")
        elif e.errno == 1452:
            print(f"No matching foreign key: {value}")
        else:
            print(f"ERROR: {value}, {e}")
    finally:
        cursor.close()
        connection.commit()
    
    return None if not result else result[0][0]

def parse_date(date_str):
    # Try to parse the date string in the given format
    try:
        return datetime.strptime(date_str, "%m/%d/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        #print(f"Invalid date format: {date_str}")
        return None

def insert_into_table(connection, table, columns, values):
    cursor = connection.cursor()
    qval = ', '.join(['%s'] * len(values))
    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({qval})"
    
    try:
        print("Trying to execute SQL:", sql, "with values:", values)
        cursor.execute(sql, values)
        connection.commit()
        print("Data inserted successfully.")
    except IntegrityError as e:
        connection.rollback()
        if e.errno == 1062:
            print(f"Duplicate entry: {values}")
        elif e.errno == 1452:
            print(f"No matching foreign key: {values}")
        else:
            print(f"ERROR: {values}, {e}")
    except Exception as ex:
        print(f"Unexpected error occurred: {ex}")
    finally:
        print("Closing cursor...")
        cursor.close()

##############################################################################################
#              Extraction functions
#############################################################################################

def extract_deleted_reviews(file_path, connection):
    cursor = connection.cursor()
    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # Skip the header line
        for line in file:
            fields = line.strip().split('\t')
            if len(fields) != 13:
                print("Erreur : Structure de données incorrecte.")
                continue
            #Les valeurs apres le else sont pour voir si ca marche ou pas
            review_text = fields[0] 
            rating = int(float(fields[1])) if len(fields[1]) == 1 else -1
            date_comment = parse_date(fields[2]) if len(fields[2]) == (13 or 14 or 15 or 16 or 17)  else '9999-12-31 00:00:01'
            print(date_comment)
            recommendation = fields[3] if "éviter" in fields[3] or "recommandé" in fields[3] else 'INCORRECT VALUE'
            restaurant_name = fields[4] 
            isdelivery = 0 if fields[5][1] == "H" else 1 # H pour Hospitality
            delivery_hospitality_rating = int(fields[5][-1])
            visit_date = parse_date(fields[6]) if len(fields[6]) == (8 or 9 or 10)  else '9999-12-31'
            items_ordered = fields[7].split(";") 
            cost = float(fields[8]) if float(fields[8]) else 9999.99
            start_time = int(fields[9]) if len(fields[9]) == 1 or len(fields[9]) == 2 else 24
            end_time = int(fields[10]) if len(fields[10]) == 1 or len(fields[10]) == 2 else 24
            reviewer_name = fields[11]
            reason = fields[12]
            client_id = sql_get_id(connection, "Client", "idCLient","nom", reviewer_name)
            if client_id is None:
                print(f"No client found with name: {reviewer_name}")
            else:
                print(f"Client ID: {client_id}")

            # Define the columns and corresponding values for insertion

            columns = [
                "Client", "restaurant", "recommandation", "DateAvis", "commentaire",
                "DateExp", "HeureDebut","HeureFin", "PrixTotal", "Cote", "Isdelivery",
                "CoteFeeling", "raison"
            ]
            # remplacer 100 par id du client (avec son nom)
            values = [
                client_id, restaurant_name, recommendation, visit_date, review_text,
                date_comment, start_time, end_time, cost, rating, isdelivery,
                delivery_hospitality_rating, reason
            ]

            # Insert into AvisRefuse table
            print("hello thereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee 3")
            insert_into_table(connection, "AvisRefuse", columns, values)


def extract_valid_reviews(file_path, connection):
    cursor = connection.cursor()
    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # Skip the header line
        for line in file:
            fields = line.strip().split('\t')
            if len(fields) != 12:
                print("Erreur : Structure de données incorrecte.")
                continue
            #Les valeurs apres le else sont pour voir si ca marche ou pas
            review_text = fields[0] 
            rating = int(float(fields[1])) if len(fields[1]) == 1 else -1
            date_comment = parse_date(fields[2]) if len(fields[2]) == (13 or 14 or 15 or 16 or 17)  else '9999-12-31 00:00:01'
            print(date_comment)
            recommendation = fields[3] if ("éviter" or "recommandé") in fields[3] else 'INCORRECT VALUE'
            restaurant_name = fields[4] 
            isdelivery = 0 if fields[5][1] == "H" else 1 # H pour Hospitality
            delivery_hospitality_rating = int(fields[5][-1])
            visit_date = parse_date(fields[6]) if len(fields[6]) == (8 or 9 or 10)  else '9999-12-31'
            items_ordered = fields[7].split(";") 
            cost = float(fields[8]) if float(fields[8]) else 9999.99
            start_time = int(fields[9]) if len(fields[9]) == 1 or len(fields[9]) == 2 else 24
            end_time = int(fields[10]) if len(fields[10]) == 1 or len(fields[10]) == 2 else 24
            reviewer_name = fields[11]
            client_id = sql_get_id(connection, "Client", "idCLient","nom", reviewer_name)
            if client_id is None:
                print(f"No client found with name: {reviewer_name}")
            else:
                print(f"Client ID: {client_id}")


            # Define the columns and corresponding values for insertion

            columns = [
                "Client", "restaurant", "recommandation", "DateAvis", "commentaire",
                "DateExp", "HeureDebut","HeureFin", "PrixTotal", "Cote", "Isdelivery",
                "CoteFeeling",
            ]
            #remplacer 100 par l'id du client
            values = [
                client_id, restaurant_name, recommendation, visit_date, review_text,
                date_comment, start_time, end_time, cost, rating, isdelivery,
                delivery_hospitality_rating, 
            ]

            # Insert into AvisRefuse table
            print("hello thereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee 3")
            insert_into_table(connection, "AvisValid", columns, values)

            

            

###########################################################################
# MAIN
###########################################################################


def main():
    connection = create_connection()
    if connection:
        file_path_refused_reviews = "AllData/removed_comments.tsv"
        extract_deleted_reviews(file_path_refused_reviews, connection)
        file_path_valid_reviews = "AllData/valid_comments.tsv"
        extract_valid_reviews(file_path_valid_reviews, connection)  
        connection.close()

    # file_path_valid_reviews = "AllData/valid_comments.tsv"
    # extract_valid_reviews(file_path_valid_reviews, connection)  # Pass 'cursor' and 'connection'
    
    # connection.close()

main()