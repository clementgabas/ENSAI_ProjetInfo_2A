import requests
import json

class Player():

    def __init__(self, pseudo, id_salle, chef_salle, jeu):
        self.pseudo = pseudo
        self.id_salle = id_salle
        self.chef_salle = chef_salle
        self.jeu = jeu

    def choix_couleur(self):
        pass

    def ask_api_if_tour(self):
        dataPost = {"id_salle":self.id_salle,
                    "pseudo_joueur":self.pseudo}
        res = requests.get(url="http://localhost:9090/home/game/room/play", data=json.dumps(dataPost))

        if res.status_code == 200:
            return True
        else:
            return False


    def ask_api_if_partie_lancee(self):
        pass
