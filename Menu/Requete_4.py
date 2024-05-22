def Requete4(cursor):
    query = """
    SELECT 
        r.restaurant,
        COUNT(m.name_plat) AS number_of_asian_dishes
    FROM 
        Restaurant r
    JOIN 
        MenuResto m ON r.restaurant = m.restaurant
    JOIN 
        (SELECT DISTINCT name_plat 
         FROM MenuResto 
         JOIN Restaurant ON MenuResto.restaurant = Restaurant.restaurant 
         WHERE TypeResto = 'asiatique') asian_dishes 
         ON m.name_plat = asian_dishes.name_plat
    WHERE 
        r.TypeResto = 'asiatique'
    GROUP BY 
        r.restaurant
    ORDER BY 
        number_of_asian_dishes DESC
    LIMIT 1;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    print("Le restaurant non-asiatique proposant le plus de plats qui sont généralement proposés dans des restaurant asiatiques est:")
    for client in results:
        print(f"{client[0]} qui propose {client[1]} plats asiatiques")