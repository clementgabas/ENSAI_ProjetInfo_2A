

from flask import request

from requests import codes as http_codes


import DAO.gestionParties as DAOparties
import DAO.gestionParametres as DAOparametres
import DAO.gestionParticipation as DAOparticipation
import DAO.gestionScores as DAOscores

from api.Travail.Base import make_reponse

#@app.route('/home/game/room/settings', methods=['GET']) #ajout de parametre
def get_param_p4():
    """
    Fonction qui traite la requête de verification de non existence des parametres la partie de p4

    :returns
    --------
    Code 409 :
        Si des parametres ont déjà été définis
    Code 200 :
        Si des parametres n'ont pas encore été définis.
    """
    request.get_json(force=True)
    id_partie, duree_tour, condition_victoire, Taille_plateau = request.json.get('id_partie'), \
                                                                request.json.get('duree_tour'), \
                                                                request.json.get('condition_victoire'), \
                                                                request.json.get('Taille_plateau')
    if DAOparametres.verif_parametre(id_partie) == False:
        response = {"status_code": http_codes.ok, "message": "Il n'y a pas de parametres actuellement"}  # code 200
        return make_reponse(response, http_codes.ok)  # code 200
    elif DAOparametres.verif_parametre(id_partie) == True :
        response = {"status_code": http_codes.conflict, "message": "Il y a déja des parametre à cette partie, methode PUT conséillé"} #code409
        return make_reponse(response, http_codes.conflict) #code409

#@app.route('/home/game/room/settings', methods=['POST']) #ajout de parametre
def ajout_param_partie_P4():
    """
    Fonction qui traite la requête d'jout des parametres la partie de p4

    :return
    -------
    Code 200 :
        Si des parametres ont bien été ajoutés.
    """
    request.get_json(force=True)
    id_partie, duree_tour, condition_victoire, Taille_plateau  = request.json.get('id_partie'), \
                                                                 request.json.get('duree_tour'), \
                                                                 request.json.get('condition_victoire'),  \
                                                                 request.json.get('Taille_plateau')

    DAOparametres.add_parametre(id_partie, duree_tour, condition_victoire, Taille_plateau)
    print(f"Les paramètres suivants : Durée d'un tour : {duree_tour} secondes \n Condition de victoire : aligner "
          f"{condition_victoire} jetons \n Taille du plateau : {Taille_plateau} \n "
          f"ont a bien été définis pour la partie {id_partie}")
    response = {"status_code": http_codes.ok, "message": "Parametre bien ajouté"}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#@app.route('/home/game/room/settings', methods=['PUT']) #modif de parametre
def maj_param_partie_p4():
    """
    Fonction qui traite la requête de mise à jour des parametres la partie de p4

    :return
    -------
    Code 200 :
        Si des parametres ont bien été mis à jour.
    """
    request.get_json(force=True)
    id_partie, duree_tour, condition_victoire, Taille_plateau = request.json.get('id_partie'), \
                                                                request.json.get('duree_tour'), \
                                                                request.json.get('condition_victoire'), \
                                                                request.json.get('Taille_plateau')
    DAOparametres.put_parametre(id_partie, duree_tour, condition_victoire, Taille_plateau)
    print(f"Les paramètres suivants : Durée d'un tour : {duree_tour} secondes \n Condition de victoire : aligner "
          f"{condition_victoire} jetons \n Taille du plateau : {Taille_plateau} \n "
          f"ont a bien été mis à jour pour la partie {id_partie}")
    response = {"status_code": http_codes.ok, "message": "Parametre bien mis à jour"}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#----------------------------- param/ game -------------------------------------------
#----------------------------- home/game -------------------------------------------


#@app.route("/home/game/room/colors", methods=["GET"])
def get_liste_couleur_dispos():
    """
    Fonction qui traite la requête de verification des couleurs disponibles pour la partie.

    :returns
    --------
    Code 403 :
        Si il n'y a pas assez de joueur pour lancer la partie
    Code 200 :
        Si la requête peut être correctement effecutée.
    """
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
    return make_reponse(response, http_codes.ok) # Code 200
#----------------------------- home/game -------------------------------------------
#----------------------------- Lunch/game -------------------------------------------

#@app.route("/home/game/room/colors", methods=["POST"])
def ajout_couleur():
    """
    Fonction qui traite la requête de la selection d'une couleur par un utilisateur pour la partie.

    :returns
    --------
    Code 409 :
        Si la couleur sélectionné a déja été choisie par quelqu'un d'autre.
    Code 200 :
        Si la requête est correctement effecutée.
    """
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
    """
    Fonction qui traite la requête de mis à jour du status d'être prêt.

    :returns
    --------
    Code 400 :
        Si la il y a un problème dans le jeu en entrée.
    Code 200 :
        Si la requête est correctement effecutée.
    """
    request.get_json(force=True)
    pseudo, id_salle, est_chef, jeu = request.json.get('pseudo'), request.json.get('id_salle'), request.json.get('est_chef'), request.json.get('jeu')
    print(f"L'utilisateur {pseudo} demande à être prêt dans la salle {id_salle}.")

    #-- on update le est_pret a True dans la table Participation
    DAOparticipation.update_est_pret(pseudo, id_salle, 'True')
    #-- on update le nombre de parties jouees
    if jeu.lower() == 'p4':
        old_number = DAOscores.get_nb_parties_jouees(pseudo, "P4")
        DAOscores.update_nb_parties_jouees(pseudo, "P4", old_number+1)
    elif jeu.lower() == "oie":
        old_number = DAOscores.get_nb_parties_jouees(pseudo, "Oie")
        DAOscores.update_nb_parties_jouees(pseudo, "Oie", old_number + 1)
    else:
        print("erreur dans le nom du jeu")
        response = {"status_code": http_codes.bad, "message": "Erreur dans le jeu"}  # code 400
        return make_reponse(response, http_codes.bad)  # code 400
    print(f"L'utilisateur {pseudo} a maintenant joué {old_number + 1} parties de {jeu}")

    #-- on fait choisir la couleur à l'utilisateur
    couleur = DAOparticipation.get_couleur(pseudo, id_salle)
    print(f"L'utilisateur {pseudo} est pret dans la table Participation pour la partie {id_salle} avec la couleur {couleur}.")
    #-- on update l'ordre de jeu dans la table Participation
    DAOparticipation.update_ordre(pseudo, id_salle)
    print(f"L'utilisateur {pseudo} s'est vu attribué son ordre de jeu pour la partie {id_salle}.")

    response = {"status_code": http_codes.ok, "message": "Utilisateur pret."}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#@app.route('/home/game/room/launch', methods=['GET']) #savoir si on peut lancer la partie pour le chef
def gestion_tour_lancement_partie():
    """
    Fonction qui traite la requête de mis à jour du status d'être prêt.

    :returns
    --------
    Code 406 :
        Si au moins un participant n'est pas pret.
    Code 200 :
        Si tous les participants sont prets.
    Code 401 :
        Si il n'y a plus de chef dans la partie.
    """
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
    """
    Fonction qui traite la requête de lancement de partie.

    :return
    -------
    Code 200 :
        Si la requête a bien été effectuée.
    """
    request.get_json(force=True)
    id_partie = request.json.get('id_salle')
    #-- on DAO pour update la table partie et mettre statut = 'en cours'
    DAOparties.lancer_partie(id_partie)
    response = {"status_code": http_codes.ok, "message": "Partie lancée"}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200



