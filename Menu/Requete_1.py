from Check_data import *
def Requete1(cursor):
    query = "SELECT restaurant FROM Restaurant WHERE evaluation >= 3;"
    cursor.execute(query)
    results = cursor.fetchall()
    restaurants = [restaurant[0] for restaurant in results]

    print("Les restaurant ayant un avis moyen de 3 ou plu:")
    for restaurant in restaurants:
        print(restaurant)

    print()
    good_choice = False
    while(not good_choice):
        print("Inscrivez 'back' pour retourner en arrière")
        choix = input()
        effacer_terminal()
        if(choix == 'back'):
            good_choice = True