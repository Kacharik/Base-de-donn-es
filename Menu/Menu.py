import mysql.connector
from Restaurateur import *
from Client import *
from Moderateur import *
from Check_data import *
from Requete_1 import *
from Requete_2 import *
from Requete_3 import *
from Requete_4 import *
from Requete_5 import *
from Requete_6 import *

# Connexion à la base de données
connexion = mysql.connector.connect(
    host="localhost",
    user=input("Entrez le nom d'utilisateur : "),
    password=input("Entrez le mot de passe : "),
    database="FastFood"
)
cursor = connexion.cursor()

def Requete_demande(perso):
    good_choice = False
    choix = ""

    while (not good_choice):
        print("Veuillez choisir la requête que vous voulez lancer :")
        print("----------------------------------------------------")
        print("1. Les restaurant ayant un avis moyen de 3 ou plus")
        print("2. Le restaurant avec le plat le plus cher")
        print("3. Les 10 clients ayant consommé le plus de plats mexicains")
        print("4. Le restaurant non-asiatique proposant le plus de plats qui sont généralement proposés dans des restaurant asiatiques")
        print("5. Le code postal de la ville dans laquelle les restaurants sont les moins bien notés en moyenne")
        print("6. Pour chaque tranche de score moyen (1/5, 2/5, 3/5, ...) de restaurant, le type de nourriture le plus représenté")
        print("7. Retour au menu principal")
        print()
        choix = input()
        effacer_terminal()
        if(int(choix) > 0 and int(choix) < 8):
            good_choice = True

    if(choix == "1"):
        Requete1(cursor)

    elif(choix == "2"):
        Requete2(cursor)

    elif(choix == "3"):
        Requete3(cursor)

    elif(choix == "4"):
        Requete4(cursor)

    elif(choix == "5"):
        Requete5(cursor)

    elif(choix == "6"):
        Requete6(cursor)

    else:
        Menu_principale(perso)

def Menu_principale(perso, id):
    if(perso == "Client"):
        good_choice = False
        choix = ""

        while (not good_choice):
            print("Menu Principal Client :")
            print("------------------------")
            print("1. Ajouter un avis")
            print("2. Consulter les autres avis")
            print("3. Consulter les info des restaurant")
            print("4. Requêtes demandées")
            print("5. Retour en arrière")
            print()
            choix = input()
            effacer_terminal()
            if (choix == "1" or choix == "2" or choix == "3" or choix == "4" or choix == "5"):
                good_choice = True

        if(choix == "1"):
            Ajouter_avis(cursor, id)
            connexion.commit()
            Menu_principale(perso, id)

        elif(choix == "2"):
            Consulter_avis(cursor)
            Menu_principale(perso, id)

        elif(choix == "3"):
            Info_resto(cursor)
            Menu_principale(perso, id)

        elif(choix == "4"):
            Requete_demande(perso)

        else:
            main()

    elif (perso == "Restaurateur"):
        good_choice = False
        choix = ""

        while (not good_choice):
            print("Menu Principal Restaurateur :")
            print("------------------------------")
            print("1. Entrer un nouveau restaurant")
            print("2. Consulter les avis d'un restaurant")
            print("3. Requêtes demandées")
            print("4. Retour en arrière")
            print()
            choix = input()
            effacer_terminal()
            if (choix == "1" or choix == "2" or choix == "3" or choix == "4"):
                good_choice = True

        if(choix == "1"):
            New_resto(cursor)
            connexion.commit()
            Menu_principale(perso, id)

        elif(choix == "2"):
            Avis_resto(cursor)
            Menu_principale(perso, id)

        elif(choix == "3"):
            Requete_demande(perso)

        else:
            main()

    else:
        good_choice = False
        choix = ""

        while (not good_choice):
            print("Menu Principal Moderateur :")
            print("------------------------------")
            print("1. Consulter les Avis valide")
            print("2. Consulter les Avis refusé")
            print("3. Requêtes demandées")
            print("4. Retour en arrière")
            print()
            choix = input()
            effacer_terminal()
            if (choix == "1" or choix == "2" or choix == "3" or choix == "4"):
                good_choice = True

        if(choix == "1"):
            Check_avis(cursor, connexion)
            Menu_principale(perso, id)
        elif(choix == "2"):
            Consulter_avis_refuse(cursor)
            Menu_principale(perso, id)
        elif(choix == "3"):
            Requete_demande(perso)
        else:
            main()

def Perso():
    good = False
    choix = ""

    while(not good):
        effacer_terminal()
        print("Veuillez choisir en tant que quoi vous voulez vous connecter :")
        print("--------------------------------------------------------------")
        print("Client")
        print("Restaurateur")
        print("Moderateur")
        print()
        choix = input()
        effacer_terminal()
        if(choix == "Client" or choix == "Restaurateur" or choix == "Moderateur"):
            good = True

    return choix

