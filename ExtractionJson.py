import json
import mysql.connector

# Connexion à la base de données
connexion = mysql.connector.connect(
    host="localhost",
    user='root',#input("Enter username: ")'',
    password= '2003',#input("Enter password: "),
    database="FastFood"
)

cursor = connexion.cursor()


def notSpecialChar(chaine):
    caracteres_speciaux = "[]"
    for caractere in chaine:
        if caractere in caracteres_speciaux:
            return False
    return True

def goodData(street):
    noSpecialChar = notSpecialChar(street)
    return noSpecialChar

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

def rest_extraction(data, cursor, connexion):
    for element in data:
        # Accéder aux données spécifiques
        firstname = element['firstname']
        lastname = element['lastname']
        nom = f"{firstname} {lastname}"  # Fusionner le prénom et le nom de famille
        address = element['address']
        restaurant = element['restaurant']

        city = address.get('city', '')
        zipcode = address.get('zipcode', '')
        street = address.get('street', '')
        number = address.get('number', '')
        country = address.get('country', '')

        if(goodData(street) and restaurant is not None and sql_get_id(connexion , "restaurant","restaurant","restaurant", restaurant) is not None):         
            #verification s'il ya une cle correspodante dans le
            if (city.isdigit() and not zipcode.isdigit()):
                    city, zipcode = zipcode, city    

        # Insérer les données dans la table Restaurateur
            query_restaurateur = "INSERT INTO Restaurateur (nom, street, numero, city, zipcode, country, restaurant) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            data_restaurateur = (nom, street, number, city, zipcode, country, restaurant)
            cursor.execute(query_restaurateur, data_restaurateur)
            connexion.commit()



def client_extraction(data, cursor, connexion):
    for element in data:
        if 'firstname' in element and 'lastname' in element and 'address' in element:
            firstname = element['firstname']
            lastname = element['lastname']
            address = element['address']

            city = address.get('city', '')
            zipcode = address.get('zipcode', '')
            street = address.get('street', '')
            number = address.get('number', '')
            country = address.get('country', '')

            if(goodData(street)):
                if (city.isdigit() and not zipcode.isdigit()):
                    city, zipcode = zipcode, city    


            # Insérer les données dans la table Client
                query_client = "INSERT INTO Client (nom, prenom, street, numero, city, zipcode, country) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                data_client = (lastname, firstname, street, number, city, zipcode, country)
                cursor.execute(query_client, data_client)

                connexion.commit()

            

def mod_extraction(data, cursor, connexion):
    for element in data:
        if 'firstname' in element and 'lastname' in element and 'address' in element:
            firstname = element['firstname']
            lastname = element['lastname']
            nom = f"{firstname} {lastname}"  # Fusionner le prénom et le nom de famille
            address = element['address']

            city = address.get('city', '')
            zipcode = address.get('zipcode', '')
            street = address.get('street', '')
            number = address.get('number', '')
            country = address.get('country', '')

            if(goodData(street)):
                if (city.isdigit() and not zipcode.isdigit()):
                    city, zipcode = zipcode, city     

            # Insérer les données dans la table Moderateur
                query_mod = "INSERT INTO Moderateur (nom, street, numero, city, zipcode, country) VALUES (%s, %s, %s, %s, %s, %s)"
                data_mod = (nom, street, number, city, zipcode, country)
                cursor.execute(query_mod, data_mod)

                connexion.commit()

def main():

    files = [
        r'AllData\restaurateur.json',
        r'AllData\customers.json',
        r'AllData\moderators.json'
    ]

    with open(files[0]) as file:
        data = json.load(file)
        rest_extraction(data, cursor, connexion)

    with open(files[1]) as file:
        data = json.load(file)
    client_extraction(data, cursor, connexion)

    with open(files[2]) as file:
        data = json.load(file)
        mod_extraction(data, cursor, connexion)

    # Fermer le curseur et la connexion
    cursor.close()
    connexion.close()

main()          # extraction de client moderateur restaurateur