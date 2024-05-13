import mysql
from mysql.connector import connect, Error
from mysql.connector.errors import IntegrityError 
import xml.etree.ElementTree as El

##########################""
def create_connection():
    """
    Connect to the database.
    :return: connection : the connection
    """
   
    try:
        
        connection = connect(
            host="localhost",
            user='root',#input("Enter username: ")'',
            password= '2003',#input("Enter password: "),
            database="FastFood"
        )
        
        print("Connection successful")
        return connection

    except Error as e:          # reception des error lors de la connection
        print(e)

#################################################################################################
#CONNEXION ETABLIE
def notSpecialChar(chaine):
    caracteres_speciaux = "!@#$%^&*()-_+=[]{}|;:',.<>?`~"
    for caractere in chaine:
        if caractere in caracteres_speciaux:
            return False
    return True

def goodDataResto(street,number,city,zipcode,country,delivery,evaluation,price_range,Type,opening,closing):
    # verifier si toutes les donnees pour un restaurant sont valides 
    noSpecialChar = notSpecialChar(street) and notSpecialChar(city)and \
    notSpecialChar(zipcode) and notSpecialChar(Type) and notSpecialChar(opening) and \
    notSpecialChar(closing)
    goodNote = 0<= float(evaluation) <=5                # si l'evaluation est correct et a un sens 
    goodType = price_range in ("moyen", "haut","bas")
    goodCountry = country in ("France", "Belgium")
    goodDelivery = delivery in("Yes", "No") or delivery in("yes", "no")         # tester le isUper() or les isLower()
    goodHour = opening < closing
    goodDigit = number.isdigit()
    # Vérifie si le caractère est dans la liste des caractères spéciaux
    return noSpecialChar and goodDigit and goodHour and goodCountry and goodType and goodDelivery and goodNote
  
def get_id(connection, table, ):
    """renvoie le id pour une table"""
def InsertInToTable(connection, table, columns, values):
    """
    Create an SQL request to insert data in a table.
    Execute the request and catch the possible errors
    :param connection: the connection to the db
    :param table: the name of the table to insert the value
    :param columns (tuple): the names of the columns of the table
    :param values: the values to insert
    :param qval: type and number of the values (optional)
    """
    cursor = connection.cursor()
    
    qval = ', '.join(['%s']*len(values))

 
    sql = f"INSERT INTO {table} ({', '.join(item for item in columns)}) VALUES ({qval})"
    try:
        cursor.execute(sql, values)     #execution de l'insertion
        #gestion des erreure 
    except mysql.connector.IntegrityError as e:      # si les integrites sont bafouet
        connection.rollback()
        if e.errno == 1062:
            print(f"Duplicate entry: {values}")
        elif e.errno == 1452:
            print(f"No matching foreign key: {values}")
        else:
            print(f"ERROR: {values}, {e}")
    finally:
        cursor.close()
        connection.commit()

#############################################################################################"
def insertion(connection): 
    """
    
     @params : 
        connection   : pour la connection avec la db 
        line : les valeurs des attributs de l'entite
    @def :  ceci est un fichier xml
        insert une nouvelle data dans la table Restaurant 
    """
    # analyse du fichier
    tree = El.parse("AllData/restos_modifié.xml")
    root = tree.getroot()
    # il ya plusieurs tables qui emanent de cet enregistrement 
    tableResto= "Restaurant"
    columnResto = ["restaurant","street","numero","city","zipcode",
    "country","delivery","evaluation","price_range",
    "TypeResto","opening","closing"]
    tableMenuResto = "MenuResto"
    columnMenu = ["restaurant","name_plat","price"]
    
    tableAllergenResto = "AllergenResto"
    columnPlatAllergen = ["restaurant","name_plat","allergen"]
    ## informations restaurants
    for restaurant in root.findall("restaurant"):
    #INFORLATIONS SUR LE RESTAUAURANT

        address = restaurant.find("address")
        resto = restaurant.find("name").text.strip()
        street = address.find("street").text.strip()          # strip pour la suppression des espaces 
                                                        #avant et apres s'il y en a 
        number  = address.find("number").text.strip()
        city = address.find("city").text.strip()
        zipcode = address.find("zipcode").text.strip()
        country = address.find("country").text.strip()
        delivery= restaurant.find("delivery").text.strip()
        evaluation = restaurant.find("evaluation").text.strip()
        price_range = restaurant.find("price_range").text.strip()
        Type = restaurant.find("type").text.strip()
        opening_hours = restaurant.find("opening_hours")
        opening = opening_hours.find("opening").text.strip()
        closing = opening_hours.find("closing").text.strip()
              
        if(goodDataResto(street,number,city,zipcode,country,delivery,evaluation,price_range,Type,opening,closing)):
            if (city.isdigit() and not zipcode.isdigit()):
                city, zipcode = zipcode, city           #on swap les deux
            InsertInToTable(connection,tableResto,columnResto,(resto,street,number,city,zipcode,country,delivery,evaluation,price_range,Type,opening,closing))
        
    #############################################################

        ## INFORMATIONS SUR LES PLATS 
            menu = restaurant.find("menu")
            for dish in menu.findall("dish"):
                name_plat = dish.find("name").text.strip()
                price = dish.find("price").text.strip()
            
               # InsertInToTable(connection,tablePlat,columnPlat,(name_plat,price))         # faire un insert dans la table plat
                InsertInToTable(connection,tableMenuResto,columnMenu,(resto,name_plat,price))         #insert dans la table menuPlat
            
            #############################################################
        # INFORMATIONS SUR PLAT ALLERGENES
                for allergen in dish.findall("allergens"):
                    all = allergen.find("allergen")
                    if (all is not None):                    # s'il ya toujours un allergene 
                        allergen_name = all.text.strip()
                        InsertInToTable(connection,tableAllergenResto,columnPlatAllergen,(resto,name_plat,allergen_name))
            #############################################################

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
        print(sql, (value,))
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

def main():
    connection = create_connection()
    insertion(connection)
main()





