from Check_data import *
def Requete3(cursor):
    query = """
        SELECT c.nom, COUNT(av.IdAvis) AS total_plats_mexicanos
        FROM Client c
        JOIN AvisValid av ON c.idClient = av.Client
        JOIN Restaurant r ON av.restaurant = r.restaurant
        WHERE r.TypeResto = 'mexicain'
        GROUP BY c.nom
        ORDER BY total_plats_mexicanos DESC
        LIMIT 10;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    print("Les 10 clients qui ont consommé le plus de plats mexicains sont:")
    for client in results:
        print(f"{client[0]} - Total plats Mexican: {client[1]}")

    print()
    good_choice = False
    while(not good_choice):
        print("Inscrivez 'back' pour retourner en arrière")
        choix = input()
        effacer_terminal()
        if(choix == 'back'):
            good_choice = True