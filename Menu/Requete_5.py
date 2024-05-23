from Check_data import *
def Requete5(cursor):
    query = """
    SELECT 
        zipcode,
        AVG(evaluation) AS average_evaluation
    FROM 
        Restaurant
    GROUP BY 
        zipcode
    ORDER BY 
        average_evaluation ASC
    LIMIT 1;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    print("Le code postal de la ville dans laquelle les restaurants sont les moins bien notés en moyenne est:")
    for client in results:
        print(f"{client[0]}")

    print(f"avec une moyenne de {client[1]}")
    good_choice = False
    while(not good_choice):
        print("Inscrivez 'back' pour retourner en arrière")
        choix = input()
        effacer_terminal()
        if(choix == 'back'):
            good_choice = True