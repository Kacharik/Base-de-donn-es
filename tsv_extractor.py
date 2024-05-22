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
            password=input("Entrez le mot de passe : "),     # METTEZ VOS IDENTIFIANTS
            database="FastFood"
        )
        print("Connection successful")
        return connection
    except Error as e:
        print(f"Error during connection: {e}")
        return None

#################################################################################################
#                                   OTHER FUNCTIONS                                             #
#################################################################################################

# ca fonctionne
def check_data(rating, date_comment, recommendation,d_h_rating, visit_date, items_ordered, cost, start, end):
        return (
            isinstance(rating, float) and
            isinstance(date_comment, str) and isinstance(recommendation, str) and 
            isinstance(d_h_rating, int) and isinstance(visit_date, str) and 
            isinstance(items_ordered, list) and all(isinstance(item, str) for item in items_ordered) and 
            isinstance(cost, float) and 
            isinstance(start, int) and 
            isinstance(end, int) and  (start) < (end)
        )
    
################################################################################################

def sql_get_id(connection, table, id_column, *column_value_pairs):
    """
    Create an SQL request to get an id of a row in a table.
    :param connection: the connection to the db
    :param table: the name of the table to get an id
    :param column: the name of the column of the table
    :param value: the value to check
    :return: id or None
    """
    cursor = connection.cursor()
    if len(column_value_pairs) % 2 != 0:
        raise ValueError("column_value_pairs must contain pairs of column names and values")

    # Construct the WHERE clause dynamically
    conditions = " AND ".join([f"{column_value_pairs[i]} = %s" for i in range(0, len(column_value_pairs), 2)])
    values = tuple(column_value_pairs[i + 1] for i in range(0, len(column_value_pairs), 2))

    sql = f"SELECT {id_column} FROM {table} WHERE {conditions}"
    try:
        #print(sql, (value,))
        cursor.execute(sql, values)
        result = cursor.fetchall()
    except mysql.connector.IntegrityError as e:
        connection.rollback()
        if e.errno == 1062:
            print(f"Duplicate entry: {values}")
        elif e.errno == 1452:
            print(f"No matching foreign key: {values}")
        else:
            print(f"Integrity Error: {values}, {e}")
    except mysql.connector.Error as e:
        connection.rollback()
        print(f"General SQL Error: {e}")
    finally:
        cursor.close()
        connection.commit()
    
    return None if not result else result[0][0]

#####################################################################################

