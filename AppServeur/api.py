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

from travailMDP.testmdp import *
import DAO.gestionUser as DAOuser
import DAO.gestionAmis as DAOfriend


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

@app.route('/home/users', methods = ['POST']) #creation d'un nouvel utilisateur
def new_user():
    request.get_json(force=True)
    username, hpassword, pseudo = request.json.get('username'), request.json.get('hpassword'), request.json.get('pseudo')

    try: #on vérifie si l'utilisateur existe
        con = sqlite3.connect("database/apijeux.db")
        cursor, cursor2 = con.cursor(), con.cursor()
        cursor.execute("SELECT pseudo FROM Utilisateur WHERE identifiant = ?", (username,))
        cursor2.execute("SELECT identifiant FROM Utilisateur WHERE pseudo = ?", (pseudo,))
        ide = cursor.fetchone()
        pse = cursor2.fetchone()
    except:
        print("ERROR : API.new_user :")
        raise ConnectionAbortedError
    finally:
        con.close()

    if ide != None: #il existe déjà un utilisateur avec cet identifiant dans la db
        response = {"status_code": http_codes.conflict, "message": "User already exists in the DB."} #error 409
        return make_reponse(response, http_codes.conflict)
    if pse != None: #il existe deja un user avec ce pseudo
        response = {"status_code": http_codes.conflict, "message": "Pseudo already exists in the DB."} #error 409
        return make_reponse(response, http_codes.conflict)

    con = sqlite3.connect("database/apijeux.db")
    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO Utilisateur (pseudo, identifiant, mdp, nbr_parties_jouees, nbr_parties_gagnees, est_connecte, en_file, en_partie) VALUES (?, ?, ?, 0, 0, 'False', 'False', 'False')", (pseudo, username, hpassword,))
        con.commit()
    except:
        print("ERROR : API.new_user : add user into db")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

    response = {"status_code": http_codes.ok, "message": "L'utilisateur a bien été ajouté à la DB."}
    return make_reponse(response, http_codes.ok) #code 200

@app.route('/home/connexion', methods = ['GET']) #connexion d'un utilisateur
def identification():
    request.get_json(force=True)
    username, password= request.json.get('username'), request.json.get('password')

    try: #on vérifie si l'utilisateur existe et s'il correspond au mot de passe
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor.execute("SELECT pseudo, mdp FROM Utilisateur WHERE identifiant = ?", (username,))
        res = cursor.fetchone()
    except:
        print("ERROR : API.identification :")
        raise ConnectionAbortedError
    finally:
        con.close()

    if res == None: #un tel ide avec ce mdp n'existe pas
        response = {"status_code": http_codes.unauthorized, "message": "Username incorrect."} #error 401
        return make_reponse(response, http_codes.unauthorized)
    pse, storedMDP = res[0], res[1]
    if not verify_password(storedMDP, password):
        response = {"status_code": http_codes.unauthorized, "message": "Password incorrect."}  # error 401
        return make_reponse(response, http_codes.unauthorized)

    #-- Connexion réussie
    try: #on update le statut "est_connecte" à True de l'utilisateur qui vient de se co
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor.execute("UPDATE Utilisateur SET est_connecte = 'True' WHERE identifiant = ?", (username,))
        con.commit()
    except:
        print("ERROR : API.identification :")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()
    response = {"status_code": http_codes.ok, "message": "Connection réussie.", "pseudo": pse}
    return make_reponse(response, http_codes.ok)  # code 200

@app.route('/home/deconnexion', methods = ['GET']) #deconnexion d'un utilisateur
def deconnect():
    request.get_json(force=True)
    pseudo = request.json.get('pseudo')
    try: #on update le statut "est_connecte" à False de l'utilisateur qui vient de se deco
        con = sqlite3.connect("database/apijeux.db")
        cursor= con.cursor()
        cursor.execute("UPDATE Utilisateur SET est_connecte = 'False' WHERE pseudo = ?", (pseudo,))
        con.commit()
    except:
        print("ERROR : API.deconnexion :")
        con.rollback()
        raise ConnectionAbortedError
    finally:
        con.close()

    response = {"status_code": http_codes.ok, "message": "Déconnection réussie."}
    return make_reponse(response, http_codes.ok)  # code 200

@app.route('/home/main/profil/friends', methods=['GET'])
def afficher_liste_amis():
    request.get_json(force=True)
    pseudo = request.json.get('pseudo')

    #-- on récupère la liste des amis
    liste_amis = DAOfriend.afficher_liste_amis(pseudo)
    #-- on renvoit le code ok, le message et la liste des amis.
    response = {"status_code": http_codes.ok, "message": "Liste des amis récupérée.", 'liste_amis': liste_amis} #code 200
    return make_reponse(response, http_codes.ok)  # code 200

@app.route('/home/main/profil/friends', methods=['POST'])
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

@app.route('/home/main/profil/friends', methods=['DELETE'])
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
    #cf_port = os.getenv("PORT")
    cf_port = conf["port"]
    if cf_port is None:
        app.run(host="localhost", port=5001, debug=True)
    else:
        app.run(host="localhost", port=int(cf_port), debug=True)

