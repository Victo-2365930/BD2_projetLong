import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

load_dotenv()

app = Flask(__name__)

def charger_configuration():
   
   #Pour se connecter à la base de donnée
    config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME'),
        'port': int(os.getenv('DB_PORT', 3306))
    }
    return config

def get_db():
    config = charger_configuration()
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        print(f"Erreur de connexion à la base de données: {err}")
        return None

@app.route('/')
def index():
    db = get_db()
    if db is None:
        return "Erreur de connexion à la base de données"
    
    try:
        cursor = db.cursor()

        # Appel de la table des croûtes
        cursor.execute("SELECT description FROM type_croute")
        croute = cursor.fetchall()

        # Appel de la table des sauces
        cursor.execute("SELECT description FROM type_sauce")
        sauce = cursor.fetchall()

        #Appel de la table des garnitures
        cursor.execute("SELECT description FROM garnitures")
        garniture = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Erreur lors de l'exécution de la requête : {err}")
        return "Erreur lors de l'exécution de la requête", 500
    
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
    
    return render_template('index.html', croute=croute, sauce=sauce, garniture=garniture)

@app.route('/confirmation', methods=['POST'])
def confirmation():
    # Enregistrer les données de renseignements client
    nom = request.form.get('nom')
    num_tel = request.form.get('num_tel')
    adresse_complete = request.form.get('adresse_complete')

    # Enregistrer les données de la commande
    croute = request.form.get('croute')
    sauce = request.form.get('sauce')
    garnitureUn = request.form.get('garnitureUn')
    garnitureDeux = request.form.get('garnitureDeux')
    garnitureTrois = request.form.get('garnitureTrois')
    garnitureQuatre = request.form.get('garnitureQuatre')
        
    
    return render_template('confirmation.html', nom=nom, num_tel=num_tel, adresse_complete=adresse_complete, 
                           croute=croute, sauce=sauce, garnitureUn=garnitureUn,
                           garnitureDeux=garnitureDeux, garnitureTrois=garnitureTrois,
                           garnitureQuatre=garnitureQuatre)

@app.route('/validation', methods=['POST'])
def validation():

    #Reprendre les données des renseignements du client
    nom = request.form.get('nom')
    num_tel = request.form.get('num_tel')
    adresse_complete = request.form.get('adresse_complete')

    #Reprendre les données de la commande
    croute = request.form.get('croute')
    sauce = request.form.get('sauce')
    garnitureUn = request.form.get('garnitureUn')
    garnitureDeux = request.form.get('garnitureDeux')
    garnitureTrois = request.form.get('garnitureTrois')
    garnitureQuatre = request.form.get('garnitureQuatre')

    db = get_db()
    if db is None:
        return "Erreur de connexion à la base de données"
    
    try:
        cursor = db.cursor()

        # Insertion dans la table clients
        query_client = ("INSERT INTO client (nom_complet, num_telephone, adresse_livraison) VALUES (%s, %s, %s)")
        cursor.execute(query_client, (nom, num_tel, adresse_complete))

        # Prendre le id du dernier client inséré
        client_id = cursor.lastrowid

        # Insertion dans la table commande
        query_commande = ("INSERT INTO commande (id_le_client, type_croute , type_sauce) VALUES (%s, (SELECT id_croute FROM type_croute WHERE description = %s ), (SELECT id_sauce FROM type_sauce WHERE description = %s ))")
        cursor.execute(query_commande, (client_id, croute, sauce) )

        # Prendre le id de la dernière commande insérée
        id_commande = cursor.lastrowid
        
        # Insertion des 4 garnitures
        query_garniture_un=("INSERT INTO commande_garniture (id_la_commande, garniture_id) VALUES (%s, (SELECT id_garniture FROM garnitures WHERE description = %s ))")
        cursor.execute(query_garniture_un, (id_commande, garnitureUn) )

        query_garniture_deux=("INSERT INTO commande_garniture (id_la_commande, garniture_id) VALUES (%s, (SELECT id_garniture FROM garnitures WHERE description = %s ))")
        cursor.execute(query_garniture_deux, (id_commande, garnitureDeux) )

        query_garniture_trois=("INSERT INTO commande_garniture (id_la_commande, garniture_id) VALUES (%s, (SELECT id_garniture FROM garnitures WHERE description = %s ))")
        cursor.execute(query_garniture_trois, (id_commande, garnitureTrois) )

        query_garniture_quatre=("INSERT INTO commande_garniture (id_la_commande, garniture_id) VALUES (%s, (SELECT id_garniture FROM garnitures WHERE description = %s ))")
        cursor.execute(query_garniture_quatre, (id_commande, garnitureQuatre) )

        db.commit()


    except mysql.connector.Error as err:
        print(f"Erreur lors de l'exécution de la requête : {err}")
        return f"Erreur SQL: {err}", 500
    
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
    
    return redirect(url_for('index'))

@app.route('/livraison_pizza')
def livraison_pizza():
    db = get_db()
    if db is None:
        return "Erreur de connexion à la base de données"
    
    try:
        cursor = db.cursor()

        # Récupération des livraisons en cours
        query = "SELECT commande.id_commande, client.nom_complet,client.adresse_livraison,client.num_telephone,type_croute.description AS croute, type_sauce.description AS sauce, GROUP_CONCAT(garnitures.description SEPARATOR ', ') AS garnitures FROM livraison_en_cours INNER JOIN client ON livraison_en_cours.id_client_livraison = client.id_client  INNER JOIN commande ON livraison_en_cours.id_commande_en_cours = commande.id_commande INNER JOIN type_croute ON commande.type_croute = type_croute.id_croute INNER JOIN type_sauce ON commande.type_sauce = type_sauce.id_sauce INNER JOIN commande_garniture ON commande_garniture.id_la_commande = commande.id_commande INNER JOIN garnitures ON commande_garniture.garniture_id = garnitures.id_garniture GROUP BY commande.id_commande;"
        cursor.execute(query)
        livraison_en_cours = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Erreur lors de l'exécution de la requête : {err}")
        return "Erreur lors de l'exécution de la requête", 500
    
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
    
    return render_template('livraison_pizza.html', livraison_en_cours=livraison_en_cours)

@app.route('/effacer_commande/<int:commande_id>', methods=['POST'])
def effacer_commande(commande_id):
    db = get_db()
    if db is None:
        return "Erreur de connexion à la base de données"
    
    try:
        cursor = db.cursor()
        
        # Suppression de la commande des livraisons en cours
        query = "DELETE FROM livraison_en_cours WHERE id_commande_en_cours = %s"
        cursor.execute(query, (commande_id,))
        
        db.commit()
        print(f"Commande {commande_id} marquée comme livrée.")
        
    except mysql.connector.Error as err:
        print(f"Erreur lors de l'exécution de la requête : {err}")
        return "Erreur lors de l'exécution de la requête", 500
    
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
    
    return redirect(url_for('livraison_pizza'))

if __name__ == '__main__':
    app.run(debug=True)

