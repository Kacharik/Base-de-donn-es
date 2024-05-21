
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
