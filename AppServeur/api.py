import os



from flask import Flask, jsonify, request, Blueprint
from flask_cors import CORS
from flask_restplus import Api, Resource
from flask_restplus import abort
from flask_caching import Cache
from loguru import logger
from requests import codes as http_codes
from api.commons import configuration



import DAO.gestionUser as DAOuser


import api.Travail.API_Accueil as APIhome
import api.Travail.API_Amis as APIfriend
import api.Travail.API_Classement as APIclassement
import api.Travail.API_Profil as APIprofil
import api.Travail.API_Salle as APIsalle
import api.Travail.API_Salon as APIsalon
import api.Travail.API_Partie as APIpartie

from api.Travail.Base import make_reponse


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

#-------------------------- main --------------------------------

@app.route("/", strict_slashes=False) #acceuil
@app.route("/home") #acceuil
def get():
    """
        Base route
    """
    response = {"status_code": http_codes.OK, "message": "Vous êtes bien sur l'Api jeux"}
    return make_reponse(response, http_codes.OK)

#---------------------------- APIhome -----------------------------------
@app.route('/home/users', methods = ['POST']) #creation d'un nouvel utilisateur
def new_user():
    return APIhome.new_user()


@app.route('/home/connexion', methods = ['GET']) #connexion d'un utilisateur
def identification():
    return APIhome.identification()


@app.route('/home/deconnexion', methods = ['GET']) #deconnexion d'un utilisateur
def deconnect():
    return APIhome.deconnect()

#----------------------------- APIhome -------------------------------------------
#----------------------------- APIfriend ---------------------------------------------

@app.route('/home/main/profil/friends', methods=['GET']) #affichage liste amis
def afficher_liste_amis():
    return APIfriend.afficher_liste_amis()

@app.route('/home/main/profil/friends', methods=['POST']) #ajout d'un ami
def ajout_ami():
    return APIfriend.ajout_ami()


@app.route('/home/main/profil/friends', methods=['DELETE']) #suppression d'un ami
def supp_ami():
    return APIfriend.supp_ami()
#----------------------------- APIfriend ---------------------------------------------

#----------------------------- APIprofil ------------------------------------------------

@app.route('/home/main/profil/user/pseudo', methods=['PUT']) #modification du pseudo
def modif_pseudo():
    return APIprofil.modif_pseudo()

@app.route('/home/main/profil/user/password', methods=['PUT']) #modification du mot de passe
def modif_password():
    return APIprofil.modif_password()

@app.route('/home/main/profil/user/stat', methods=['GET']) #afficher stat perso
def afficher_stats_perso():
    return APIprofil.afficher_stats_perso()

@app.route('/home/main/profil/user/stat', methods=['PUT']) #reinitialiser stat perso
def modifier_stats_perso():
    return APIprofil.modifier_stats_perso()

#----------------------------- APIprofil ------------------------------------------------

#----------------------------- APIclassement ------------------------------------------

@app.route('/home/main/profil/classment/jeu', methods=['GET']) #affichage classement jeu de l'oie
def afficher_classement():
    return APIclassement.afficher_classement()


@app.route('/home/main/profil/classment/general', methods=['GET']) #affichage classement général
def afficher_classement_general():
    return APIclassement.afficher_classement_general()
#----------------------------- APIclassement ------------------------------------------

#----------------------------- APIsalle -------------------------------------------
@app.route('/home/game/room', methods=['POST'])
def creer_salle():
    return APIsalle.creer_salle()

@app.route('/home/game/room', methods=['PUT'])
def rejoindre_salle():
    return APIsalle.rejoindre_salle()

@app.route('/home/game/room', methods=['DELETE'])
def quitter_salle():
    return APIsalle.quitter_salle()

@app.route('/home/game/room', methods=['GET'])
def voir_membres_salle():
    return APIsalle.voir_membres_salle()


#----------------------------- APIsalle -------------------------------------------
#----------------------------- APIsalon -------------------------------------------

@app.route('/home/game/room/settings', methods=['GET']) #recup de parametre
def get_param_p4():
    return APIsalon.get_param_p4()

@app.route('/home/game/room/settings', methods=['POST']) #ajout de parametre
def ajout_param_partie_P4():
    return APIsalon.ajout_param_partie_P4()

@app.route('/home/game/room/settings', methods=['PUT']) #modif de parametre
def maj_param_partie_p4():
    return APIsalon.maj_param_partie_p4()

@app.route("/home/game/room/colors", methods=["GET"])
def get_liste_couleur_dispos():
    return APIsalon.get_liste_couleur_dispos()

@app.route("/home/game/room/colors", methods=["POST"])
def ajout_couleur():
    return APIsalon.ajout_couleur()

@app.route('/home/game/room/turns', methods=['POST']) #dire qu'on est pret à jouer
def je_suis_pret():
    return APIsalon.je_suis_pret()

@app.route('/home/game/room/launch', methods=['GET']) #savoir si on peut lancer la partie pour le chef
def gestion_tour_lancement_partie():
    return APIsalon.gestion_tour_lancement_partie()

@app.route('/home/game/room/launch', methods=['POST'])
def lancer_partie():
    return APIsalon.lancer_partie()
#----------------------------- APIsalon -------------------------------------------

#----------------------------- APIpartie -------------------------------------------

@app.route('/home/game/room/turns', methods=['GET']) #dsavoir si c'est son tour de jouer
def est_ce_mon_tour():
    return APIpartie.est_ce_mon_tour()

@app.route('/home/game/room/turns', methods=['PUT']) #passer son tour et maj la db pour savoir a qui ca sera le tour apres
def passer_son_tour():
    return APIpartie.passer_son_tour()

@app.route("/home/game/room/grid", methods=["GET"]) #requetage pour obtenir l'etat de la grille
def get_grille():
    return APIpartie.get_grille()

@app.route("/home/game/room/grid", methods=["POST"]) #requetage pour jouer son coup
def jouer_son_tour():
    return APIpartie.jouer_son_tour()

@app.route("/home/game/room/grid", methods=["PUT"]) #requetage pour savoir si il y a un winner
def demander_si_vainqueur():
    return APIpartie.demander_si_vainqueur()

@app.route("/home/game/room/end", methods=["PUT"]) #-- fonction qui nous retire de la table participation pour cette partie,
        # qui update si on a gagné notre nb de parties gagnees dans la table score
        # et qui update notre score (si la partie est anonyme
def gestion_fin_partie():
    return APIpartie.gestion_fin_partie()


#----------------------------- APIpartie -------------------------------------------









#---------------------------------------------------------
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == "__main__":
    DAOuser.put_all_users_disconnected()
    #cf_port = os.getenv("PORT")
    cf_port = conf["port"]
    if cf_port is None:
        app.run(host="localhost", port=5001, debug=True)
    else:
        app.run(host="localhost", port=int(cf_port), debug=True)

