/* 
*Création de la base de données pizza_di_mama
* Par Yohan Rajotte
*/

DROP DATABASE IF EXISTS pizza_di_mama;
CREATE DATABASE IF NOT EXISTS pizza_di_mama;

USE pizza_di_mama;

/* *******Création des tables ******* */

DROP TABLE IF EXISTS type_croute;

CREATE TABLE IF NOT EXISTS type_croute(
	id_croute INTEGER PRIMARY KEY AUTO_INCREMENT,
	description VARCHAR(255)
	);

DROP TABLE IF EXISTS type_sauce;

CREATE TABLE IF NOT EXISTS type_sauce(
	id_sauce INTEGER PRIMARY KEY AUTO_INCREMENT,
	description VARCHAR(255)
	);

DROP TABLE IF EXISTS garnitures;

CREATE TABLE IF NOT EXISTS garnitures(
	id_garniture INTEGER PRIMARY KEY AUTO_INCREMENT,
	description VARCHAR(255)
	);

DROP TABLE IF EXISTS client;


CREATE TABLE IF NOT EXISTS client(
	id_client INTEGER PRIMARY KEY AUTO_INCREMENT,
	nom_complet VARCHAR(255),
	num_telephone VARCHAR(12),
	adresse_livraison VARCHAR(255)
	);

DROP TABLE IF EXISTS commande;

CREATE TABLE IF NOT EXISTS commande(
	id_commande INTEGER PRIMARY KEY AUTO_INCREMENT,
	id_le_client INTEGER,
	type_croute INTEGER,
	type_sauce INTEGER,
	FOREIGN KEY (id_le_client) REFERENCES client (id_client),
	FOREIGN KEY (type_croute) REFERENCES type_croute (id_croute),
	FOREIGN KEY (type_sauce) REFERENCES type_sauce (id_sauce)
	);

DROP TABLE IF EXISTS commande_garniture;

CREATE TABLE IF NOT EXISTS commande_garniture(
	id_comm_garn INTEGER PRIMARY KEY AUTO_INCREMENT,
	id_la_commande INTEGER,
	garniture_id INTEGER,
	FOREIGN KEY (id_la_commande) REFERENCES commande(id_commande),
	FOREIGN KEY (garniture_id) REFERENCES garnitures(id_garniture)
);

DROP TABLE IF EXISTS livraison_en_cours;

CREATE TABLE IF NOT EXISTS livraison_en_cours(
	id_commande_en_cours INTEGER PRIMARY KEY,
	id_client_livraison INTEGER,
	FOREIGN KEY (id_commande_en_cours) REFERENCES commande(id_commande),
	FOREIGN KEY (id_client_livraison) REFERENCES client(id_client)
	);

/* *******Création du déclencheur ******* */

DROP TRIGGER IF EXISTS commande_livraison;

DELIMITER $$

CREATE TRIGGER IF NOT EXISTS commande_livraison
    AFTER INSERT
    ON commande FOR EACH ROW
    BEGIN
        INSERT INTO livraison_en_cours(id_commande_en_cours, id_client_livraison)
        	VALUES(NEW.id_commande, NEW.id_le_client);
    END $$

DELIMITER ;