def User(perso):
    good = False
    choix = ""

    while(not good):
        print("Veuillez choisir votre mode de connexion :")
        print("------------------------------------------")
        if (perso != "Moderateur"):
            print("Register")
        print("Login")
        print()
        choix = input()
        effacer_terminal()
        if(perso == "Moderateur"):
            if(choix == "Login"):
                good = True
        else:
            if(choix == "Register" or choix == "Login"):
                good = True

    return choix

def Register(perso):
    good_firstname = False
    good_lastname = False
    good_street = False
    good_country = False
    good_city = False
    good_zipcode = False
    good_number = False
    good_restaurant = False

    firstname = ""
    lastname = ""
    street = ""
    country = ""
    city = ""
    zipcode = ""
    number = ""
    restaurant = ""

    while(not good_firstname):
        print("Qu'elle est votre Prenom ?")
        firstname = input()
        effacer_terminal()
        if(notSpecialChar(firstname) and not isDigit(firstname)):
            good_firstname = True
    while(not good_lastname):
        print("Qu'elle est votre Nom ?")
        lastname = input()
        effacer_terminal()
        if(notSpecialChar(lastname) and not isDigit(lastname)):
            good_lastname = True
    while(not good_country):
        print("Dans quel pays habitez vous ?")
        country = input()
        effacer_terminal()
        if(country == "Belgium" or country == "France"):
            good_country = True
    while(not good_city):
        print("Dans quel ville habitez vous ?")
        city = input()
        effacer_terminal()
        if(notSpecialChar(city) and not isDigit(city)):
            good_city = True
    while(not good_zipcode):
        print("Le code postal de votre domicile ?")
        zipcode = input()
        effacer_terminal()
        if(isDigit(zipcode)):
            good_zipcode = True
    while(not good_street):
        print("La rue de votre domicile ?")
        street = input()
        effacer_terminal()
        if(notSpecialChar(street) and not isDigit(street)):
            good_street = True
    while(not good_number):
        print("Le numero de votre domicile ?")
        number = input()
        effacer_terminal()
        if(isDigit(number)):
            good_number = True
    if(perso == "Restaurateur"):
        while (not good_restaurant):
            print("Quel est votre restauarant ?")
            restaurant = input()
            effacer_terminal()
            if (notSpecialChar(restaurant)):
                good_restaurant = True

    nom = firstname + lastname
    nom_espace = firstname + " " + lastname

    if(perso == "Client"):
        query_client = "INSERT INTO Client (nom, street, numero, city, zipcode, country) VALUES (%s, %s, %s, %s, %s, %s)"
        data_client = (nom, street, number, city, zipcode, country)
        cursor.execute(query_client, data_client)

    elif(perso == "Restaurateur"):
        query_restaurateur = "INSERT INTO Restaurateur (nom, street, numero, city, zipcode, country, restaurant) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        data_restaurateur = (nom_espace, street, number, city, zipcode, country, restaurant)
        cursor.execute(query_restaurateur, data_restaurateur)

    else:
        query_mod = "INSERT INTO Moderateur (nom, street, numero, city, zipcode, country) VALUES (%s, %s, %s, %s, %s, %s)"
        data_mod = (nom_espace, street, number, city, zipcode, country)
        cursor.execute(query_mod, data_mod)

    connexion.commit()

def Login(perso):
    good_name = False
    first_name = ""
    last_name = ""
    id = 0

    while(not good_name):
        print("Connexion :")
        print("-----------")
        print("!! Entrez votre Nom !!")
        print()
        last_name = input()
        effacer_terminal()
        print("Connexion :")
        print("-----------")
        print("!! Entrez votre Prenom !!")
        print()
        first_name = input()
        effacer_terminal()
        nom = first_name + last_name
        nom_espace = first_name + " " + last_name
        if(perso == "Client"):
            cursor.execute("SELECT * FROM Client WHERE nom = '" + nom + "'")
            resultat = cursor.fetchall()
        elif(perso == "Restaurateur"):
            cursor.execute("SELECT * FROM Restaurateur WHERE nom = '" + nom_espace + "'")
            resultat = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM Moderateur WHERE nom = '" + nom_espace + "'")
            resultat = cursor.fetchall()

        if(len(resultat) != 0):   #Requete qui vérifie si le Nom est dans la table du perso
            good_name = True
            id = int(resultat[0][0])
    return id


def main():
    perso = Perso()
    choix = User(perso)
    if(choix == "Register"):
        Register(perso)
        id = Login(perso)
    else:
        id = Login(perso)

    Menu_principale(perso, id)

    connexion.close()

main()