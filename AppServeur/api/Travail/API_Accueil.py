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

from api.Travail.Base import *



#@app.route('/home/users', methods = ['POST']) #creation d'un nouvel utilisateur
def new_user():
    request.get_json(force=True)
    username, hpassword, pseudo = request.json.get('username'), request.json.get('hpassword'),\
                                  request.json.get('pseudo')
    print(f"Demande de création d'un nouvel utilisateur (username = {username}, "
          f"pseudo = {pseudo}) dans la base de données.")

    #-- on vérifie si un tel username n'existe pas déjà dans la DB
    if DAOuser.does_username_exist(username):
        print(f"L'identifiant ({username}) existe déjà dans la base de données.")
        response = {"status_code": http_codes.conflict, "message": "User already exists in the DB."} #error 409
        return make_reponse(response, http_codes.conflict)
    #-- on vérifie si un tel pseudo n'existe pas déjà dans la DB
    if DAOuser.does_pseudo_exist(pseudo):
        print(f"Le pseudo ({pseudo}) existe déjà dans la base de données.")
        response = {"status_code": http_codes.conflict, "message": "Pseudo already exists in the DB."} #error 409
        return make_reponse(response, http_codes.conflict)

    #-- on ajoute le nouvel utilisateur (username, pseudo, hpassword) à la DB Utilisateur
    DAOuser.add_user(username, pseudo, hpassword)
    print("utilisateur ajouté dans la table Utilisateur.")
    #-- on ajoute l'utilisateur à la db Score pour suivre ces classement
    DAOuser.add_user_score(pseudo)
    print("utilisateur ajouté dans la base Scores.")
    #-- on renvoit le code ok et le message d'ajout de l'utilisateur.
    response = {"status_code": http_codes.ok, "message": "L'utilisateur a bien été ajouté à la DB."}
    return make_reponse(response, http_codes.ok) #code 200

#@app.route('/home/connexion', methods = ['GET']) #connexion d'un utilisateur
def identification():
    request.get_json(force=True)
    username, password= request.json.get('username'), request.json.get('password')
    print(f"Demande d'identification (identifiant ={username}).")

    #-- on vérifie si un utilisateur avec cet identifiant existe dans la DB
    if not DAOuser.does_username_exist(username):
        print(f"L'identifiant founit ({username}) est incorrect.")
        response = {"status_code": http_codes.unauthorized, "message": "Username incorrect."} #error 401
        return make_reponse(response, http_codes.unauthorized)

    #-- on récupère le hpass associé à l'utilisateur et on le compare au hash du mdp fournit pour la connection
    stored_hpass = DAOuser.get_hpass_username(username)
    if not MDPgestion.verify_password(stored_hpass, password):
        print("Le mot de passe fournit ne correspond pas à celui stocké en base.")
        response = {"status_code": http_codes.unauthorized, "message": "Password incorrect."}  # error 401
        return make_reponse(response, http_codes.unauthorized)

    #-- on vérifie que l'utilisateur n'est pas déjà conencté
    if DAOuser.get_est_connecte(username): #l'utilisateur est déjà connecté
        print(f"L'utilisateur ({username}) est déjà connecté et ne peut donc pas se reconnecter.")
        response = {"status_code": http_codes.forbidden, "message": "User already connected."}  # error 403
        return make_reponse(response, http_codes.forbidden)

    #-------------------------- Connexion réussie -----------------------------
    #-- on update le statut "est_connecte" à True de l'utilisateur qui vient de se connecter
    DAOuser.update_est_connecte(username, username_or_pseudo = 'username', nouvel_etat = 'True')
    #-- on renvoit le code ok, le message et le pseudo
    pse = DAOuser.get_pseudo(username)
    print("Utilisateur connecté.")
    response = {"status_code": http_codes.ok, "message": "Connection réussie.", "pseudo": pse}
    return make_reponse(response, http_codes.ok)  # code 200

#@app.route('/home/deconnexion', methods = ['GET']) #deconnexion d'un utilisateur
def deconnect():
    request.get_json(force=True)
    pseudo = request.json.get('pseudo')
    print(f"Demande de déconenxion (pseudo = {pseudo}).")

    # -- on vérifie si un utilisateur avec ce pseudo existe dans la DB
    if not DAOuser.does_pseudo_exist(pseudo):
        print(f"Le pseudo ({pseudo}) du joueur qui demande sa déconnexion n'existe pas...")
        response = {"status_code": http_codes.unauthorized, "message": "Pseudo incorrect."}  # error 401
        return make_reponse(response, http_codes.unauthorized)

    #-- on update le statut "est_connecte" à False de l'utilisateur qui vient de se deco via son pseudo
    DAOuser.update_est_connecte(pseudo, username_or_pseudo = 'pseudo', nouvel_etat = 'False')
    print(f"Utilisateur (pseudo = {pseudo}) déconnecté")
    #-- on renvoit le code ok et le message.
    response = {"status_code": http_codes.ok, "message": "Déconnection réussie."}
    return make_reponse(response, http_codes.ok)  # code 200


