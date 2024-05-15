import os
import mysql.connector
from Restaurateur import *
from Client import *
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

def effacer_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

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
        Requete_1()

    elif(choix == "2"):
        Requete_2() 

    elif(choix == "3"):
        Requete_3()

    elif(choix == "4"):
        Requete_4()

    elif(choix == "5"):
        Requete_5()

    elif(choix == "6"):
        Requete_6()

    else:
        Menu_principale(perso)

def Menu_principale(perso):
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
            cursor.execute("SELECT * FROM Client")
            resultat = cursor.fetchall()
            print("je suis la")
            for ligne in resultat:
                print(ligne)
            Ajouter_avis()

        elif(choix == "2"):
            Consulter_avis()

        elif(choix == "3"):
            Info_resto()

        elif(choix == "4"):
            Requete_demande(perso)

        else:
            main()

    else:
        good_choice = False
        choix = ""

        while (not good_choice):
            print("Menu Principal Restaurateur :")
            print("------------------------------")
            print("1. Entrer un nouveau restaurant")
            print("2. Consulter les avis de son restaurant")
            print("3. Requêtes demandées")
            print("4. Retour en arrière")
            print()
            choix = input()
            effacer_terminal()
            if (choix == "1" or choix == "2" or choix == "3" or choix == "4"):
                good_choice = True

        if(choix == "1"):
            New_resto()

        elif(choix == "2"):
            Avis_resto()

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
        print()
        choix = input()
        effacer_terminal()
        if(choix == "Client" or choix == "Restaurateur"):
            good = True

    return choix

def User():
    good = False
    choix = ""

    while(not good):
        print("Veuillez choisir votre mode de connexion :")
        print("------------------------------------------")
        print("Register")
        print("Login")
        print()
        choix = input()
        effacer_terminal()
        if(choix == "Register" or choix == "Login"):
            good = True

    return choix

def Register(perso):
    good_firstname = False
    good_lastname = False
    firstname = ""
    lastname = ""

    while(not good_firstname):
        print("Qu'elle est votre Prenom ?")
        firstname = input()
        effacer_terminal()
        if(len(firstname) < 10):
            good_firstname = True
    while(not good_lastname):
        print("Qu'elle est votre Nom ?")
        lastname = input()
        effacer_terminal()
        if(len(lastname) < 10):
            good_lastname = True

    #Requete pour ajouter le Nom et le Prénom dans la BDD

    Login(perso)

def Login(perso):
    good_name = False

    while(not good_name):
        print("Connexion :")
        print("-----------")
        print("!! Entrez votre Nom et Prenom avec un espace entre !!")
        print()
        name = input()
        effacer_terminal()
        if(True):   #Requete qui vérifie si le Nom est dans la base de donnée
            good_name = True


def main():
    perso = Perso()
    choix = User()
    if(choix == "Register"):
        Register(perso)
    else:
        Login(perso)

    Menu_principale(perso)

main()