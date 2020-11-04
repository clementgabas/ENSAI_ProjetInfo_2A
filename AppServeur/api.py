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

import travailMDP.testmdp as MDPgestion
import DAO.gestionUser as DAOuser
import DAO.gestionAmis as DAOfriend
import DAO.gestionClassement as DAOclassement
import DAO.gestionParties as DAOparties

CACHE_TTL = 60  # 60 seconds

# Load conf
conf = configuration.load()
script_dir = os.path.dirname(__file__)


def _init_app(p_conf):
    # Load app config into Flask WSGI running instance
    r_app = Flask(__name__)
    r_app.config["API_CONF"] = p_conf


    blueprint = Blueprint("api", __name__)
    r_swagger_api = Api(
        blueprint,
        doc="/" + p_conf["url_prefix"] + "/doc/",
        title="API",
        description="Serveur jeux API",
    )
    r_app.register_blueprint(blueprint)
    r_ns = r_swagger_api.namespace(
        name=p_conf["url_prefix"], description="Api documentation"
    )

    return r_app, r_swagger_api, r_ns

app, swagger_api, ns = _init_app(conf)

# Init cache
cache = Cache(app, config={"CACHE_TYPE": "simple"})

# Access log query interceptor
@app.before_request
def access_log():
    logger.info("{0} {1}".format(request.method, request.path))

#-------------------------------------------------------------------

@app.route("/", strict_slashes=False) #acceuil
@app.route("/home") #acceuil
def get():
    """
        Base route
    """
    response = {"status_code": http_codes.OK, "message": "Vous êtes bien sur l'Api jeux"}
    return make_reponse(response, http_codes.OK)

#---------------------------- home -----------------------------------
@app.route('/home/users', methods = ['POST']) #creation d'un nouvel utilisateur
def new_user():
    request.get_json(force=True)
    username, hpassword, pseudo = request.json.get('username'), request.json.get('hpassword'), request.json.get('pseudo')

    #-- on vérifie si un tel username n'existe pas déjà dans la DB
    if DAOuser.does_username_exist(username):
        response = {"status_code": http_codes.conflict, "message": "User already exists in the DB."} #error 409
        return make_reponse(response, http_codes.conflict)
    #-- on vérifie si un tel pseudo n'existe pas déjà dans la DB
    if DAOuser.does_pseudo_exist(pseudo):
        response = {"status_code": http_codes.conflict, "message": "Pseudo already exists in the DB."} #error 409
        return make_reponse(response, http_codes.conflict)

    #-- on ajoute le nouvel utilisateur (username, pseudo, hpassword) à la DB Utilisateur
    DAOuser.add_user(username, pseudo, hpassword)
    #-- on ajoute l'utilisateur à la db Score pour suivre ces classement
    DAOuser.add_user_score(pseudo)
    #-- on renvoit le code ok et le message d'ajout de l'utilisateur.
    response = {"status_code": http_codes.ok, "message": "L'utilisateur a bien été ajouté à la DB."}
    return make_reponse(response, http_codes.ok) #code 200

@app.route('/home/connexion', methods = ['GET']) #connexion d'un utilisateur
def identification():
    request.get_json(force=True)
    username, password= request.json.get('username'), request.json.get('password')

    #-- on vérifie si un utilisateur avec cet identifiant existe dans la DB
    if not DAOuser.does_username_exist(username):
        response = {"status_code": http_codes.unauthorized, "message": "Username incorrect."} #error 401
        return make_reponse(response, http_codes.unauthorized)

    #-- on récupère le hpass associé à l'utilisateur et on le compare au hash du mdp fournit pour la connection
    stored_hpass = DAOuser.get_hpass_username(username)
    if not MDPgestion.verify_password(stored_hpass, password):
        response = {"status_code": http_codes.unauthorized, "message": "Password incorrect."}  # error 401
        return make_reponse(response, http_codes.unauthorized)

    #-- on vérifie que l'utilisateur n'est pas déjà conencté
    if DAOuser.get_est_connecte(username): #l'utilisateur est déjà connecté
        response = {"status_code": http_codes.forbidden, "message": "User already connected."}  # error 403
        return make_reponse(response, http_codes.forbidden)

    #-------------------------- Connexion réussie -----------------------------
    #-- on update le statut "est_connecte" à True de l'utilisateur qui vient de se connecter
    DAOuser.update_est_connecte(username, username_or_pseudo = 'username', nouvel_etat = 'True')
    #-- on renvoit le code ok, le message et le pseudo
    pse = DAOuser.get_pseudo(username)
    response = {"status_code": http_codes.ok, "message": "Connection réussie.", "pseudo": pse}
    return make_reponse(response, http_codes.ok)  # code 200

