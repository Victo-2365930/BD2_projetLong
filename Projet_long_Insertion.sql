/* 
*Insertion des données dans la base de données pizza_di_mama
*Par Yohan Rajotte
*/

USE pizza_di_mama;
	
INSERT INTO type_croute(description)
	VALUES
	('Classique'),
	('Mince'),
	('Épaisse');
	
INSERT INTO type_sauce(description)
	VALUES 
	('Tomate'),
	('Spaghetti'),
	('Alfredo');
	
INSERT INTO garnitures(description)
	VALUES 
	('Aucune'),
	('Pepperoni'),
	('Champignons'),
	('Oignons'),
	('Poivron'),
	('Olives'),
	('Anchois'),
	('Bacon'),
	('Poulet'),
	('Maïs'),
	('Fromage'),
	('Piments forts');
	