DROP DATABASE IF EXISTS FastFood;
CREATE DATABASE IF NOT EXISTS FastFood; 
USE FastFood; 

-- Création de la table Client
CREATE TABLE IF NOT EXISTS Client (
    idClient INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    street VARCHAR(100) NOT NULL, 
    numero INT NOT NULL,
    city VARCHAR(100) NOT NULL,
    zipcode VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL
);

-- Création de la table Moderateur
CREATE TABLE IF NOT EXISTS Moderateur (
    idModerateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    street VARCHAR(100) NOT NULL, 
    numero INT NOT NULL,
    city VARCHAR(100) NOT NULL,
    zipcode VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL
);

-- Création de la table Restaurateur
CREATE TABLE IF NOT EXISTS Restaurateur (
    idRestaurateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    street VARCHAR(100) NOT NULL, 
    numero INT NOT NULL,
    city VARCHAR(100) NOT NULL,
    zipcode VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL

);

-- Création de la table Restaurant
CREATE TABLE IF NOT EXISTS Restaurant (
    restaurant VARCHAR(100) NOT NULL,
    street VARCHAR(100) NOT NULL, 
    numero INT NOT NULL,
    city VARCHAR(100) NOT NULL,
    zipcode VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    TypeResto VARCHAR(100) NOT NULL,
    price_range VARCHAR(100) NOT NULL,
    evaluation FLOAT NOT NULL,
    Delivery VARCHAR(3) NOT NULL,
    opening INT NOT NULL,
    closing INT NOT NULL,
    PRIMARY KEY(restaurant)
);


-- Création de la table RestoAllergen
CREATE TABLE IF NOT EXISTS AllergenResto (
    restaurant VARCHAR(100) NOt NULL,
    name_plat VARCHAR(100) NOT NULL,
    allergen VARCHAR(100) , 
    PRIMARY KEY (restaurant,name_plat),
    FOREIGN KEY (restaurant) REFERENCES Restaurant(restaurant)
);

-- Création de la table MenuResto
CREATE TABLE IF NOT EXISTS MenuResto (
    restaurant VARCHAR(100) NOT NULL,
    name_plat VARCHAR(100) NOT NULL,
    price VARCHAR(6) NOT NULL,
    PRIMARY KEY (restaurant,name_plat),
    FOREIGN KEY (restaurant) REFERENCES Restaurant(restaurant)
);

-- Création de la table Avis
CREATE TABLE IF NOT EXISTS Avis (
    IdAvis INT AUTO_INCREMENT PRIMARY KEY,
    client INT NOT NULL,                    --id du client 
    restaurant VARCHAR(100) NOT NULL,
    recommandation VARCHAR(100) NOT NULL,
    DateAvis DATE NOT NULL,
    commentaire TEXT,
    FOREIGN KEY (restaurant) REFERENCES Restaurant(restaurant),
    FOREIGN KEY (client) REFERENCES Client(idClient)
);

-- Création de la table AvisRefuse
CREATE TABLE IF NOT EXISTS AvisRefuse (
    IdAvis INT AUTO_INCREMENT PRIMARY KEY,
    client INT NOT NULL,
    restaurant VARCHAR(100) NOT NULL,
    DateAvis DATE NOT NULL,
    commentaire TEXT,
    raison VARCHAR(100) NOT NULL,
     FOREIGN KEY (restaurant) REFERENCES Restaurant(restaurant),
    FOREIGN KEY (client) REFERENCES Client(idClient)
);

-- Création de la table ClientResto
CREATE TABLE IF NOT EXISTS ClientResto (
    client INT NOT NULL,
    restaurant VARCHAR(100) NOT NULL,
    PRIMARY KEY(client,restaurant),
     FOREIGN KEY (restaurant) REFERENCES Restaurant(restaurant),
    FOREIGN KEY (client) REFERENCES Client(idClient)
);

-- Création de la table Experience
CREATE TABLE IF NOT EXISTS Experience (
    DateExp DATE NOT NULL,
    HeureDebut INT NOT NULL, 
    HeureFin INT NOT NULL,
    Avis INT NOT NULL,
    PrixTotal REAL NOT NULL, 
    Cote INT NOT NULL, 
    Isdelivery BOOLEAN NOT NULL, 
    CoteFeeling INT NOT NULL,
    PRIMARY KEY(DateExp, HeureDebut, HeureFin),
    FOREIGN KEY (Avis) REFERENCES Avis(IdAvis)
);

-- Création de la table ExperiencePlat
CREATE TABLE IF NOT EXISTS ExperiencePlat (
    DateExp DATE NOT NULL,
    HeureDebut INT NOT NULL, 
    HeureFin INT NOT NULL,
    plat VARCHAR(100) NOT NULL,
    PRIMARY KEY(DateExp, HeureDebut, HeureFin, plat),
    FOREIGN KEY (plat) REFERENCES MenuResto(name_plat)
);