@app.route('/home/deconnexion', methods = ['GET']) #deconnexion d'un utilisateur
def deconnect():
    request.get_json(force=True)
    pseudo = request.json.get('pseudo')

    # -- on vérifie si un utilisateur avec ce pseudo existe dans la DB
    if not DAOuser.does_pseudo_exist(pseudo):
        response = {"status_code": http_codes.unauthorized, "message": "Pseudo incorrect."}  # error 401
        return make_reponse(response, http_codes.unauthorized)

    #-- on update le statut "est_connecte" à False de l'utilisateur qui vient de se deco via son pseudo
    DAOuser.update_est_connecte(pseudo, username_or_pseudo = 'pseudo', nouvel_etat = 'False')
    #-- on renvoit le code ok et le message.
    response = {"status_code": http_codes.ok, "message": "Déconnection réussie."}
    return make_reponse(response, http_codes.ok)  # code 200

#-----------------------------home/main -------------------------------------------

@app.route('/home/main/profil/friends', methods=['GET']) #affichage liste amis
def afficher_liste_amis():
    request.get_json(force=True)
    pseudo = request.json.get('pseudo')

    #-- on récupère la liste des amis
    liste_amis = DAOfriend.afficher_liste_amis(pseudo)
    #-- on renvoit le code ok, le message et la liste des amis.
    response = {"status_code": http_codes.ok, "message": "Liste des amis récupérée.", 'liste_amis': liste_amis} #code 200
    return make_reponse(response, http_codes.ok)  # code 200

@app.route('/home/main/profil/friends', methods=['POST']) #ajout d'un ami
def ajout_ami():
    request.get_json(force=True)
    pseudo, pseudo_ami = request.json.get('pseudo'), request.json.get('pseudo_ami')

    #-- vérification si un utilisateur avec le pseudo_ami existe dans la DB
    if not DAOuser.does_pseudo_exist(pseudo_ami):
        response = {"status_code": http_codes.not_found, "message": "L'ami à ajouter n'existe pas."}  # code 404
        return make_reponse(response, http_codes.not_found)  # code 404

    #-- on vérifie si pseudo n'est pas déjà ami avec pseudo_ami
    if DAOfriend.are_pseudos_friends(pseudo, pseudo_ami):
        response = {"status_code": http_codes.already_reported, "message": "L'amitié existe déjà."}  # code 208
        return make_reponse(response, http_codes.already_reported)  # code 208

    #-- on effectue la procédure qui ajoute le lien d'amitié
    DAOfriend.add_amitie(pseudo, pseudo_ami)
    #-- on renvoit le code ok et le message d'ajout de l'ami.
    response = {"status_code": http_codes.ok, "message": "Ami ajouté."}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

@app.route('/home/main/profil/friends', methods=['DELETE']) #suppression d'un ami
def supp_ami():
    request.get_json(force=True)
    pseudo, pseudo_ami = request.json.get('pseudo'), request.json.get('pseudo_ami')

    #-- vérification si un utilisateur avec le pseudo_ami existe dans la DB
    if not DAOuser.does_pseudo_exist(pseudo_ami):
        response = {"status_code": http_codes.not_found, "message": "L'ami à supprimer n'existe pas."}  # code 404
        return make_reponse(response, http_codes.not_found)  # code 404

    # -- on vérifie si pseudo est bien ami avec pseudo_ami
    if not DAOfriend.are_pseudos_friends(pseudo, pseudo_ami):
        response = {"status_code": http_codes.already_reported, "message": "L'amitié n'existe pas."}  # code 208
        return make_reponse(response, http_codes.already_reported)  # code 208

    # -- on effectue la procédure qui supprime le lien d'amitié
    DAOfriend.sup_amitie(pseudo, pseudo_ami)
    #-- on renvoit le code ok et le message de suppression de l'ami.
    response = {"status_code": http_codes.ok, "message": "Ami supprimé."}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

@app.route('/home/main/profil/user/pseudo', methods=['PUT']) #modification du pseudo
def modif_pseudo():
    request.get_json(force=True)
    old_pseudo, new_pseudo = request.json.get('old_pseudo'), request.json.get('new_pseudo')

    #-- on vérifie si le new_pseudo est libre
    if DAOuser.does_pseudo_exist(new_pseudo):
        response = {"status_code": http_codes.conflict, "message": "Le pseudo demandé est déjà utilisé."}  # code 409
        return make_reponse(response, http_codes.conflict)  # code 409

    # -- on effectue la procédure qui uptade le pseudo
    DAOuser.update_pseudo(old_pseudo, new_pseudo)
    # -- on renvoit le code ok et le message de suppression de l'ami.
    response = {"status_code": http_codes.ok, "message": "pseudo mis à jour."}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

