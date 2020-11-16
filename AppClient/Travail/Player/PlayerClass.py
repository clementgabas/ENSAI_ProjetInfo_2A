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
        self.est_chef = chef_salle
        self.jeu = jeu





    def creer_salle(self):
        relative_address = "/home/game/room"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo_chef_salle': self.pseudo, 'game': self.jeu}
        res = requests.post(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True, f"Une salle (numéro {res.json()['id_salle']}) vient d'être créée. Vos amis peuvent la rejoindre via son numéro.")
            Resultat["id_salle"] = res.json()['id_salle']
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def rejoindre_salle(self,id_salle):
        relative_address = "/home/game/room"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo, 'id_salle': id_salle, 'jeu':self.jeu}
        res = requests.put(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True, f"Vous avez bien été ajouté à la salle {id_salle}.")
            Resultat["id_salle"] = id_salle
        elif res.status_code == 401:
            Resultat = self.update_resultat(False, f"Vous ne pouvez pas rejoindre la salle {id_salle} car elle est déjà pleine.")
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "La salle demandée n'existe pas.")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

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

        dataPost = {"pseudo": self.pseudo, "id_salle": self.id_salle, "est_chef_salle": self.est_chef}
        res = requests.delete(adresse, data=json.dumps(dataPost))
        if res.status_code == 401:
            Resultat = self.update_resultat(False,"Vous êtes le chef de la salle! Vous ne pouvez pas la quitter tant qu'un autre utilisateur s'y trouve encore. Un capitaine quitte toujours son navire en dernier n'est-ce pas?")
        elif res.status_code == 200:
            Resultat = self.update_resultat(True, f"Vous avez quitté la salle {self.id_salle}")
        return Resultat

    def get_liste_couleurs_dispos(self):
        relative_address = "/home/game/room/colors"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'id_salle':self.id_salle}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["liste_couleurs_dispos"] = res.json()["liste_couleurs_dispos"]
        elif res.status_code == 403:
            Resultat = self.update_resultat(False, "Vous ne pouvez pas être pret car vous êtes seuls dans la salle. Il faut être au moins 2.")
        else:
            Resultat = self.update_resultat(False, "erreur ndas PlayerClass.get_liste_couleurs_dispos")
        return Resultat

    def choix_couleur(self, couleur_choisie):
        relative_address = "/home/game/room/colors"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'id_salle':self.id_salle, 'pseudo':self.pseudo, 'couleur':couleur_choisie}
        res = requests.post(adresse, data=json.dumps(dataPost))

        if res.status_code == 409: #la couleur a été choisie entre temps
            Resultat = self.update_resultat(False, "La couleur demandée a été choisie entre temps par un autre utilisateur. Veuillez réessayer svp.")
        elif res.status_code == 200:
            Resultat = self.update_resultat(True)
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.choix_couleur")
        return Resultat

    def etre_pret(self):
        relative_address = "/home/game/room/turns"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo':self.pseudo,'id_salle':self.id_salle, 'est_chef':self.est_chef}
        res = requests.post(adresse, data=json.dumps(dataPost))
        if res.status_code == 200:
            Resultat = self.update_resultat(True, "Vous êtes prêts!")
        else:
            Resultat = self.update_resultat(False, "erreur ndas PlayerClass.choix_couleur")
        return Resultat

    def is_everyone_ready(self):
        relative_address = "/home/game/room/launch"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo, 'id_salle': self.id_salle, 'est_chef': self.est_chef}
        # -- on requete pour savoir si tout le monde est pret dans la salle
        res = requests.get(adresse, data=json.dumps(dataPost))
        # -- si on récupère un "tout le monde est pret", on lance la partie
        if res.status_code == 200:
            Resultat = self.update_resultat(True, "Tout le monde est prêt dans la salle. La partie va se lancer.")
        else:
            Resultat = self.update_resultat(False, "En attente que tous les participants soient prêts pour lancer la partie.")
        return Resultat

    def lancer_partie(self):
        relative_address = "/home/game/room/launch"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'id_salle': self.id_salle}
        res = requests.post(adresse, data=json.dumps(dataPost))  # dao pour modifier dans la table Partie le statut à en cours
        if res.status_code == 200:
            # la partie est lancée, on peut requeter pour savoir si c'est son tour
            Resultat = self.update_resultat(True)
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.lancer_partie")
        return Resultat

    def passer_tour(self):
        relative_address = "/home/game/room/turns"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo, 'id_salle': self.id_salle}
        res = requests.put(adresse, data=json.dumps(dataPost))
        if res.status_code == 200:
            Resultat = self.update_resultat(True, "Vous passez votre tour.")
        else:
            Resultat = self.update_resultat(False)
        return Resultat

    def demander_tour(self):
        relative_address = "/home/game/room/turns"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo, 'id_salle': self.id_salle}
        res = requests.get(adresse, data=json.dumps(dataPost))
        if res.status_code == 200:
            Resultat = self.update_resultat(True, "C'est votre tour de jouer")
        elif res.status_code == 403:
            Resultat = self.update_resultat(False, "C'était votre tour de jouer mais vous deviez le passer.")
        elif res.status_code == 449:
            Resultat = self.update_resultat(False, "Ce n'est pas votre tour de jouer")
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.demander_tour")
        return Resultat

    def demander_grille(self):
        relative_address = "/home/game/room/grid"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'id_partie': self.id_salle, 'jeu': self.jeu.lower()}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["Grille"] = res.json()["grid"]
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.demander_grille")
        return Resultat

    def jouer_son_tour(self, action):
        relative_address = "/home/game/room/grid"
        adresse = make_address(absolute_address, relative_address)

        coup = {'pseudo': self.pseudo, 'id_partie': self.id_salle, 'position': action['action'], 'jeu': self.jeu}
        res = requests.post(adresse, data=json.dumps(coup))

        if res.status_code == 200:
            Resultat = self.update_resultat(True, "Le coup a bien été joué.")
        elif res.status_code == 403:
            Resultat = self.update_resultat(False, res.json()["message"])
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.jouer_son_tour")
        return Resultat