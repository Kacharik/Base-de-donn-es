import json
import mysql.connector

# Connexion à la base de données
connexion = mysql.connector.connect(
    host="localhost",
    user=input("Entrez le nom d'utilisateur : "),
    password=input("Entrez le mot de passe : "),
    database="FastFood"
)

cursor = connexion.cursor()


def notSpecialChar(chaine):
    caracteres_speciaux = "[]"
    for caractere in chaine:
        if caractere in caracteres_speciaux:
            return False
    return True

def goodDataResto(street):
    noSpecialChar = notSpecialChar(street)
    return noSpecialChar


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

        if(goodDataResto(street)):
            if (city.isdigit() and not zipcode.isdigit()):
                    city, zipcode = zipcode, city    

        # Insérer les données dans la table Restaurateur
            query_restaurateur = "INSERT INTO Restaurateur (nom, street, numero, city, zipcode, country) VALUES (%s, %s, %s, %s, %s, %s)"
            data_restaurateur = (nom, street, number, city, zipcode, country)
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

            if(goodDataResto(street)):
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

            if(goodDataResto(street)):
                if (city.isdigit() and not zipcode.isdigit()):
                    city, zipcode = zipcode, city     

            # Insérer les données dans la table Moderateur
                query_mod = "INSERT INTO Moderateur (nom, street, numero, city, zipcode, country) VALUES (%s, %s, %s, %s, %s, %s)"
                data_mod = (nom, street, number, city, zipcode, country)
                cursor.execute(query_mod, data_mod)

                connexion.commit()



files = [
    r'C:\Users\wayac\Downloads\ProjetBDD\ProjetBDD\AllData\restaurateur.json',
    r'C:\Users\wayac\Downloads\ProjetBDD\ProjetBDD\AllData\customers.json',
    r'C:\Users\wayac\Downloads\ProjetBDD\ProjetBDD\AllData\moderators.json'
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