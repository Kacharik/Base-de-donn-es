from Check_data import *
from datetime import datetime

def Ajouter_avis(cursor, first_name, last_name):
    good_choice = False
    while(not good_choice):
        cursor.execute("SELECT restaurant FROM Restaurant")
        resultat = cursor.fetchall()
        print("Choisissez un restaurant")
        print("------------------------")
        print()
        for ligne in resultat:
            print(ligne[0])
        print()
        choix = input()
        effacer_terminal()
        for ligne in resultat:
            if(choix == ligne[0]):
                good_choice = True

    # Obtient la date et l'heure actuelles
    date_actuelle = datetime.now()

    # Formate la date et l'heure comme une chaîne de caractères
    date_formatee = date_actuelle.strftime("%Y/%m/%d")

    # Affiche la date et l'heure
    print("Date et heure d'exécution du code :", date_formatee)

    good_recommandation = False
    good_commentaire = False
    good_DateExp = False
    good_HeureDebut = False
    good_HeureFin = False
    good_PrixTotal = False
    good_Cote = False
    good_Isdelivery = False
    good_CoteFeeling = False

    recommandation = ""
    commentaire = ""
    DateExp = ""
    HeureDebut = ""
    HeureFin = ""
    PrixTotal = ""
    Cote = ""
    Isdelivery = ""
    CoteFeeling = ""
    '''
    while (not good_recommandation):
        print("Recommandation (recommander ou déconseiller) ?")
        recommandation = input()
        effacer_terminal()
        if (recommandation == "recommander" or recommandation == "déconseiller"):
            good_recommandation = True
    while (not good_commentaire):
        print("Commentaire ?")
        commentaire = input()
        effacer_terminal()
        if (True):
            good_commentaire = True
    while (not good_city):
        print("Ville ?")
        city = input()
        effacer_terminal()
        if (notSpecialChar(city) and not isDigit(city)):
            good_city = True
    while (not good_zipcode):
        print("Code postal ?")
        zipcode = input()
        effacer_terminal()
        if (isDigit(zipcode)):
            good_zipcode = True
    while (not good_country):
        print("Pays ?")
        country = input()
        effacer_terminal()
        if (country == "Belgium" or country == "France"):
            good_country = True
    while (not good_type):
        print("Type de restaurant ?")
        type = input()
        effacer_terminal()
        if (notSpecialChar(type) and not isDigit(type)):
            good_type = True
    while (not good_price):
        print("Tranche de prix (haut, moyen ou bas) ?")
        price = input()
        effacer_terminal()
        if (price == "bas" or price == "moyen" or price == "haut"):
            good_price = True
    while (not good_eval):
        print("Evaluation ?")
        eval = input()
        effacer_terminal()
        try:
            if (float(eval) > 0.0 and float(eval) < 5.1):
                good_eval = True
        except ValueError:
            pass
    while (not good_delivery):
        print("Livraison (No ou Yes) ?")
        delivery = input()
        effacer_terminal()
        if (delivery == "No" or delivery == "Yes"):
            good_delivery = True
    while (not good_opening):
        print("Heure d'ouverture ?")
        opening = input()
        effacer_terminal()
        if (isDigit(opening) and int(opening) > 0 and int(opening) < 25):
            good_opening = True
    while (not good_closing):
        print("Heure de fermeture ?")
        closing = input()
        effacer_terminal()
        if (isDigit(closing) and int(opening) > 0 and int(opening) < 25 and int(closing) > int(opening)):
            good_closing = True


    query_client = "INSERT INTO Restaurant (restaurant, street, numero, city, zipcode, country, TypeResto, price_range, evaluation, Delivery, opening, closing) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data_client = (name, street, number, city, zipcode, country, type, price, eval, delivery, opening, closing)
    cursor.execute(query_client, data_client)
    '''
def Consulter_avis(cursor):
    '''
    cursor.execute("SELECT * FROM AvisValid")
    resultat = cursor.fetchall()
    print("je suis la")
    for ligne in resultat:
        print(ligne)
    '''
    pass

def Info_resto(cursor):
    good_choice = False
    while(not good_choice):
        cursor.execute("SELECT * FROM Restaurant")
        resultat = cursor.fetchall()
        print("Voici tout les restaurants")
        print("--------------------------")
        print()
        for ligne in resultat:
            print(ligne)
        print()
        print("Inscrivez 'back' pour retourner en arrière")
        choix = input()
        effacer_terminal()
        if(choix == 'back'):
            good_choice = True