import mysql.connector


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