def parse_date(date_str):
    # Try to parse the date string in the given format
    try:
        return datetime.strptime(date_str, "%m/%d/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        #print(f"Invalid date format: {date_str}")
        return None

####################################################################################

def check_duplicate_entry(connection, table, columns, values):
    cursor = connection.cursor()
    conditions = ' AND '.join([f"{col} = %s" for col in columns])
    sql = f"SELECT COUNT(*) FROM {table} WHERE {conditions}"

    try:
        cursor.execute(sql, values)
        result = cursor.fetchone()
        return result[0] > 0
    except Error as e:
        print(f"SQL Error: {e}")
        return True
    finally:
        cursor.close()

####################################################################################

def insert_into_table(connection, table, columns, values):
    cursor = connection.cursor()
    qval = ', '.join(['%s'] * len(values))
    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({qval})"
    
    try:
        cursor.execute(sql, values)
        connection.commit()
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
        cursor.close()

#############################################################################################
#                               Extraction functions                                        #
#############################################################################################

            

def extract_reviews(file_path, connection, table_name, columns, columnsPlat, has_reason=False):
    """
    Extracts reviews from a file and inserts them into the specified table.
    :param file_path: The path to the file containing reviews.
    :param connection: The connection to the database.
    :param table_name: The name of the table to insert reviews into.
    :param columns: The columns of the review table.
    :param columnsPlat: The columns of the related plat table.
    :param has_reason: Boolean indicating if the reviews have a reason field (for deleted reviews).
    """
    count = 0
    count_total = 0
    counter = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        next(file)  # Skip the header line
        print(f"Starting to process comments for {table_name}")
        for line in file:
            fields = line.strip().split('\t')
            expected_length = 13 if has_reason else 12
            
            if len(fields) == expected_length:
                count_total += 1
                review_text = fields[0]
                rating = float(fields[1]) if fields[1].replace(".", "").isnumeric() else None
                date_comment = fields[2]
                recommendation = fields[3]
                restaurant_name = fields[4]
                isdelivery = 0 if fields[5][1] == "H" else 1  # H for Hospitality
                delivery_hospitality_rating = int(fields[5][-1]) if fields[5][-1].isnumeric() else None
                visit_date = fields[6]
                items_ordered = fields[7].split(";")
                cost = float(fields[8]) if fields[8].replace(".", "").isnumeric() else None
                start_time = int(fields[9]) if fields[9].isnumeric() else None
                end_time = int(fields[10]) if fields[10].isnumeric() else None
                reviewer_name = fields[11]
                reason = fields[12] if has_reason else None

                IdClient = sql_get_id(connection, "Client", "idClient", "nom", reviewer_name)
                resto = sql_get_id(connection, "Restaurant", "restaurant", "restaurant", restaurant_name)
                # ON TRAITE PLUSIEURS ERREURS POSSIBLES DANS LE NOM

                if IdClient is None and len(reviewer_name.split(" ")) == 2:
                    temp = reviewer_name.split(" ")
                    var1 = temp[1] + temp[0]
                    IdClient = sql_get_id(connection, "Client", "idClient", "nom", var1)

                if IdClient is None and (" " not in reviewer_name):
                    var2 = reviewer_name + " "
                    IdClient = sql_get_id(connection, "Client", "idClient", "nom", var2)
                
                if IdClient is not None and resto is not None:
                    if check_data(rating, date_comment, recommendation, delivery_hospitality_rating, visit_date, items_ordered, cost, start_time, end_time):

                        values = [
                            IdClient, restaurant_name, recommendation, date_comment, review_text,
                            visit_date, start_time, end_time, cost, rating, isdelivery,
                            delivery_hospitality_rating
                        ]
                        if has_reason:
                            values.append(reason)

                        # INSERTING INTO TABLE
                        insert_into_table(connection, table_name, columns, values)
                        count += 1
                        # Get the ID of the inserted review
                        IdAvis = sql_get_id(connection, table_name, "IdAvis", "Client", IdClient, "restaurant", restaurant_name, "DateAvis", date_comment)
                        if IdAvis is not None:
                            for plat in items_ordered:
                                valuesPlat = [IdAvis, plat]

                                if not check_duplicate_entry(connection, f"ExperiencePlat{table_name[4:]}", columnsPlat, valuesPlat):
                                    
                                    insert_into_table(connection, f"ExperiencePlat{table_name[4:]}", columnsPlat, valuesPlat)

    print(f"Total processed for {table_name}: ", count_total)
    print(f"Successfully inserted into {table_name}: ", count)

def extract_deleted_reviews(file_path, connection):
    columns = [
        "Client", "restaurant", "recommandation", "DateAvis", "commentaire",
        "DateExp", "HeureDebut", "HeureFin", "PrixTotal", "Cote", "Isdelivery",
        "CoteFeeling", "raison"
    ]
    columnsPlat = ["Avis", "plat"]
    extract_reviews(file_path, connection, "AvisRefuse", columns, columnsPlat, has_reason=True)

def extract_valid_reviews(file_path, connection):
    columns = [
        "Client", "restaurant", "recommandation", "DateAvis", "commentaire",
        "DateExp", "HeureDebut", "HeureFin", "PrixTotal", "Cote", "Isdelivery",
        "CoteFeeling"
    ]
    columnsPlat = ["Avis", "plat"]
    extract_reviews(file_path, connection, "AvisValid", columns, columnsPlat, has_reason=False)

    

###########################################################################
#                                MAIN                                     #
###########################################################################


def main():
    connection = create_connection()
    if connection:
        file_path_refused_reviews = "AllData/removed_comments.tsv"
        extract_deleted_reviews(file_path_refused_reviews, connection)
        file_path_valid_reviews = "AllData/valid_comments.tsv"
        extract_valid_reviews(file_path_valid_reviews, connection)  
        connection.close()

    print("Job's done")
main()