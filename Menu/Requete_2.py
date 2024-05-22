from Check_data import *
def Requete2(cursor):
    query = """SELECT r.restaurant FROM Restaurant r
            JOIN MenuResto mr ON r.restaurant = mr.restaurant
            WHERE mr.price = (SELECT MAX(price) FROM MenuResto);"""
    cursor.execute(query)

    result = cursor.fetchall()

    restaurant = result[0] if result else None
    if restaurant:
        print(f"Le restaurant avec le plat le plus cher est: {restaurant}")
    else:
        print("No restaurant found.")

    print()
    good_choice = False
    while(not good_choice):
        print("Inscrivez 'back' pour retourner en arrière")
        choix = input()
        effacer_terminal()
        if(choix == 'back'):
            good_choice = True