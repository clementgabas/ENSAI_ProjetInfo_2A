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
import DAO.gestionAmis as DAOfriend

from api.Travail.Base import *


#----------------------------- Friends ---------------------------------------------
#@app.route('/home/main/profil/friends', methods=['GET']) #affichage liste amis
def afficher_liste_amis():
    """
    Fonction qui traite la requête d'affichage la liste d'amis.

    :return
    --------
    Code 200 :
        Affichage réussie.
    """
    request.get_json(force=True)
    pseudo = request.json.get('pseudo')
    print(f"Demande d'affichage de la liste d'amis de pseudo = {pseudo}.")

    #-- on récupère la liste des amis
    liste_amis = DAOfriend.afficher_liste_amis(pseudo)
    print(f"Liste d'amis transmise.")
    #-- on renvoit le code ok, le message et la liste des amis.
    response = {"status_code": http_codes.ok, "message": "Liste des amis récupérée.", 'liste_amis': liste_amis} #code 200
    return make_reponse(response, http_codes.ok)  # code 200

#@app.route('/home/main/profil/friends', methods=['POST']) #ajout d'un ami
def ajout_ami():
    """
    Fonction qui traite la requête d'ajout d'un utilisateur dans la liste d'amis.

    :returns
    --------
    Code 404 :
        - Si l'identifiant fourni n'existe pas.
    Code 208 :
        - Si l'utilisateur est déjà dans la liste d'amis.
    Code 200 :
        Ajout réussi.
    """
    request.get_json(force=True)
    pseudo, pseudo_ami = request.json.get('pseudo'), request.json.get('pseudo_ami')
    print(f"Demande de pseudo = {pseudo} d'ajouter pseudo = {pseudo_ami} à sa liste d'amis.")

    #-- vérification si un utilisateur avec le pseudo_ami existe dans la DB
    if not DAOuser.does_pseudo_exist(pseudo_ami):
        print(f"Le pseudo ({pseudo_ami}) à ajouter à la liste d'amis n'existe pas.")
        response = {"status_code": http_codes.not_found, "message": "L'ami à ajouter n'existe pas."}  # code 404
        return make_reponse(response, http_codes.not_found)  # code 404

    #-- on vérifie si pseudo n'est pas déjà ami avec pseudo_ami
    if DAOfriend.are_pseudos_friends(pseudo, pseudo_ami):
        print(f"{pseudo} est déjà ami avec {pseudo_ami}.")
        response = {"status_code": http_codes.already_reported, "message": "L'amitié existe déjà."}  # code 208
        return make_reponse(response, http_codes.already_reported)  # code 208

    #-- on effectue la procédure qui ajoute le lien d'amitié
    DAOfriend.add_amitie(pseudo, pseudo_ami)
    print(f"{pseudo_ami} a bien été ajouté à la liste d'ami de {pseudo}.")
    #-- on renvoit le code ok et le message d'ajout de l'ami.
    response = {"status_code": http_codes.ok, "message": "Ami ajouté."}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#@app.route('/home/main/profil/friends', methods=['DELETE']) #suppression d'un ami
def supp_ami():
    """
    Fonction qui traite la requête de suppression d'un utilisateur de la liste d'amis.

    :returns
    --------
    Code 404 :
        - Si l'identifiant fourni n'existe pas.
    Code 208 :
        - Si l'utilisateur n'est pas dans la liste d'amis.
    Code 200 :
        Suppression réussie.
    """
    request.get_json(force=True)
    pseudo, pseudo_ami = request.json.get('pseudo'), request.json.get('pseudo_ami')
    print(f"Demande de pseudo = {pseudo} de supprimer pseudo = {pseudo_ami} de sa liste d'amis.")

    #-- vérification si un utilisateur avec le pseudo_ami existe dans la DB
    if not DAOuser.does_pseudo_exist(pseudo_ami):
        print(f"Le pseudo ({pseudo_ami}) à supprimer de la liste d'amis n'existe pas.")
        response = {"status_code": http_codes.not_found, "message": "L'ami à supprimer n'existe pas."}  # code 404
        return make_reponse(response, http_codes.not_found)  # code 404

    # -- on vérifie si pseudo est bien ami avec pseudo_ami
    if not DAOfriend.are_pseudos_friends(pseudo, pseudo_ami):
        print(f"{pseudo} n'est déjà pas ami avec {pseudo_ami}.")
        response = {"status_code": http_codes.already_reported, "message": "L'amitié n'existe pas."}  # code 208
        return make_reponse(response, http_codes.already_reported)  # code 208

    # -- on effectue la procédure qui supprime le lien d'amitié
    DAOfriend.sup_amitie(pseudo, pseudo_ami)
    print(f"{pseudo_ami} a bien été supprimé de la liste d'ami de {pseudo}.")
    #-- on renvoit le code ok et le message de suppression de l'ami.
    response = {"status_code": http_codes.ok, "message": "Ami supprimé."}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200
#----------------------------- Friends ---------------------------------------

