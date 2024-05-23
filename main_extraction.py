import CreateDataBase
import dataExtraction
import ExtractionJson
import tsv_extractor
from os import name
import mysql
from mysql.connector import connect, Error
import mysql.connector.errors 
from mysql.connector.errors import IntegrityError 
from datetime import datetime
import xml.etree.ElementTree as El
import json

def create_connection():
    """
    Connect to the database server.
    :return: connection : the connection
    """
    try:
        
        connection = connect(
            host="localhost",
            user="root",    #input("Enter username: ")"",
            password=input("Enter password: "),
        )
        print("Connection successful")
        return connection

    except Error as e:
        print(e)

#FILE PATHS
ddlPath = "BDD_DDL.sql"
restaurateur_json_path = 'AllData/restaurateur.json'
customers_json_path = 'AllData/customers.json'
moderators_json_path = 'AllData/moderators.json'
file_path_refused_reviews = "AllData/removed_comments.tsv"
file_path_valid_reviews = "AllData/valid_comments.tsv"

def main():
    connexion = create_connection()
    if connexion is None:
        print("Failed to create database connection.")
        return
    try:

        print("Building database...")
        CreateDataBase.createDb(connexion, ddlPath)
        print("Database finished setting up.")

        with connexion.cursor() as cursor:
            
            # EXTRACTION BEGINS HERE

            print("Beginning extraction of restaurant data...")
            dataExtraction.insertion(connexion, cursor)
            print("Restaurant data extracted.")

            print("Beginning extraction of restaurateur data...")
            with open(restaurateur_json_path) as file:
                data = json.load(file)
                ExtractionJson.rest_extraction(data, cursor, connexion)
            print("Restaurateur data extracted.")

            print("Beginning extraction of client data...")
            with open(customers_json_path) as file:
                data = json.load(file)
                ExtractionJson.client_extraction(data, cursor, connexion)
            print("Client data extracted.")
        
            print("Beginning extraction of moderator data...")
            with open(moderators_json_path) as file:
                data = json.load(file)
                ExtractionJson.mod_extraction(data, cursor, connexion)
            print("Moderator data extracted.")

            print("Extracting deleted comments...")
            tsv_extractor.extract_deleted_reviews(file_path_refused_reviews, connexion)
            print("Deleted comments extracted")

            print("Extracting comments...")
            tsv_extractor.extract_valid_reviews(file_path_valid_reviews, connexion)  
            print("Comments extracted.")

        connexion.commit()
    except Error as e:
        print(f"Error: {e}")
        connexion.rollback()
    finally:
        connexion.close()

main()