@app.route('/home/main/profil/user/password', methods=['PUT']) #modification du mot de passe
def modif_password():
    request.get_json(force=True)
    pseudo, old_password, new_password = request.json.get('pseudo'), request.json.get('old_password'), request.json.get('new_password')
    #-- on vérifie si l'ancien mdp correspond bien au mdp enregistré pour le pseudo
        #-- on recupere le hpass stocké
    stored_hpass = DAOuser.get_hpass_pseudo(pseudo)
    print(stored_hpass)
        #-- on compare les hpass
    if not MDPgestion.verify_password(stored_hpass, old_password):
        response = {"status_code": http_codes.unauthorized, "message": "Password incorrect."}  # error 401
        return make_reponse(response, http_codes.unauthorized)

    new_hpass = MDPgestion.hacherMotDePasse(new_password)
    #-- on modifie le mdp dans la db utilisateur
    DAOuser.update_password(pseudo, new_hpass)
    # -- on renvoit le code ok et le message de suppression de l'ami.
    response = {"status_code": http_codes.ok, "message": "mdp mis à jour."}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200


@app.route('/home/main/profil/user/stat', methods=['GET']) #afficher stat perso
def afficher_stats_perso():
    request.get_json(force=True)
    pseudo = request.json.get('pseudo')
    stat_perso = DAOuser.get_stat(pseudo)
    response = {"status_code": http_codes.ok, "message": "Statistiques personelles récupérées.",
                'Statistiques personelles': stat_perso}  # code 200
    return make_reponse(response, http_codes.ok)

@app.route('/home/main/profil/user/stat', methods=['PUT']) #reinitialiser stat perso
def modifier_stats_perso():
    request.get_json(force=True)
    pseudo = request.json.get('pseudo')
    DAOuser.update_stat(pseudo)
    response = {"status_code": http_codes.ok, "message": "Statistiques personelles réinitialisées."}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200



@app.route('/home/main/profil/classment/jeu', methods=['GET']) #affichage classement jeu de l'oie
def afficher_classement():
    request.get_json(force=True)
    nom_jeu = request.json.get("nom_jeu")
    #-- on récupère le classement du jeu de l'oie
    classement_jeu = DAOclassement.afficher_classement_jeu(nom_jeu)
    #-- on renvoit le code ok, le message et le classement du jeu de l'oie
    response = {"status_code": http_codes.ok, "message": "Classement jeu de l'oie récupéré.", 'classement_jeu': classement_jeu} #code 200
    return make_reponse(response, http_codes.ok)  # code 200

@app.route('/home/main/profil/classment/general', methods=['GET']) #affichage classement général
def afficher_classement_general():
    request.get_json(force=True)
    #-- on récupère le classement général
    classement_general = DAOclassement.afficher_classement_general()
    #-- on renvoit le code ok, le message et le classement général
    response = {"status_code": http_codes.ok, "message": "Classement général récupéré.", "classement_general": classement_general} #code 200
    return make_reponse(response, http_codes.ok)  # code 200

#------------------------home/game----------------------------------
@app.route('/home/game/room', methods=['POST'])
def creer_salle():
    request.get_json(force=True)
    pseudo_chef, game = request.json.get('pseudo_chef_salle'), request.json.get('game')
    if game.lower() == 'p4':
        total_places = 2
    elif game.lower() == 'oie':
        total_places = 5


    #-- fonction qui créé la partie dans la table et qui renvoit son id
    id_partie = DAOparties.add_partie(pseudo_chef, game, total_places)
    #-- procedure qui créé la table coups associée
    DAOparties.create_coup(id_partie)
    # -- on renvoit le code ok, le message et l'id de la partie créée.
    response = {"status_code": http_codes.ok, "message": "Salle et table coup créées.", "id_salle":id_partie}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200



#---------------------------------------------------------
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

def _success(response):
    return make_reponse(response, http_codes.OK)


def _failure(exception, http_code=http_codes.SERVER_ERROR):
    try:
        exn = traceback.format_exc(exception)
        logger.info("EXCEPTION: {}".format(exn))
    except Exception as e:
        logger.info("EXCEPTION: {}".format(exception))
        logger.info(e)

    try:
        data, code = exception.to_tuple()
        return make_reponse(data, code)
    except:
        try:
            data = exception.to_dict()
            return make_reponse(data, exception.http)
        except Exception:
            return make_reponse(None, http_code)

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


if __name__ == "__main__":
    DAOuser.put_all_users_disconnected()
    #cf_port = os.getenv("PORT")
    cf_port = conf["port"]
    if cf_port is None:
        app.run(host="localhost", port=5001, debug=True)
    else:
        app.run(host="localhost", port=int(cf_port), debug=True)

