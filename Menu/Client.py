from Check_data import *

def Ajouter_avis(cursor):
    '''
    cursor.execute("SELECT * FROM Restaurateur")
    resultat = cursor.fetchall()
    print("je suis la")
    for ligne in resultat:
        print(ligne)
    '''

def Consulter_avis(cursor):
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