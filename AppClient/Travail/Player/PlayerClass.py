import requests
import json
from tabulate import tabulate
from Player.UserClass import User
from RequestsTools.AddressTools import get_absolute_address, make_address


absolute_address = get_absolute_address()


class Player(User):

    def __init__(self, pseudo, jeu, id_salle, chef_salle):
        self.pseudo = pseudo
        self.id_salle = id_salle
        self.chef_salle = chef_salle
        self.jeu = jeu


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


    def creer_salle(self):
        dataPost = {'pseudo_chef_salle': self.pseudo, 'game': self.jeu}
        res = requests.post('http://localhost:9090/home/game/room', data=json.dumps(dataPost))

        if res.status_code == 200:
            id_salle = res.json()['id_salle']
            print(f"Une salle (numéro {id_salle}) vient d'être créée. Vos amis peuvent la rejoindre via son numéro.")
            Resultat = {"Statut" : True, "id_salle" : id_salle}
            return(Resultat)
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 500:
            print("erreur dans le code de l'api")
            Resultat = {"Statut": False}
            return (Resultat)
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut": False}
            return (Resultat)

    def rejoindre_salle(self,id_salle):

        dataPost = {'pseudo': self.pseudo, 'id_salle': id_salle, 'jeu':self.jeu}
        res = requests.put('http://localhost:9090/home/game/room', data=json.dumps(dataPost))

        if res.status_code == 200:
            print(f"Vous avez bien été ajouté à la salle {id_salle}.")
            Resultat = {"Statut": True, "id_salle": id_salle}
            return (Resultat)
        elif res.status_code == 401:
            print(f"Vous ne pouvez pas rejoindre la salle {id_salle} car elle est déjà pleine.")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 404:
            print("La salle demandée n'existe pas.")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 500:
            print("erreur dans le code de l'api")
            Resultat = {"Statut": False}
            return (Resultat)
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut": False}
            return (Resultat)

    def voir_membres_salle(self):
        relative_address = "/home/game/room"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'id_salle': self.id_salle}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["liste_membres"] = res.json()["liste_membres"]
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.voir_membres_salle")
        return Resultat

    def quitter_salle(self):
        relative_address = "/home/game/room"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {"pseudo": self.pseudo, "id_salle": self.id_salle, "est_chef_salle": self.chef_salle}
        res = requests.delete(adresse, data=json.dumps(dataPost))
        if res.status_code == 401:
            Resultat = self.update_resultat(False,"Vous êtes le chef de la salle! Vous ne pouvez pas la quitter tant qu'un autre utilisateur s'y trouve encore. Un capitaine quitte toujours son navire en dernier n'est-ce pas?")
        elif res.status_code == 200:
            Resultat = self.update_resultat(True, f"Vous avez quitté la salle {self.id_salle}")
        return Resultat