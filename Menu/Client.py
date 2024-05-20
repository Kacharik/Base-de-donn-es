from Check_data import *
from datetime import datetime

def Ajouter_avis(cursor, id):
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
    bool_delivery = True
    CoteFeeling = ""

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
    while (not good_DateExp):
        print("A qu'elle date avez vous visiter ce restaurant (XXXX/XX/XX) ?")
        DateExp = input()
        effacer_terminal()
        if (isDate(DateExp)):
            good_DateExp = True
    while (not good_HeureDebut):
        print("Heure de début ?")
        HeureDebut = input()
        effacer_terminal()
        if (isDigit(HeureDebut) and int(HeureDebut) < 25):
            good_HeureDebut = True
    while (not good_HeureFin):
        print("Heure de fin ?")
        HeureFin = input()
        effacer_terminal()
        if (isDigit(HeureFin) and int(HeureFin) > int(HeureDebut) and int(HeureFin) < 25):
            good_HeureFin = True
    while (not good_PrixTotal):
        print("Prix totale ?")
        PrixTotal = input()
        effacer_terminal()
        try:
            if (float(PrixTotal) > 0.0):
                good_PrixTotal = True
        except ValueError:
            pass
    while (not good_Cote):
        print("Cote ?")
        Cote = input()
        effacer_terminal()
        if (isDigit(Cote)):
            good_Cote = True
    while (not good_Isdelivery):
        print("Avez vous pris à emporter ou en livraison  (Yes ou No) ?")
        Isdelivery = input()
        effacer_terminal()
        if (Isdelivery == "Yes" or Isdelivery == "No"):
            if(Isdelivery == "Yes"):
                Isdelivery = "Delivery"
                bool_delivery = True
            else:
                Isdelivery = "Hospitality and service:"
                bool_delivery = False
            good_Isdelivery = True
    while (not good_CoteFeeling):
        print("Note du service ?")
        CoteFeeling = input()
        effacer_terminal()
        if (isDigit(CoteFeeling)):
            good_CoteFeeling = True

    date_actuelle = datetime.now()
    date_Avis = date_actuelle.strftime("%Y/%m/%d")

    query_client = "INSERT INTO AvisValid (Client, restaurant, recommandation, DateAvis, commentaire, DateExp, HeureDebut, HeureFin, PrixTotal, Cote, Isdelivery, CoteFeeling) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data_client = (id, restaurant, recommandation, date_Avis, commentaire, DateExp, HeureDebut, HeureFin, PrixTotal, Cote, bool_delivery, CoteFeeling)
    cursor.execute(query_client, data_client)

def Consulter_avis(cursor):
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

def Info_resto(cursor):
    good_choice = False
    restaurant = ""
    while(not good_choice):
        cursor.execute("SELECT * FROM Restaurant")
        resultat = cursor.fetchall()
        print("Voici tout les restaurants")
        print("--------------------------")
        print()
        for ligne in resultat:
            print(ligne)
        print()
        print("Inscrivez le nom d'un restaurant pour avoir son Menu et la liste de ces allergène ou 'back' pour retourner en arrière")
        restaurant = input()
        effacer_terminal()
        for ligne in resultat:
            if(restaurant == ligne[0]):
                good_choice = True

    good_choice = False
    while (not good_choice):
        cursor.execute("SELECT * FROM MenuResto WHERE restaurant = '" + restaurant + "'")
        resultat = cursor.fetchall()
        print("Voici le Menu du restaurant '" + restaurant + "'")
        print()
        for ligne in resultat:
            print(ligne[1:])
        print()

        cursor.execute("SELECT * FROM AllergenResto WHERE restaurant = '" + restaurant + "'")
        resultat = cursor.fetchall()
        print("Voici les allergène du restaurant '" + restaurant + "'")
        print()
        for ligne in resultat:
            print(ligne[1:])
        print()

        print("Inscrivez 'back' pour retourner en arrière")
        choix = input()
        effacer_terminal()
        if (choix == 'back'):
            good_choice = True