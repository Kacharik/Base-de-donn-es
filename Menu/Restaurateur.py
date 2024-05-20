from Check_data import *

def New_resto(cursor):
    good_name = False
    good_street = False
    good_number = False
    good_city = False
    good_zipcode = False
    good_country = False
    good_type = False
    good_price = False
    good_eval = False
    good_delivery = False
    good_opening = False
    good_closing = False

    name = ""
    street = ""
    number = ""
    city = ""
    zipcode = ""
    country = ""
    type = ""
    price = ""
    eval = ""
    delivery = ""
    opening = ""
    closing = ""

    while (not good_name):
        print("Nom ?")
        name = input()
        effacer_terminal()
        if (notSpecialChar(name)):
            good_name = True
    while (not good_street):
        print("Rue ?")
        street = input()
        effacer_terminal()
        if (notSpecialChar(street) and not isDigit(street)):
            good_street = True
    while (not good_number):
        print("Numéro ?")
        number = input()
        effacer_terminal()
        if (isDigit(number)):
            good_number = True
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

    good_choice = False
    while (not good_choice):
        print("Entrez 'o' pour ajouter un nouveau plat ou 'f' si vous n'avez plus de plat")
        choice = input()
        effacer_terminal()
        if(choice == "o"):
            good_plat = False
            good_price = False
            good_allergene = False
            plat = ""
            price = ""
            allergene = ""

            while (not good_plat):
                print("Qu'elle est le nom du plat ?")
                plat = input()
                effacer_terminal()
                if (notSpecialChar(plat)):
                    good_plat = True
            while (not good_price):
                print("Le prix de ce plat ? (format: euro.centime")
                price = input()
                effacer_terminal()
                if (True):
                    price += "€"
                    good_price = True
            while (not good_allergene):
                print("Ce plat à t'il un allergène ? (Yes or No)")
                choix_allergene = input()
                effacer_terminal()
                if (choix_allergene == "Yes" or choix_allergene == "No"):
                    if(choix_allergene == "Yes"):
                        print("Qu'elle est l'allergène ?")
                        allergene = input()
                        effacer_terminal()
                    else:
                        allergene = "None"
                    good_allergene = True

            query_client = "INSERT INTO MenuResto (restaurant, name_plat, price) VALUES (%s, %s, %s)"
            data_client = (name, plat, price)
            cursor.execute(query_client, data_client)

            if(allergene != "None"):
                query_client = "INSERT INTO AllergenResto (restaurant, name_plat, allergen) VALUES (%s, %s, %s)"
                data_client = (name, plat, allergene)
                cursor.execute(query_client, data_client)

        elif (choice == "f"):
            good_choice = True
        else:
            pass


def Avis_resto(cursor):
    good_choice = False
    restaurant = ""
    while(not good_choice):
        cursor.execute("SELECT restaurant FROM Restaurant")
        resultat = cursor.fetchall()
        print("Choisissez un restaurant")
        print("------------------------")
        print()
        for ligne in resultat:
            print(ligne[0])
        print()
        restaurant = input()
        effacer_terminal()
        for ligne in resultat:
            if(restaurant == ligne[0]):
                good_choice = True

    good_choice = False
    while(not good_choice):
        cursor.execute("SELECT * FROM AvisValid WHERE restaurant = '" + restaurant + "'")
        resultat = cursor.fetchall()
        print("Voici tout les Avis")
        print("-------------------")
        print()
        for ligne in resultat:
            print(ligne)
            print()
        print()
        print("Inscrivez 'back' pour retourner en arrière")
        choix = input()
        effacer_terminal()
        if(choix == 'back'):
            good_choice = True