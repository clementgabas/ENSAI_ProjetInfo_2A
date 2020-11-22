import math

from flask import request

from requests import codes as http_codes

import DAO.gestionParties as DAOparties
import DAO.gestionParticipation as DAOparticipation
import DAO.gestionCoups as DAOcoups
import DAO.gestionScores as DAOscores

from jeuxservice.plateau.p4grid import GridP4
from jeuxservice.plateau.oiegrid import Dice, Tray
from jeuxservice.jeux.p4game import GameP4

from api.Travail.Base import make_reponse


#@app.route('/home/game/room/turns', methods=['GET']) #dsavoir si c'est son tour de jouer
def est_ce_mon_tour():
    """
    Fonction qui traite la requête de vérification si c'est le tour d'un utilisateur

    :returns
    --------
    Code 449 :
        - Si ce n'est pas le tour de l'utilisateur.
    Code 403 :
        - Si l'utilisateur ne peut pas jouer son tour.
    Code 200 :
        Si c'est le tour de l'utilisateur.
    """
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
    """
    Fonction qui traite la requête de passage de tour d'un joueur.

    :return
    --------
    Code 200 :
        La requète réussie.
    """
    request.get_json(force=True)
    id_partie, pseudo = request.json.get('id_salle'), request.json.get('pseudo')
    print(f"Le joueur {pseudo} passe son tour dans la salle {id_partie}")

    #-- on update aquiltour en faisant bien attention a ce qu'un foie que le dernier à jouer ça revient au premier
    DAOparties.update_aquiltour(id_partie)
    response = {"status_code": http_codes.ok, "message": "Aquiltour updaté"}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#@app.route("/home/game/room/grid", methods=["GET"]) #requetage pour obtenir l'etat de la grille
def get_grille():
    """
    Fonction qui traite la requête de recuperation de la grille de jeu.

    :return
    --------
    Code 200 :
        La requète réussie.
    """
    request.get_json(force=True)
    id_partie, jeu = request.json.get('id_partie'), request.json.get('jeu')
    print(f"La grille est demandée dans la salle {id_partie} pour le jeu {jeu}")

    #-- on requete la DB pour obtenir l'ensemble des coups qui ont eu lieu dans une partie
    liste_coups = DAOcoups.get_all_coups(id_partie)
    print("Liste des coups : " + str(liste_coups))

    if jeu.lower() == "p4":
        #-- on envoit cette liste à jeux service qui va simuler tous les coups et renvoyer la grille dans cet etat
        plateau = GridP4(numHeight=7, numWidth=7, tokenWinNumber=4) #pour l'instant, on ne travaille que avec des parties par default
        plateau.simulatation(liste_coups)
        grille = plateau.getGrid()
    elif jeu.lower() == 'oie':
        plateau = Tray(numofdice=2, numoffaces=6, nbBox=63, id_partie=id_partie) #pour le moment, on ne joue qu'avec des valeurs standards
        grille = plateau.simulation(liste_coups)
        print(f"grille oie : {grille}")

    print(f"La grille a été simulée dans la salle {id_partie}")

    #-- on recupère aussi une liste donnant les couleurs dans l'ordre pour l'affichage couleur
    #liste = [rouge, bleu, vert] car le joueur etant premier dans l'ordre a la couleur rouge, le 2nd vert, etc...
    liste_couleur = DAOparticipation.get_liste_couleur(id_partie)
    print(f"La liste des couleurs ordonnee fournit {liste_couleur}")

    response = {"status_code": http_codes.ok, "message": "Grille simulée", 'grid': grille, 'liste_couleur_ordonnee': liste_couleur}  # code 200
    return make_reponse(dict(response), http_codes.ok)  # code 200

#@app.route("/home/game/room/grid", methods=["POST"]) #requetage pour jouer son coup
def jouer_son_tour():
    """
    Fonction qui traite la requête "jouer son tour" d'un utilisateur

    :returns
    --------
    Code 401 :
        - Si l'identifiant fourni n'existe pas.
        - Si le mot de passe est incorrecte.
    Code 403 :
        - Si l'utilisateur est déjà connecté.
    Code 200 :
        La Connexion réussie.
    """
    request.get_json(force=True)
    id_partie, pseudo, jeu = request.json.get('id_partie'), request.json.get('pseudo'), request.json.get('jeu')
    position = request.json.get('position')

    if type(position) == float:
        dice1, dice2 = math.floor(position), round((position%1)*10)
        position2 = [dice1, dice2]

    print(f"L'utilisateur {pseudo} joue la position {position} pour le jeu {jeu}")
    if jeu.lower() == "p4":
        coup = {'player' : pseudo, 'id_partie': id_partie , 'colonne': position}
        print(
            f"L'utilisateur {pseudo} va jouer son tour dans la salle {id_partie} au P4. Il a joué dans la colonne {position}.")
    elif jeu.lower() == "oie":
        coup = {'player' : pseudo, 'id_partie': id_partie , 'dice1': position2[0], 'dice2': position2[1]}
        print(
            f"L'utilisateur {pseudo} va jouer son tour dans la salle {id_partie} au jeu de l'oie. Il a joué un {position2[0]} et un {position2[1]}.")

    #-- on demande a jeux service si le coup est valide
    if jeu.lower() == "p4":
        plateau = GridP4(numHeight=7, numWidth=7,
                         tokenWinNumber=4)  # pour l'instant, on ne travaille que avec des parties par default
        plateau.simulatation(DAOcoups.get_all_coups(id_partie))

        jeu = GameP4(id_partie)
        Resultat = jeu.is_coup_valide(coup=coup, gridClass=plateau)
    elif jeu.lower() == 'oie':
        if not 0<position2[0]<7 or not 0<position2[1]<7:
            print(f"Erreur dans les dés pour {pseudo} dans la salle {id_partie}")
            Resultat = {"Statut": False, "Message": "Au moins l'un des 2 dés à une valeur innapropriée."}
        else:
            Resultat = {"Statut": True, "Message": "Pas de problèmes dans les dés."}

    if not Resultat["Statut"]: #le coup n'est pas valide
        print(f"Le coup n'est pas valide")
        response = {"status_code": http_codes.forbidden, "message": Resultat["Message"]}  # code 403
        return make_reponse(response, http_codes.forbidden)  # code 403
    print("Le coup est valide")


    #-- on enregistre ce coup dans la bd
    last_coup = DAOcoups.get_last_coup(id_partie)[0] #valeur du num_turn_précédent
    DAOcoups.add_new_coup(id_partie, math.floor(last_coup)+1, pseudo, position, 1)
    print("Le coup a été enregistré dans la DB")
    response = {"status_code": http_codes.ok, "message": "Coup joué et ajouté à la DB"}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200

