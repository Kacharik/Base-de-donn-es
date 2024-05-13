import mysql.connector
from mysql.connector import connect, Error
from mysql.connector.errors import IntegrityError
import xml.etree.ElementTree as El

def create_connection():
    """
    Connect to the database.
    :return: connection : the connection
    """
    try:
        connection = connect(
            host="localhost",
            user=input("Enter username: "),
            password=input("Enter password: "),
            database="FastFood"
        )
        print("Connection successful")
        return connection

    except Error as e:
        print(e)

def InsertInToTable(connection, table, columns, values):
    """
    Create an SQL request to insert data in a table.
    Execute the request and catch the possible errors
    :param connection: the connection to the db
    :param table: the name of the table to insert the value
    :param columns (tuple): the names of the columns of the table
    :param values: the values to insert
    """
    cursor = connection.cursor()
    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(columns))})"
    print(sql)  # for checking if the values are present correctly
    try:
        cursor.execute(sql, values)
        connection.commit()
    except IntegrityError as e:
        connection.rollback()
        if e.errno == 1062:
            print(f"Duplicate entry: {values}")
        elif e.errno == 1452:
            print(f"No matching foreign key: {values}")
        else:
            print(f"ERROR: {values}, {e}")
    finally:
        cursor.close()

def insertion(connection):
    """
    Insert data into the database from an XML file.
    """
    tree = El.parse("AllData/restos_modifié.xml")
    root = tree.getroot()

    tableResto = "Restaurant"
    columnResto = ["street", "numero", "city", "zipcode", "country", "delivery", "evaluation", "price_range", "TypeResto", "opening", "closing"]

    tablePlat = "Plat"
    columnPlat = ["name_plat", "price"]

    tableMenuResto = "MenuResto"

    tablePlatAllergen = "PlatAllergenes"
    columnPlatAllergen = ["name_plat", "allergen"]

    for restaurant in root.findall("restaurant"):
        address = restaurant.find("address")
        street = address.find("street").text.strip()
        number = address.find("number").text.strip()
        city = address.find("city").text.strip()
        zipcode = address.find("zipcode").text.strip()
        country = address.find("country").text.strip()
        delivery = restaurant.find("delivery").text.strip()
        evaluation = restaurant.find("evaluation").text.strip()
        price_range = restaurant.find("price_range").text.strip()
        Type = restaurant.find("type").text.strip()
        opening_hours = restaurant.find("opening_hours")
        opening = opening_hours.find("opening").text.strip()
        closing = opening_hours.find("closing").text.strip()
        InsertInToTable(connection, tableResto, columnResto, (street, number, city, zipcode, country, delivery, evaluation, price_range, Type, opening, closing))
        menu = restaurant.find("menu")
        for dish in menu.findall("dish"):
            name_plat = dish.find("name").text.strip()
            price = dish.find("price").text.strip()
            InsertInToTable(connection, tablePlat, columnPlat, (name_plat, price))
            InsertInToTable(connection, tableMenuResto, columnResto + ["name_plat"], (street, number, city, zipcode, country, name_plat))
            allergens = dish.find("allergens")
            if allergens is not None:
                for allergen in allergens.findall("allergen"):
                    allergen_name = allergen.text.strip()
                    InsertInToTable(connection, tablePlatAllergen, columnPlatAllergen, (name_plat, allergen_name))

def main():
    connection = create_connection()
    if connection:
        insertion(connection)

main()
