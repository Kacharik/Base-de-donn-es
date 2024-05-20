from Check_data import *

def Check_avis(cursor, connexion):
    good_id = False
    id = ""

    while(not good_id):
        cursor.execute("SELECT * FROM AvisValid")
        resultat = cursor.fetchall()
        print("Voici tout les Avis")
        print("-------------------")
        print()
        for ligne in resultat:
            print(ligne)
        print()
        print("Inscrivez l'id de l'avis à supprimer ou 'back' pour retourner en arrière")
        id = input()
        effacer_terminal()
        if(isDigit(id) or id == "back"):
            good_id = True


    if(id != "back"):
        good_raison = False
        raison = ""
        while (not good_raison):
            print("Qu'elle est la raison ?")
            raison = input()
            effacer_terminal()
            if (notSpecialChar(raison)):
                good_raison = True

        cursor.execute("SELECT * FROM AvisValid WHERE idAvis = '" + id + "'")
        resultat = cursor.fetchall()
        ligne = resultat[0]

        query_client = "INSERT INTO AvisRefuse (Client, restaurant, recommandation, DateAvis, commentaire, DateExp, HeureDebut, HeureFin, PrixTotal, Cote, Isdelivery, CoteFeeling, raison) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data_client = (ligne[1], ligne[2], ligne[3], ligne[4], ligne[5], ligne[6], ligne[7], ligne[8], ligne[9], ligne[10], ligne[11], ligne[12], raison)
        cursor.execute(query_client, data_client)
        connexion.commit()

        cursor.execute("DELETE FROM AvisValid WHERE IdAvis = '" + id + "'")
        connexion.commit()

def Consulter_avis_refuse(cursor):
    good_choice = False
    while(not good_choice):
        cursor.execute("SELECT * FROM AvisRefuse")
        resultat = cursor.fetchall()
        print("Voici tout les Avis refuse")
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