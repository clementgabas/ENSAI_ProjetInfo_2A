from flask import request
from requests import codes as http_codes

import api.travailMDP.testmdp as MDPgestion
import DAO.gestionUser as DAOuser

from api.Travail.Base import make_reponse


#----------------------------- USER ------------------------------------------
#@app.route('/home/main/profil/user/pseudo', methods=['PUT']) #modification du pseudo
def modif_pseudo():
    """
    Fonction qui traite la requête de modification de pseudo.

    :returns
    --------
    Code 409 :
        Si le pseudo demandé est déjà utilisé.
    Code 200 :
        Si le pseudo a bien été modifié.

    """
    request.get_json(force=True)
    old_pseudo, new_pseudo = request.json.get('old_pseudo'), request.json.get('new_pseudo')
    print(f"Demande de pseudo = {old_pseudo} de modifier son pseudo en pseudo = {new_pseudo}.")
    #-- on vérifie si le new_pseudo est libre
    if DAOuser.does_pseudo_exist(new_pseudo):
        print(f"Le pseudo ({new_pseudo}) est déja pris par un autre utilisateur.")
        response = {"status_code": http_codes.conflict, "message": "Le pseudo demandé est déjà utilisé."}  # code 409
        return make_reponse(response, http_codes.conflict)  # code 409

    # -- on effectue la procédure qui uptade le pseudo
    DAOuser.update_pseudo(old_pseudo, new_pseudo)
    print(f"{new_pseudo} a bien été défini comme nouveau pseudo")
    # -- on renvoit le code ok et le message de suppression de l'ami.
    response = {"status_code": http_codes.ok, "message": "pseudo mis à jour."}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#@app.route('/home/main/profil/user/password', methods=['PUT']) #modification du mot de passe
def modif_password():
    """
    Fonction qui traite la requête de modification de mot de passe.

    :returns
    --------
    Code 401 :
        Si l'ancien mot de passe entré n'est pas le bon.
    Code 200 :
        Si le mot de passe a bien été modifié.

    """
    request.get_json(force=True)
    pseudo, old_password, new_password = request.json.get('pseudo'), request.json.get('old_password'),\
                                         request.json.get('new_password')
    print(f"Demande de modification de mot de passe du pseudo = {pseudo}.")
    #-- on vérifie si l'ancien mdp correspond bien au mdp enregistré pour le pseudo
        #-- on recupere le hpass stocké
    stored_hpass = DAOuser.get_hpass_pseudo(pseudo)
    print(stored_hpass)
        #-- on compare les hpass
    if not MDPgestion.verify_password(stored_hpass, old_password):
        print(f"L'ancien mot de passe est incorrect du pseudo = {pseudo}. ")
        response = {"status_code": http_codes.unauthorized, "message": "Password incorrect."}  # error 401
        return make_reponse(response, http_codes.unauthorized)

    new_hpass = MDPgestion.hacherMotDePasse(new_password)
    #-- on modifie le mdp dans la db utilisateur
    DAOuser.update_password(pseudo, new_hpass)
    print(f"Le mot de passe du pseudo = {pseudo} a bien été mis à jour.")
    # -- on renvoit le code ok et le message de suppression de l'ami.
    response = {"status_code": http_codes.ok, "message": "mdp mis à jour."}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200


#@app.route('/home/main/profil/user/stat', methods=['GET']) #afficher stat perso
def afficher_stats_perso():
    """
    Fonction qui traite la requête d'affichage des statistiques personnelles d'un utilisateur.

    :return
    --------
    Code 200 :
        Si la requête est bien éffectuée.

    """
    request.get_json(force=True)
    pseudo = request.json.get('pseudo')
    print(f"Demande d'affichage des statistiques personnelles du pseudo = {pseudo}.")
    #-- on recupere les statistique personnel de l'utilisateur 'pseudo'
    stat_perso = DAOuser.get_stat(pseudo)
    print(f"Affichage des statistiques personnelles du pseudo = {pseudo}.")
    #-- on renvoie un message de reussite
    response = {"status_code": http_codes.ok, "message": "Statistiques personnelles récupérées.",
                'Statistiques personnelles': stat_perso}  # code 200
    return make_reponse(response, http_codes.ok)

#@app.route('/home/main/profil/user/stat', methods=['PUT']) #reinitialiser stat perso
def modifier_stats_perso():
    """
        Fonction qui traite la requête de réinitialisation des statistiques personnelles d'un utilisateur.

        :return
        --------
        Code 200 :
            Si la requête est bien éffectuée.

        """
    request.get_json(force=True)
    pseudo = request.json.get('pseudo')
    print(f"Demande de réitialisation des statistiques personnelles du pseudo = {pseudo}.")
    # -- on réinitialise les statistique personnel de l'utilisateur 'pseudo'
    DAOuser.update_stat(pseudo)
    print(f"Statistiques personnelles du pseudo = {pseudo} réinitialisées.")
    # -- on renvoie un msg de réussite
    response = {"status_code": http_codes.ok, "message": "Statistiques personnelles réinitialisées."}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#----------------------------- USER ------------------------------------------

