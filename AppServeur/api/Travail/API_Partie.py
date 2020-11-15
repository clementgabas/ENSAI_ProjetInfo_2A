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

import DAO.gestionParties as DAOparties
import DAO.gestionParticipation as DAOparticipation
import DAO.gestionCoups as DAOcoups

from api.Travail.Base import *


#@app.route('/home/game/room/turns', methods=['GET']) #dsavoir si c'est son tour de jouer
def est_ce_mon_tour():
    request.get_json(force=True)
    id_partie, pseudo = request.json.get('id_salle'), request.json.get('pseudo')
    print(f"L'utilisateur {pseudo} demande si c'est son tour dans la salle {id_partie}.")
    aquiltour = DAOparties.get_aquiltour(id_partie)
    self_ordre = DAOparticipation.get_position_ordre(pseudo, id_partie)
    #mettre condition prochain tour != 1
    if aquiltour == self_ordre: #c'est le tour du joueur qui demande
        print(f"C'est bien le tour de l'utilisateur {pseudo} dans la salle {id_partie}.")
        old_coup = DAOcoups.get_old_coup(id_partie,pseudo)
        last_coup = DAOcoups.get_last_coup(id_partie)[0]
        if old_coup[4] == 1 :
            print(f"L'utilisateur {pseudo} peut jouer son tour dans la salle {id_partie}")
            response = {"status_code": http_codes.ok, "message": "C'est ton tour"}  # code 200
            return make_reponse(response, http_codes.ok)  # code 200
        else :
            print(f"L'utilisateur {pseudo} n'a pas le droit de jouer son tour dans la salle {id_partie} et doit donc passer son tour.")
            DAOcoups.add_new_coup(id_partie, last_coup+1 , pseudo, old_coup[3], old_coup[4]+1)
            response = {"status_code": http_codes.forbidden,
                        "message": "C'est votre tour, mais vous ne pouvez pas jouer"}  # code 403
            return make_reponse(response, http_codes.forbidden)   # code 403
    else: #ce n'est pas son tour de jouer
        print(f"Ce n'est pas le tour de l'utilisateur {pseudo} dans la salle {id_partie}.")
        response = {"status_code": http_codes.retry_with, "message": "Ce n'est pas votre tour"}  # code 449
        return make_reponse(response, http_codes.retry_with)  # code 449

#@app.route('/home/game/room/turns', methods=['PUT']) #passer son tour et maj la db pour savoir a qui ca sera le tour apres
def passer_son_tour():
    request.get_json(force=True)
    id_partie, pseudo = request.json.get('id_salle'), request.json.get('pseudo')

    #-- on update aquiltour en faisant bien attention a ce qu'un foie que le dernier à jouer ça revient au premier
    DAOparties.update_aquiltour(id_partie)
    response = {"status_code": http_codes.ok, "message": "Aquiltour updaté"}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200



