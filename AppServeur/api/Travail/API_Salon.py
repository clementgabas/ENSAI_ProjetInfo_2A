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
import DAO.gestionParametres as DAOparametres
import DAO.gestionParticipation as DAOparticipation



#@app.route('/home/game/room/settings', methods=['POST']) #ajout de parametre
def ajout_param_partie_P4():
    request.get_json(force=True)
    id_Partie, duree_tour, condition_victoire, Taille_plateau  = request.json.get('id_Partie'), \
                                                                 request.json.get('duree_tour'), \
                                                                 request.json.get('condition_victoire'),  \
                                                                 request.json.get('Taille_plateau')
    DAOparametres.add_parametre(id_Partie, duree_tour, condition_victoire, Taille_plateau)
    print(f"Les paramètres suivants : Durée d'un tour : {duree_tour} secondes \n Condition de victoire : aligner "
          f"{condition_victoire} jetons \n Taille du plateau : {Taille_plateau} \n "
          f"ont a bien été définis pour la partie {id_Partie}")
    response = {"status_code": http_codes.ok, "message": ""}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#----------------------------- param/ game -------------------------------------------
#----------------------------- home/game -------------------------------------------


#@app.route("/home/game/room/colors", methods=["GET"])
def get_liste_couleur_dispos():
    request.get_json(force=True)
    id_partie = request.json.get("id_salle")
    # -- on vérifie si il y a au moins 2 personnes dans la salle sinon il pourrait lancer une partie solo, ce qui casserait tout
    if DAOparties.get_nbr_participants(id_partie) < 2:
        print(f"L'utilisateur ne peut pas être prêt dans la salle {id_partie} car il y est tout seul.")
        response = {"status_code": http_codes.forbidden,
                    "message": "Pas assez d'utilisateurs dans la salle."}  # code 403
        return make_reponse(response, http_codes.forbidden)  # code 403

    print(f"La liste des couleurs disponibles pour la partie {id_partie} a été demandée.")

    #-- on récupère la liste des couleurs dispo
    liste_couleurs_dispos = DAOparticipation.get_free_color(id_partie)
    print(f"La liste des couleurs disponibles pour la partie {id_partie} a été transmise.")

    response = {"status_code": http_codes.ok, "message": "", "liste_couleurs_dispos":liste_couleurs_dispos}
    return make_reponse(response, http_codes.ok)
#----------------------------- home/game -------------------------------------------
#----------------------------- Lunch/game -------------------------------------------

#@app.route("/home/game/room/colors", methods=["POST"])
def ajout_couleur():
    request.get_json(force=True)
    id_partie, pseudo, couleur = request.json.get("id_salle"), request.json.get("pseudo"), request.json.get("couleur")

    #-- on vérifie d'abord que la couleur est tjrs libre
    if not DAOparticipation.is_color_free(id_partie, couleur):
        print(f"La couleur {couleur} a été prise par un autre joueur entre temps dans la partie {id_partie}.")
        liste_couleurs_dispos = DAOparticipation.get_free_color(id_partie)
        response = {"status_code": http_codes.conflict, "message": "La couleur été libre mais a été sélectionnée par un autre joueur entre temps.",
                    "liste_couleurs_dispos": liste_couleurs_dispos}
        return make_reponse(response, http_codes.conflict) #code 409 conflict

    #-- on update la db pour mettre la couleur
    DAOparticipation.update_color(pseudo, id_partie, couleur)
    print(f"Le joueur {pseudo} a choisi la couleur {couleur} dans la partie {id_partie}.")
    response = {"status_code": http_codes.ok, "message": ""}
    return make_reponse(response, http_codes.ok)




#@app.route('/home/game/room/turns', methods=['POST']) #dire qu'on est pret à jouer
def je_suis_pret():
    request.get_json(force=True)
    pseudo, id_salle, est_chef = request.json.get('pseudo'), request.json.get('id_salle'), request.json.get('est_chef')
    print(f"L'utilisateur {pseudo} demande à être prêt dans la salle {id_salle}.")

    #-- on update le est_pret a True dans la table Participation
    DAOparticipation.update_est_pret(pseudo, id_salle, 'True')
    couleur = DAOparticipation.get_couleur(pseudo, id_salle)
    print(f"L'utilisateur {pseudo} est pret dans la table Participation pour la partie {id_salle} avec la couleur {couleur}.")
    #-- on update l'ordre de jeu dans la table Participation
    DAOparticipation.update_ordre(pseudo, id_salle)
    print(f"L'utilisateur {pseudo} s'est vu attribué son ordre de jeu pour la partie {id_salle}.")

    response = {"status_code": http_codes.ok, "message": "Utilisateur pret."}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#@app.route('/home/game/room/launch', methods=['GET']) #savoir si on peut lancer la partie pour le chef
def gestion_tour_lancement_partie():
    request.get_json(force=True)
    pseudo, id_salle, est_chef = request.json.get('pseudo'), request.json.get('id_salle'), request.json.get('est_chef')

    if est_chef:
        print(f"{pseudo}, chef de la salle {id_salle} aimerait savoir si tout le monde est pret pour pouvoir lancer la partie.")
        #-- on DAO pour savoir si tout le monde est pret dans la salle
        if DAOparticipation.number_of_ready(id_salle) == DAOparties.get_nbr_participants(id_salle): #tout les participants sont prets
            print(f"Tout le monde est pret dans la partie {id_salle}")
            response = {"status_code": http_codes.ok, "message": "Tous les participants sont prets."}  # code 200
            return make_reponse(response, http_codes.ok)  # code 200
        else: #au moins 1 participant n'est pas pret
            print(f"Tout le monde n'est pas pret dans la partie {id_salle}")
            response = {"status_code": http_codes.not_acceptable, "message": "Au moins un participant n'est pas pret."}  # code 406
            return make_reponse(response, http_codes.not_acceptable)  # code 406

    else:
        print(f"{pseudo} n'est pas chef de la salle {id_salle} et n'a donc rien à faire ici..")
        response = {"status_code": http_codes.unauthorized, "message": "Vous n'etes pas chef de salle. Vous ne devriez pas être ici comme dirait Hagrid."}  # code 401
        return make_reponse(response, http_codes.unauthorized)  # code 401
#----------------------------- Lunch/game -------------------------------------------
#----------------------------- home/game -------------------------------------------


#@app.route('/home/game/room/launch', methods=['POST'])
def lancer_partie():
    request.get_json(force=True)
    id_partie = request.json.get('id_salle')
    #-- on DAO pour update la table partie et mettre statut = 'en cours'
    DAOparties.lancer_partie(id_partie)
    response = {"status_code": http_codes.ok, "message": "Partie lancée"}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200



def make_reponse(p_object=None, status_code=http_codes.OK):
    if p_object is None and status_code == http_codes.NOT_FOUND:
        p_object = {
            "status": {
                "status_content": [
                    {"code": "404 - Not Found", "message": "Resource not found"}
                ]
            }
        }

    json_response = jsonify(p_object)
    json_response.status_code = status_code
    json_response.content_type = "application/json;charset=utf-8"
    json_response.headers["Cache-Control"] = "max-age=3600"
    return json_response