#@app.route("/home/game/room/grid", methods=["PUT"])
def demander_si_vainqueur():
    """
    Fonction qui traite la requête de vérification si il y a un vainqueur.

    :return
    --------
    Code 200 :
        Si il y a bien un vainqueur.
    """
    request.get_json(force=True)
    id_partie, jeu = request.json.get('id_partie'), request.json.get('jeu')
    print(f"Demande de savoir si la grille de la salle {id_partie} est gagnante dans le jeu {jeu} ")

    if jeu.lower() == 'p4':
        plateau = GridP4(numHeight=7, numWidth=7,
                         tokenWinNumber=4)  # pour l'instant, on ne travaille que avec des parties par default
        plateau.simulatation(DAOcoups.get_all_coups(id_partie))

        Bool = plateau.TestIfWin()

    elif jeu.lower()=='oie':
        Bool = False
        pass

    if Bool:
        print(f"La partie {id_partie} est gagnante")
    else:
        print(f"La partie {id_partie} n'est pas gagnante")

    response = {"status_code": http_codes.ok, "message": "", "is_winner": Bool}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200


#@app.route("/home/game/room/end", methods=["PUT"])
def gestion_fin_partie():
    """
    Fonction qui traite la requête de gestion de fin de partie.

    :return
    --------
    Code 200 :
        Requête bien effecuté.
    """

    request.get_json(force=True)
    id_partie, jeu, pseudo, win_bool, ami_anonyme = request.json.get('id_partie'), request.json.get('jeu').upper(), request.json.get('pseudo'), request.json.get('win_bool'), request.json.get('ami_anonyme')

    #-- on retire le joueur de la table participation
    #en fait, on ne le retire pas de la table participation sinon les fin de parties vont bug chez les autres vu que les simulations ne pourront plus marcher.
    #du coup, on met a jour le nb_de_place dans la table partie mais on ne retire pas de la table participation
    #et seulement quand on supprime la table partie, on supprime toutes les occurances dans la table participatipon

    nb_places_dispos = DAOparties.check_cb_places_libres(id_partie)
    DAOparties.update_parties_nb_place(id_partie, nb_places_dispos + 1)

    print(f"L'utilisateur {pseudo} a bien été retiré de la salle {id_partie}")
    nbr_places_restantes = DAOparties.check_cb_places_libres(id_partie)
    print(f"La salle {id_partie} a dorénavant {nbr_places_restantes} de libres.")
    if DAOparties.get_nbr_participants(id_partie)==0: #si c'était le dernier joueur dans la salle, on supprime la salle
        #avant de supprimer la salle, on récupère la liste de tous les joueurs de la salle
        liste_players = DAOparticipation.get_all_players(id_partie)
        print(f"Liste des joueurs dans la salle : " + str(liste_players))
        for player in liste_players:
            DAOparties.delete_from_participation(id_partie, player, -1)
        #on supprimer egalement tous les coups de la table Coups
        DAOcoups.delete_all_coups(id_partie)
        DAOparties.delete_partie(id_partie)
        print(f"La salle {id_partie} était vide et a donc été supprimée")

    #-- si le joueur a gagné la partie, on lui ajoute un dans la table scores
    if win_bool:
        nb_parties_gagnnes = DAOscores.get_nb_parties_gagnees(pseudo, jeu)
        DAOscores.update_nb_parties_gagnees(pseudo, jeu, nb_parties_gagnnes+1)
        print(f"L'utilisateur {pseudo} a dorenavant gagné {nb_parties_gagnnes+1} dans le jeu {jeu}")

    #-- on update les points
    DAOscores.update_score(pseudo, jeu, win_bool)

    response = {"status_code": http_codes.ok, "message": ""}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200
