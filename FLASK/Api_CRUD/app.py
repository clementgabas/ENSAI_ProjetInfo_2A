# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 16:19:36 2020

@author: Maël
"""

    
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Initialisation de l'app
app = Flask(__name__)

######Database######

basedir = os.path.abspath(os.path.dirname(__file__)) 
# permet de dire au serveur que la database est défini par ce fichier

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +os.path.join(basedir, 'db.sqlite')
#configure la base de données
#basedir donne le chemin au serveur et db.sqlite est le nom du fichier database

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#permet d'éviter des conflits avec la console

#Initialisation de SQLAlchemy
db = SQLAlchemy(app)

#Initialisation de Marshmallow
ma = Marshmallow(app)

#classe joueur
class Player(db.Model): #le .Model permet de do
    pseudo = db.Column(db.String(16), primary_key=True)
    classement = db.Column(db.Integer, unique=True)
    amis = db.Column(db.String(16))
#chaque db.Column ajoute un champ à la base de donnée db   
    
    def __init__(self, classement, amis):
        self.classement = classement
        self.amis = amis
#constructeur
        
        
#classe schéma joueur
class  PlayerSchema(ma.Schema):
    class Meta:
        fields = ('pseudo', 'classement', 'amis') 
# fields permet de déterminer les champs publiques
        
#Initialisation Schéma
player_schema = PlayerSchema() 
players_schema = PlayerSchema(many=True)

#Création de méthodes pour interagir avec la db

@app.route('/player', methods=['POST'])
def add_player():
    
    pseudo = request.json['pseudo']
    classement = request.json['classement']
    amis = request.json['amis']
    #informations pour postman
    
    new_player = Player(pseudo, classement, amis)
    #permet d'instancier un objet avec la méthode add_player    
    
    
    db.session.add(new_player)
    db.session.commit()
    #ajoute l'objet instancié à la base de données
    
    return player_schema.jsonify(new_player)
    # information du joueur retournée au client sous le format Json

#obtenir tous les joueurs
@app.route('/player', methods=['GET'])
def get_players():  
    all_players  = Player.query.all() # = SELECT all from Product...
    result = players_schema.dump(all_players) # fourni tous les joueurs
    return jsonify(result.data)

#obtenir un seul joueur
@app.route('/player/<pseudo>', methods=['GET'])
def get_player(pseudo):  
    player  = Player.query.get(pseudo) # = SELECT all from Product...
    return player_schema.jsonify(player)

@app.route('/player/<pseudo>', methods=['PUT'])
def update_player(pseudo):
    player = Player.query.get(pseudo )
    pseudo = request.json['pseudo']
    classement = request.json['classement']
    amis = request.json['amis']
    #informations pour postman
    
    player.pseudo = pseudo
    player.classement = classement
    player.amis = amis
    #créer un nouveau joueur 
    
    
    db.session.commit()
    #ajoute l'objet instancié à la base de données
    
    return player_schema.jsonify(player)
    # information du joueur retournée au client sous le format Json

@app.route('/player/<pseudo>', methods=['DELETE'])
def delete_player(pseudo):  
    player  = Player.query.get(pseudo) # = SELECT all from Product...
    db.session.delete(player)
    db.session.commit
    
    return player_schema.jsonify(player)   
"""
les lignes de commandes :
from app import db
db.create_all() 
permettent de créer la base de données à partir des classes ci-dessus 
(à lancer dans console ou fichier test)
 # Lancer le serveur
""" 

if __name__ == '__main__':
    app.run(debug=True)   
#lancer l'application en mode "test"


