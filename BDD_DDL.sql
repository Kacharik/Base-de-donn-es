DROP DATABASE IF EXISTS FastFood;
CREATE DATABASE IF NOT EXISTS FastFood; 
USE FastFood; 

-- Création de la table Client
CREATE TABLE IF NOT EXISTS Client (
    idClient INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
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

-- Création de la table Restaurant
CREATE TABLE IF NOT EXISTS Restaurant (
    restaurant VARCHAR(100)  PRIMARY KEY,
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
    closing INT NOT NULL
   
);

-- Création de la table Restaurateur
CREATE TABLE IF NOT EXISTS Restaurateur (
    idRestaurateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    street VARCHAR(100) NOT NULL, 
    numero INT NOT NULL,
    city VARCHAR(100) NOT NULL,
    zipcode VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    restaurant VARCHAR(100) NOT NULL,
    FOREIGN KEY (restaurant) REFERENCES Restaurant(restaurant)
);

-- Création de la table AllergenResto
CREATE TABLE IF NOT EXISTS AllergenResto (
    restaurant VARCHAR(100) NOT NULL,
    name_plat VARCHAR(100) NOT NULL,
    allergen VARCHAR(100), 
    PRIMARY KEY (restaurant, name_plat),
    FOREIGN KEY (restaurant) REFERENCES Restaurant(restaurant)
);
-- Création de la table MenuResto
CREATE TABLE IF NOT EXISTS MenuResto (
    restaurant VARCHAR(100) NOT NULL,
    name_plat VARCHAR(100) NOT NULL,
    price VARCHAR(6) NOT NULL,
    PRIMARY KEY (restaurant, name_plat),
    FOREIGN KEY (restaurant) REFERENCES Restaurant(restaurant)
);
-- Création de la table Avis
CREATE TABLE IF NOT EXISTS AvisValid (
    IdAvis INT AUTO_INCREMENT PRIMARY KEY,
    Client  INT NOT NULL,
    restaurant  VARCHAR(100) NOT NULL,
    recommandation VARCHAR(100),
    DateAvis VARCHAR(100) NOT NULL,
    commentaire TEXT,
    DateExp VARCHAR(100) NOT NULL,
    HeureDebut INT NOT NULL, 
    HeureFin INT NOT NULL,
    PrixTotal REAL NOT NULL, 
    Cote INT NOT NULL, 
    Isdelivery BOOLEAN NOT NULL, 
    CoteFeeling INT NOT NULL,
    FOREIGN KEY (restaurant) REFERENCES Restaurant(restaurant),
    FOREIGN KEY (Client) REFERENCES Client(idClient)
);
-- Création de la table AvisRefuse
CREATE TABLE IF NOT EXISTS AvisRefuse (
    IdAvis INT AUTO_INCREMENT PRIMARY KEY,
    Client  INT NOT NULL,
    restaurant  VARCHAR(100) NOT NULL,
    recommandation VARCHAR(100),
    DateAvis VARCHAR(100) NOT NULL,
    commentaire TEXT,
    DateExp VARCHAR(100) NOT NULL,
    HeureDebut INT NOT NULL, 
    HeureFin INT NOT NULL,
    PrixTotal REAL NOT NULL, 
    Cote INT NOT NULL, 
    Isdelivery BOOLEAN NOT NULL, 
    CoteFeeling INT NOT NULL,
    raison VARCHAR(100) NOT NULL,
    FOREIGN KEY (restaurant) REFERENCES Restaurant(restaurant),
    FOREIGN KEY (Client) REFERENCES Client(idClient)
);

-- Création de la table ExperiencePlatValid
CREATE TABLE IF NOT EXISTS ExperiencePlatValid (
    Avis INT NOT NULL,
    plat VARCHAR(100) NOT NULL,
    PRIMARY KEY(Avis, plat),
    FOREIGN KEY (Avis) REFERENCES AvisValid(IdAvis) -- Référence la table AvisValid
);

-- Création de la table ExperiencePlatRefuse
CREATE TABLE IF NOT EXISTS ExperiencePlatRefuse (
    Avis INT NOT NULL,
    plat VARCHAR(100) NOT NULL,
    PRIMARY KEY(Avis, plat),
    FOREIGN KEY (Avis) REFERENCES AvisRefuse(IdAvis) -- Référence la table AvisRefuse
);
