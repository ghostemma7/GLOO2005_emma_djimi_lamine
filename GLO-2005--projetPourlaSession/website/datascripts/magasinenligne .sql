CREATE DATABASE IF NOT EXISTS magasinenligne;
USE magasinenligne;


CREATE TABLE IF NOT EXISTS Utilisateurs (
    id int AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    date_inscription date NOT NULL UNIQUE,
    password VARCHAR(150) NOT NULL,
    role VARCHAR(150) DEFAULT 'Utilisateur' NOT NULL
    );


CREATE TABLE IF NOT EXISTS Clients (
  idClient INT PRIMARY KEY,
  username VARCHAR(150) NOT NULL UNIQUE,
  email VARCHAR(150) NOT NULL UNIQUE,
  date_inscription date NOT NULL UNIQUE,
  password VARCHAR(150) NOT NULL,
  FOREIGN KEY(idClient) REFERENCES Utilisateurs(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Vendeurs (
  idVendeur INT PRIMARY KEY,
  username VARCHAR(150) NOT NULL UNIQUE,
  email VARCHAR(150) NOT NULL UNIQUE,
  date_inscription date NOT NULL UNIQUE,
  numeroduVendeur INT NOT NULL UNIQUE,
  password VARCHAR(150) NOT NULL,
  FOREIGN KEY(idVendeur) REFERENCES Utilisateurs(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS produits (
  idProduit int AUTO_INCREMENT PRIMARY KEY,
  nomProduits varchar(100) NOT NULL,
  prixProduit decimal(10, 2) NOT NULL,
  descriptions text NOT NULL,
  idCommandes int DEFAULT NULL,
  role VARCHAR(150) DEFAULT "produit" not null
);



CREATE TABLE IF NOT EXISTS Commandes (
  Datecommande date,
  Cout_total decimal(10, 0),
  Statut ENUM("Passer", "Pas_passer"),
  nombre_en_stock INT,
  idClientS INT,
  idCommandeS INT PRIMARY KEY,
  idProduit INT,
  FOREIGN KEY (idProduit) REFERENCES produits(idProduit),
  FOREIGN KEY(idClientS) REFERENCES Clients(idClient) ON DELETE CASCADE
);




CREATE TABLE IF NOT EXISTS Evaluation (
  idCommentaire int PRIMARY KEY,
  commentaire text NOT NULL,
  note decimal(2,1) DEFAULT NULL,
  dateNote date DEFAULT NULL,
  idProduits int DEFAULT NULL,
  FOREIGN KEY (idProduits) REFERENCES produits (idProduit) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Jouets (
  idJouets int PRIMARY KEY,
  nomJouets varchar(45) DEFAULT NULL,
  prixJouet decimal(10, 2) NOT NULL,
  descriptions text NOT NULL,
  FOREIGN KEY (idJouets) REFERENCES produits (idProduit)
);


CREATE TABLE IF NOT EXISTS Livres (
  idLivres int PRIMARY KEY,
  nomLivre varchar(45) NOT NULL,
  prixLivre decimal(10, 2) NOT NULL,
  descriptions text NOT NULL,
  FOREIGN KEY (idLivres) REFERENCES produits (idProduit)
);

DELIMITER //

CREATE PROCEDURE InsertionUtilisateurr(
    IN username_param VARCHAR(150),
    IN email_param VARCHAR(150),
    IN date_inscription_param DATE,
    IN password_param VARCHAR(150),
    IN numero_param INT,
    IN is_client BOOLEAN,
    IN is_vendeur BOOLEAN
)
BEGIN
    DECLARE user_id INT;

    -- Insertion dans la table Utilisateurs
    INSERT INTO Utilisateurs (username, email, date_inscription, password) 
    VALUES (username_param, email_param, date_inscription_param, password_param);

    SET user_id = LAST_INSERT_ID();

    IF is_client THEN
        INSERT INTO Clients (idClient, username, email, date_inscription, password) 
        VALUES (user_id, username_param, email_param, date_inscription_param, password_param);
        
        UPDATE Utilisateurs SET role = 'Client' WHERE id = user_id;

    ELSE
        INSERT INTO Vendeurs (idClient, username, email, date_inscription, numeroduVendeur, password) 
        VALUES (user_id, username_param, email_param, date_inscription_param, numero_param, password_param);
        
        UPDATE Utilisateurs SET role = 'Vendeur' WHERE id = user_id;
    END IF;

    SELECT user_id AS id;

END //

DELIMITER ;


DELIMITER //
CREATE PROCEDURE InsertionProduit(
	IN nomProduits_param varchar(100),
  IN prixProduit_param decimal(10, 2),
  IN descriptions_param text,
  IN role_param VARCHAR(150),
  IN is_jouet BOOLEAN,
  IN is_livre BOOLEAN
)
BEGIN
	  DECLARE p_idProduit INT;
     
    INSERT INTO produits (nomProduits, prixProduit, descriptions) 
    VALUE (nomProduits_param, prixProduit_param, descriptions_param); 
    SET p_idProduit = LAST_INSERT_ID();
 
	IF is_jouet THEN
     INSERT INTO Jouets (idJouets, nomJouets, prixJouet, descriptions) 
     VALUES (nomProduits_param, prixProduit_param, descriptions_param);
     UPDATE Produits P SET P.role = 'Jouets' WHERE P.idProduit = p_idProduit;
	ELSE
	 INSERT INTO Livres (idLivres, nomLivre, prixLivre, descriptions) 
     VALUES (nomProduits_param, prixProduit_param, descriptions_param);
     UPDATE Produits P SET P.role = 'Livres' WHERE P.idProduit = p_idProduit;
  END IF;
END // 

DELIMITER ;

DELIMITER //

CREATE TRIGGER AugmenterNombreProduitApresInsertion
AFTER INSERT ON produits
FOR EACH ROW
BEGIN
    -- Déclarer une variable pour stocker la nouvelle valeur de nombre_en_stock
    DECLARE nouvelle_quantite INT;

    -- Calculer la nouvelle valeur de nombre_en_stock
    SET nouvelle_quantite = (SELECT nombre_en_stock FROM produits WHERE idProduit = NEW.idProduit) + 1;

    -- Mettre à jour la table produits avec la nouvelle valeur
    UPDATE produits
    SET nombre_en_stock = nouvelle_quantite
    WHERE idProduit = NEW.idProduit;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER DiminuerNombreProduitApresCommande
AFTER INSERT ON Commandes
FOR EACH ROW
BEGIN
    DECLARE nouvelle_quantite INT;

    -- Calculer la nouvelle valeur de nombre_en_stock
    SET nouvelle_quantite = (SELECT nombre_en_stock FROM produits WHERE idProduit = NEW.idProduit) - 1;

    -- Mettre à jour la table produits avec la nouvelle valeur
    UPDATE produits
    SET nombre_en_stock = nouvelle_quantite
    WHERE idProduit = NEW.idProduit;
END //
 
DELIMITER ;

 
DELIMITER //
CREATE TRIGGER EffaceVendeur
AFTER DELETE ON Vendeurs
FOR EACH ROW
BEGIN
    DECLARE nmbVendeur INT;
 
    -- Compter le nombre de tuples restants dans auditeurs pour cette personne
    SELECT COUNT(*) INTO nmbVendeur
    FROM Vendeurs
    WHERE idVendeur = OLD.idVendeur;
 
    -- Si la personne n'a plus de tuples dans auditeurs, supprimer le tuple correspondant dans Utilisateurs
    IF nmbVendeur = 0 THEN
        DELETE FROM Vendeur WHERE id = OLD.idVendeur;
    END IF;
END //;
DELIMITER ;
 
 
DELIMITER //
CREATE TRIGGER EffaceProduit
AFTER DELETE ON Produits
FOR EACH ROW
BEGIN
    DECLARE nmbProduits INT;
 
    -- Compter le nombre de tuples restants dans auditeurs pour cette personne
    SELECT COUNT(*) INTO nmbProduits
    FROM Produits
    WHERE idProduits = OLD.idProduit;
 
    -- Si la personne n'a plus de tuples dans auditeurs, supprimer le tuple correspondant dans Utilisateurs
    IF nmbProduits = 0 THEN
        DELETE FROM Produits WHERE id = OLD.idProduit;
    END IF;
END //;
DELIMITER ;


-- INDEXATION

-- Créer un index sur la colonne 'username' de la table 'Utilisateurs'
CREATE INDEX idx_jouets ON Jouets (nomJouets);

-- Créer un index sur la colonne 'role' de la table 'Utilisateurs'
CREATE INDEX idx_livre ON Livres (nomLivre);

-- Créer un index sur la colonne 'posseder' de la table 'Emissions'
CREATE INDEX idx_user ON Utilisateurs (username);