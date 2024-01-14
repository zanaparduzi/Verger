CREATE DATABASE Verger;

USE Verger;

CREATE TABLE Fruits (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nom_du_Produit VARCHAR(100),
    Quantite_en_Stock INT,
    Prix_Unitaire DECIMAL(10, 2),
    Date_de_Reception DATE,
    Date_de_Vente DATE,
    Fournisseur VARCHAR(100)
);

CREATE TABLE Legumes (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nom_du_Produit VARCHAR(100),
    Quantite_en_Stock INT,
    Prix_Unitaire DECIMAL(10, 2),
    Date_de_Reception DATE,
    Date_de_Vente DATE,
    Fournisseur VARCHAR(100)
);

CREATE TABLE Produits_Externes (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nom_du_Produit VARCHAR(100),
    Quantite_en_Stock INT,
    Prix_Unitaire DECIMAL(10, 2),
    Date_de_Reception DATE,
    Date_de_Vente DATE,
    Fournisseur VARCHAR(100)
);

CREATE TABLE Commandes_aux_Fournisseurs (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nom_du_Produit VARCHAR(100),
    Quantite_commandee INT,
    Prix_Unitaire DECIMAL(10, 2),
    Prix_total DECIMAL(10, 2),
    Date_de_commande DATE,
    Fournisseur VARCHAR(100)
);

CREATE TABLE Client (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Nom VARCHAR(50),
    Prenom VARCHAR(50),
    Telephone VARCHAR(20),
    Email VARCHAR(100),
    Adresse VARCHAR(255),
    DateInscription DATE,
    TotalAchats DECIMAL(10, 2),
    DerniereDateAchat DATE,
    username VARCHAR(50),
    admin BOOLEAN DEFAULT FALSE,
    password VARCHAR(50)
);

CREATE TABLE PurchaseHistory (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ClientID INT,
    FOREIGN KEY (ClientID) REFERENCES Client(ID),
    Produit VARCHAR(100),
    Quantite INT,
    Prix DECIMAL(10, 2),
    DateAchat DATE
);

CREATE TABLE Sales (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ClientID INT,
    FOREIGN KEY (ClientID) REFERENCES Client(ID),
    Produit VARCHAR(100),
    Quantite INT,
    Prix DECIMAL(10, 2),
    DateVente DATE
);

/*pour créer le seul compte qui a accès aux pages admin*/
INSERT INTO client (username, password, Nom, admin) VALUES ('admin', 'admin', 'admin', true);

-- Insert into Fruits table
INSERT INTO Fruits (Nom_du_Produit, Quantite_en_Stock, Prix_Unitaire, Date_de_Reception, Date_de_Vente, Fournisseur)
VALUES ('Pomme', 100, 1.50, '2024-01-12', NULL, 'Fournisseur1'),
       ('Banane', 50, 0.75, '2024-01-11', NULL, 'Fournisseur2'),
       ('Orange', 75, 1.20, '2024-01-10', NULL, 'Fournisseur3');

-- Insert into Legumes table
INSERT INTO Legumes (Nom_du_Produit, Quantite_en_Stock, Prix_Unitaire, Date_de_Reception, Date_de_Vente, Fournisseur)
VALUES ('Carotte', 200, 0.90, '2024-01-09', NULL, 'Fournisseur4'),
       ('Tomate', 150, 1.25, '2024-01-08', NULL, 'Fournisseur5'),
       ('Poivron', 100, 1.75, '2024-01-07', NULL, 'Fournisseur6');

-- Insert into Produits_Externes table
INSERT INTO Produits_Externes (Nom_du_Produit, Quantite_en_Stock, Prix_Unitaire, Date_de_Reception, Date_de_Vente, Fournisseur)
VALUES ('Produit1', 50, 5.00, '2024-01-06', NULL, 'Fournisseur7'),
       ('Produit2', 30, 8.50, '2024-01-05', NULL, 'Fournisseur8'),
       ('Produit3', 20, 12.75, '2024-01-04', NULL, 'Fournisseur9');

-- Insert into Commandes_aux_Fournisseurs table
INSERT INTO Commandes_aux_Fournisseurs (Nom_du_Produit, Quantite_commandee, Prix_Unitaire, Prix_total, Date_de_commande, Fournisseur)
VALUES ('Pomme', 50, 1.50, 75.00, '2024-01-12', 'Fournisseur1'),
       ('Banane', 25, 0.75, 18.75, '2024-01-11', 'Fournisseur2'),
       ('Orange', 40, 1.20, 48.00, '2024-01-10', 'Fournisseur3'),
       ('Carotte', 100, 0.90, 90.00, '2024-01-09', 'Fournisseur4'),
       ('Tomate', 75, 1.25, 93.75, '2024-01-08', 'Fournisseur5'),
       ('Poivron', 50, 1.75, 87.50, '2024-01-07', 'Fournisseur6'),
       ('Produit1', 20, 5.00, 100.00, '2024-01-06', 'Fournisseur7'),
       ('Produit2', 15, 8.50, 127.50, '2024-01-05', 'Fournisseur8'),
       ('Produit3', 10, 12.75, 127.50, '2024-01-04', 'Fournisseur9');

RENAME TABLE PurchaseHistory TO Reservations;
ALTER TABLE Reservations
ADD COLUMN Recupere BOOLEAN DEFAULT FALSE;

ALTER TABLE Commandes_aux_Fournisseurs
ADD COLUMN Date_de_Reception DATE;

-- Insert into Commandes_aux_Fournisseurs table
INSERT INTO Commandes_aux_Fournisseurs (Nom_du_Produit, Quantite_commandee, Prix_Unitaire, Prix_total, Date_de_commande, Fournisseur, Date_de_Reception)
VALUES
    ('Pomme', 50, 1.50, 75.00, '2024-01-12', 'Fournisseur1', NULL),
    ('Banane', 25, 0.75, 18.75, '2024-01-11', 'Fournisseur2', NULL),
    ('Orange', 40, 1.20, 48.00, '2024-01-10', 'Fournisseur3', NULL),
    ('Carotte', 100, 0.90, 90.00, '2024-01-09', 'Fournisseur4', NULL),
    ('Tomate', 75, 1.25, 93.75, '2024-01-08', 'Fournisseur5', NULL),
    ('Poivron', 50, 1.75, 87.50, '2024-01-07', 'Fournisseur6', NULL),
    ('Produit1', 20, 5.00, 100.00, '2024-01-06', 'Fournisseur7', NULL),
    ('Produit2', 15, 8.50, 127.50, '2024-01-05', 'Fournisseur8', NULL),
    ('Produit3', 10, 12.75, 127.50, '2024-01-04', 'Fournisseur9', NULL);
