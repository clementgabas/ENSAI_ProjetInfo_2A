from flask import request
from requests import codes as http_codes

import DAO.gestionClassement as DAOclassement

from api.Travail.Base import make_reponse


#----------------------------- Classement ------------------------------------------

#@app.route('/home/main/profil/classment/jeu', methods=['GET']) #affichage classement jeu de l'oie
def afficher_classement():
    """
    Fonction qui traite la requête d'affichage du classement d'un jeu.

    :return
    --------
    Code 200 :
        Affichage réussi.
    """

    request.get_json(force=True)
    nom_jeu = request.json.get("nom_jeu")
    pseudo = request.json.get("pseudo")
    print(f" Demande de {pseudo} d'accès au classement du jeu : {nom_jeu}")
    #-- on récupère le classement du jeu de l'oie
    classement_jeu = DAOclassement.afficher_classement_jeu(nom_jeu,pseudo)
    print(f"Récupération classement mondial du jeu : {nom_jeu}")
    classement_jeu_amis = DAOclassement.afficher_classement_jeu_friends(nom_jeu, pseudo)
    print(f"Récupération classement amis de {pseudo} du jeu : {nom_jeu}")
    #-- on renvoit le code ok, le message et le classement du jeu de l'oie
    response = {"status_code": http_codes.ok, "message": "Classement du jeu récupéré.",
                'classement_jeu': classement_jeu,'classement_jeu_amis': classement_jeu_amis}
    #response2 = {"status_code": http_codes.ok, "message": "Classement du l'oie récupéré.", 'classement_jeu_amis': classement_jeu_amis} #code 200#code 200 #####
    return make_reponse(response, http_codes.ok)  # code 200


#@app.route('/home/main/profil/classment/general', methods=['GET']) #affichage classement général
def afficher_classement_general():
    """
        Fonction qui traite la requête d'affichage du classement général.

        :return
        --------
        Code 200 :
            Affichage réussi.
        """
    request.get_json(force=True)
    pseudo = request.json.get("pseudo")
    print(f" Demande de {pseudo} d'accès au classement général")
    #-- on récupère le classement général
    classement_general = DAOclassement.afficher_classement_general(pseudo)
    print(f"Récupération classement mondial")
    classement_general_amis = DAOclassement.afficher_classement_general_friends(pseudo)
    print(f"Récupération classement amis de {pseudo}")
    # -- on renvoit le code ok, le message et le classement général
    response = {"status_code": http_codes.ok, "message": "Classement général récupéré.",
                "classement_general": classement_general, "classement_general_amis"
                                                          "": classement_general_amis}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200
#----------------------------- Classement ------------------------------------------


