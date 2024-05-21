import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user='root',
    password='pepe',
    database="FastFood"
)

cursor = conexion.cursor()


def Requete2():
    query = """SELECT r.restaurant FROM Restaurant r
            JOIN MenuResto mr ON r.restaurant = mr.restaurant
            WHERE mr.price = (SELECT MAX(price) FROM MenuResto);"""
    cursor.execute(query)

    result = cursor.fetchall()

    return result[0] if result else None


def main():
    # Call the Requete2 function and print the result
    restaurant = Requete2()
    if restaurant:
        print(f"Le restaurant avec le plat le plus cher est: {restaurant}")
    else:
        print("No restaurant found.")

    # Close the cursor and the connection
    cursor.close()
    conexion.close()

if __name__ == "__main__":
    main() 

