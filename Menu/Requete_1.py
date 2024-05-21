import mysql.connector


conexion = mysql.connector.connect(
    host="localhost",
    user='root',
    password='pepe',
    database="FastFood"
)

cursor = conexion.cursor()

def Requete1():
    query = "SELECT restaurant FROM Restaurant WHERE evaluation >= 3;"
    cursor.execute(query)
    results = cursor.fetchall()
    restaurants = [restaurant[0] for restaurant in results]
    

    return restaurants

def main():
    # Call the Requete function and print the results
    restaurants = Requete1()
    print("Les restaurant ayant un avis moyen de 3 ou plu:")
    for restaurant in restaurants:
        print(restaurant)

    cursor.close()
    conexion.close()

if __name__ == "__main__":
    main()