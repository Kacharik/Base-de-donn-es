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
            password="BIGKARTH",
            database="FastFood"
        )
        print("Connection successful")
        return connection
    except Error as e:
        print(f"Error during connection: {e}")
        return None

#################################################################################################

#cursor = connexion.cursor()

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

def extract_deleted_reviews(file_path, connection):
    cursor = connection.cursor()
    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # Skip the header line
        for line in file:
            fields = line.strip().split('\t')
            if len(fields) != 13:
                print("Erreur : Structure de données incorrecte.")
                continue

            review_text = fields[0] if fields[0] else 'Plain text'
            rating = int(fields[1]) if fields[1].isdigit() else None
            date = parse_date(fields[2]) if fields[2] else None
            recommendation = fields[3] if fields[3] else None
            restaurant_name = fields[4] if fields[4] else None
            categories = fields[5] if fields[5] else None
            review_date = parse_date(fields[6]) if fields[6] else None
            items_ordered = fields[7] if fields[7] else None
            cost = float(fields[8]) if fields[8].replace('.', '', 1).isdigit() else None
            delivery_time = int(fields[9]) if fields[9].isdigit() else None
            delivery_fee = float(fields[10]) if fields[10].replace('.', '', 1).isdigit() else None
            reviewer_name = fields[11] if fields[11] else None
            reason = fields[12] if fields[12] else None
            print(reason)

            if date is None or review_date is None:
                continue

            # try:
            #     isdelivery = 1 if "delivery" in recommendation.lower() else 0
            #     cursor.execute("""
            #         INSERT INTO AvisRefuse (Cote, recommandation, DateAvis, commentaire, DateExp, HeureDebut, HeureFin, PrixTotal, CoteFeeling, Isdelivery, restaurant, raison)
            #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            #     """, (rating, recommendation, date, review_text, review_date, delivery_time, delivery_fee, cost, rating, reason, restaurant_name, categories))
            #     connection.commit()
            #     print("Data inserted successfully into AvisRefuse.")
            # except IntegrityError as e:
            #     connection.rollback()
            #     print(f"Error: {e}")
            
            isdelivery = 1 if "delivery" in recommendation.lower() else 0

            # Define the columns and corresponding values for insertion

            columns = [
                "Cote", "recommandation", "DateAvis", "commentaire", "DateExp",
                "HeureDebut", "HeureFin", "PrixTotal", "CoteFeeling", "Isdelivery",
                "restaurant", "raison"
            ]
            values = [
                rating, recommendation, date, review_text, review_date,
                delivery_time, delivery_time, cost, rating, isdelivery,
                restaurant_name, reason
            ]

            # Insert into AvisRefuse table
            print("hello thereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee 3")
            insert_into_table(connection, "AvisRefuse", columns, values)

# def extract_valid_reviews(file_path, connection):
#     cursor = connection.cursor()
#     with open(file_path, 'r', encoding='utf-8') as file:
#         next(file)  # Skip the header line
#         for line in file:
#             fields = line.strip().split('\t')
#             if len(fields) != 13:
#                 print("Erreur : Structure de données incorrecte.")
#                 continue

#             review_text = fields[0]
#             rating = int(fields[1])
#             visit_date = parse_date(fields[2])
#             recommendation = fields[3]
#             restaurant_name = fields[4]
#             service_delivery_rating = int(fields[5].split(': ')[1])
#             comment_date = parse_date(fields[6])
#             menu_tested = fields[7]
#             price_paid = float(fields[8])
#             meal_start_time = int(fields[9])
#             meal_end_time = int(fields[10])
#             reviewer_name = fields[11]

#             if visit_date is None or comment_date is None:
#                 continue

#             try:
#                 cursor.execute("""
#                     INSERT INTO AvisValid (Cote, recommandation, DateAvis, commentaire, DateExp, HeureDebut, HeureFin, PrixTotal, CoteFeeling, Isdelivery, restaurant)
#                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                 """, (rating, recommendation, visit_date, review_text, comment_date, meal_start_time, meal_end_time, price_paid, rating, service_delivery_rating, restaurant_name))
#                 connection.commit()
#                 print("Data inserted successfully into AvisValid.")
#             except IntegrityError as e:
#                 connection.rollback()
#                 print(f"Error: {e}")

###########################################################################3

# file_path_bad_review = "donnees_projet/removed_comments.tsv"
# file_path_good_review = "donnees_projet/valid_comments.tsv"

# bad_review_extraction(file_path_bad_review, cursor, connexion)

# good_review_extraction(file_path_good_review, cursor, connexion)

# # Fermer le curseur et la connexion
# cursor.close()
# connexion.close()

def main():
    connection = create_connection()
    if connection:
        file_path_refused_reviews = "AllData/removed_comments.tsv"
        extract_deleted_reviews(file_path_refused_reviews, connection)
        connection.close()

    # file_path_valid_reviews = "AllData/valid_comments.tsv"
    # extract_valid_reviews(file_path_valid_reviews, connection)  # Pass 'cursor' and 'connection'
    
    # connection.close()

main()