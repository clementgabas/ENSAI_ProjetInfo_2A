import os
import traceback
import csv
import random
import json
import hashlib

from api.codeList import _codes

from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from flask_restplus import Api, Resource
from flask_restplus import abort
from flask_caching import Cache
from loguru import logger
from requests import codes as http_codes
from api.commons import configuration

import sqlite3
import requests
from datetime import datetime

import DAO.gestionUser as DAOuser
import DAO.gestionParties as DAOparties

from api.Travail.Base import *


#----------------------------- home/game -------------------------------------------
#@app.route('/home/game/room', methods=['POST'])
def creer_salle():
    request.get_json(force=True)
    pseudo_chef, game = request.json.get('pseudo_chef_salle'), request.json.get('game')
    print(f"{pseudo_chef} crée une salle pour jouer au jeu : {game}.")
    if game.lower() == 'p4':
        total_places = 2
        print("Nombre de place maximum : 2")
    elif game.lower() == 'oie':
        total_places = 5
        print("Nombre de place maximum : 5")

    #-- fonction qui créé la partie dans la table et qui renvoit son id
    id_partie = DAOparties.add_partie(pseudo_chef, game, total_places)
    print(f"création de la salle {id_partie} pour la partie de {pseudo_chef} sur le jeu : {game}")
    #-- on ajoute le joueur directement à sa salle dans la table participation
    nb_places_libres = DAOparties.check_cb_places_libres(id_partie)
    DAOparties.add_to_participation(id_partie, pseudo_chef, nb_places_libres)
    print(f"Il y a {nb_places_libres} place.s libre.s dans la salle {id_partie}")
    #-- on update le statut du joueur en_partie a True dans la table Utilisateur
    DAOuser.update_en_partie_pseudo(pseudo_chef, "True")
    print(f"Mise a jours du status de {pseudo_chef}")
    # -- on renvoit le code ok, le message et l'id de la partie créée.
    response = {"status_code": http_codes.ok, "message": "Salle créée. Joueur ajouté à la salle.", "id_salle":id_partie}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#@app.route('/home/game/room', methods=['PUT'])
def rejoindre_salle():
    request.get_json(force=True)
    pseudo, id_salle, jeu = request.json.get('pseudo'), request.json.get("id_salle"), request.json.get("jeu")
    print(f"Le joueur {pseudo} demande à rejoindre la salle {id_salle} sur le jeu : {jeu}")
    #-- on vérifie si la salle existe
    if not DAOparties.does_partie_exist(id_salle):
        print(f"La salle {id_salle} a rejoindre n'existe pas.")
        response = {"status_code": http_codes.not_found, "message": "Salle inexistante.",
                    "id_salle": id_salle}  # code 404
        return make_reponse(response, http_codes.not_found)  # code 404
    #-- on vérifie si il y a assez de place dans la salle
    nb_places_libres = DAOparties.check_cb_places_libres(id_salle)
    if nb_places_libres == 0:
        print(f"La salle {id_salle} est déjà pleine.")
        response = {"status_code": http_codes.unauthorized, "message": "Salle déjà pleine.",
                    "id_salle": id_salle}  # code 401
        return make_reponse(response, http_codes.unauthorized)  # code 401
    #-- on vérifie si le jeu de la salle correspond bien à notre jeu
    jeu_salle = DAOparties.get_jeu_salle(id_salle)[0][0]
    print(f"le jeu actuel de salle de la salle est : {jeu_salle}")
    print(f"{pseudo} veut jouer à {jeu}")
    if jeu != jeu_salle:
        print("les jeux sont différents, la salle désirée n'existe pas")
        response = {"status_code": http_codes.not_found, "message": "Salle inexistante.",
                    "id_salle": id_salle}  # code 404
        return make_reponse(response, http_codes.not_found)  # code 404
    #-- on ajoute l'utilisateur a la salle
    print("les jeux sont les même")
    DAOparties.add_to_participation(id_salle, pseudo, nb_places_libres)
    # -- on update le statut du joueur en_partie a True dans la table Utilisateur
    DAOuser.update_en_partie_pseudo(pseudo, "True")
    print(f"{pseudo} a bien rejoint la salle {id_salle} pour jouer à {jeu_salle}")
    response = {"status_code": http_codes.ok, "message": "Utilisateur ajouté à la salle.",
                "id_salle": id_salle}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#@app.route('/home/game/room', methods=['DELETE'])
def quitter_salle():
    request.get_json(force=True)
    pseudo, id_salle, est_chef_salle = request.json.get('pseudo'), \
                                       request.json.get("id_salle"), request.json.get("est_chef_salle")
    nb_places_libres = DAOparties.check_cb_places_libres(id_salle)
    print(f"Le joueur {pseudo} demande à quitter la partie {id_salle}")
    #-- pas la peine de vérifier si la salle existe car cette méthode n'est disponible que depuis une salle

    #-- si l'utilisateur qui tente de quitter la salle est le chef de groupe, on vérifie si la salle est vide sauf lui.
    if est_chef_salle:
        #-- s'il est le dernier a quitter la salle, il la quitte, sinon, il ne peut pas la quitter.
        if DAOparties.check_cb_places_libres(id_salle)+1 != DAOparties.check_cb_places_tot(id_salle):
            print(f"Le joueur {pseudo} est chef de la salle {id_salle} il ne peut la quitter car il n'est pas seul")
            response = {"status_code": http_codes.unauthorized, "message": "Utilisateur supprimé de la salle.",
                        "id_salle": id_salle}  # code 401
            return make_reponse(response, http_codes.unauthorized)  # code 401

    #-- on retire le pseudo de la salle dans la salle participation et on ajoute une place de libre dans la salle dans la table Parties
    DAOparties.delete_from_participation(id_salle, pseudo, nb_places_libres)
    # -- on update le statut du joueur en_partie a False dans la table Utilisateur
    DAOuser.update_en_partie_pseudo(pseudo, "False")
    print(f"Le joueur {pseudo} quitte la salle {id_salle}")
    #-- on vérifie si la salle est vide et si elle est vide on la supprime
    if DAOparties.check_cb_places_libres(id_salle) == DAOparties.check_cb_places_tot(id_salle):
        DAOparties.delete_partie(id_salle)
        print(f"Il n'y a plus de joueur dans la salle {id_salle}, elle est donc supprimée")
    response = {"status_code": http_codes.ok, "message": "Utilisateur supprimé de la salle.",
                "id_salle": id_salle}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#@app.route('/home/game/room', methods=['GET'])
def voir_membres_salle():
    request.get_json(force=True)
    id_salle = request.json.get("id_salle")
    print(f"Demande d'affichage des membres de la salle {id_salle}")
    #-- on affiche les membres de cette salle
    membres = DAOparties.get_membres_salle(id_salle)
    print(f"Les membres de la salle {id_salle} sont : {membres}")

    response = {"status_code": http_codes.ok, "message": "Liste des membres de la salle.",
                "liste_membres": membres}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#----------------------------- home/game -------------------------------------------
