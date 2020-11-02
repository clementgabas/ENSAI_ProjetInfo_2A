import os
import traceback
import csv
import random
import json
import hashlib

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












@app.route("/", strict_slashes=False)
@app.route("/home")
def get():
    """
        Base route
    """
    response = {"status_code": http_codes.OK, "message": "Vous êtes bien sur l'Api jeux"}
    return make_reponse(response, http_codes.OK)

@app.route('/home/users', methods = ['POST'])
def new_user():
    print(request.get_json(force=True))
    username = request.json.get('username')
    password = request.json.get('password')
    pseudo = request.json.get('pseudo')

    if username is None or password is None:
        abort(400) # missing arguments


    try: #on vérifie si l'utilisateur existe
        con = sqlite3.connect("database/apijeux.db")
        cursor = con.cursor()
        cursor.execute("SELECT pseudo FROM Utilisateur WHERE identifiant = ?", (username,))
        ide = cursor.fetchone()
    except:
        print("ERROR : API.new_user : does user already exist")
        raise ConnectionAbortedError
    finally:
        con.close()

    if ide != None: #il existe déjà un utilisateur avec cet identifiant dans la db
        abort(401) #existing user
        #return jsonify ave les erreurs

    hpassword = password

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

    return print("c valide")

    #return jsonify({ 'username': username }), 201, {'Location': url_for('get_user', id = username, _external = True)}

















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
