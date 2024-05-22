
def Requete6(cursor):
    for number in range(5):
        query = "SELECT DISTINCT TypeResto FROM Restaurant WHERE evaluation >= " + str(number+1) + " AND evaluation < " + str(number+2)
        cursor.execute(query)
        results = cursor.fetchall()
        compteur_type = {}
        if(len(results) != 0):
            for ligne in results:
                type_resto = ligne[0]
                if type_resto in compteur_type:
                    compteur_type[type_resto] += 1
                else:
                    compteur_type[type_resto] = 1
            type_present = max(compteur_type, key=compteur_type.get)
            print(f"Le type de restaurant le plus présent est {type_present} pour la tranche " + str(number+1) + "/5")
