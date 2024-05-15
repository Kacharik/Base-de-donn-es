# CONCERNE PROJET DE BASE DE DONNEES 

# Membres du groupe
    |SOFFACK MAFOKEN Irène
    |Achari Karthik
    |Celia Aguilera Camino
    |Bilal El Yahyaoui
    
# projet de base de donnees 

    *Configuration de l'environnement
    *installer pip si il n'est pas encore installer
    *installer la bibliotheque pour qt : pip install PySide2  
    *installer pyodbc
        *commande dans l'invite de commande : pip install pyodbc  
        pour la connexion serveur avec la base de donnees 
# organisation des fichiers deja presents
    AllData
        contient toutes les donnees a exploiter
    BDD_DDL : contient toutes nos tables normalisées en sql
    CreationDataBase.py : creer  les tables vides dans BDD_DDL
    les autres fichiers sont les fichiers 'extractions des donnees 
# A SAVOIR:

# faire la connexion entre  mySql et python 
    installer mysql 
    comment installer : pip install mysql-connector-python
    from mysql.connector import connect, Error
# execution
    lancer CreationDataBase.py
    lancer DataExtraction.py
    lancer Extraction.py

