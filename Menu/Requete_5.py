def Requete5(cursor):
    query = """
    SELECT 
        city,
        zipcode,
        AVG(evaluation) AS average_evaluation
    FROM 
        Restaurant
    GROUP BY 
        city, zipcode
    ORDER BY 
        average_evaluation ASC
    LIMIT 1;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    print("Le code postal de la ville dans laquelle les restaurants sont les moins bien notés en moyenne est:")
    for client in results:
        print(f"{client[1]}")