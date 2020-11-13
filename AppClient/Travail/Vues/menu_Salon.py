import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print
import requests
import json
from tabulate import tabulate
import time

class Salon(AbstractView):
    def __init__(self, pseudo, id_salle, jeu, est_chef):
        self.pseudo = pseudo.lower()
        self.game = jeu.lower()
        self.id_salle = id_salle
        self.est_chef = est_chef

        self.question = [
            {
                'type' : 'list',
                'name' : 'Salon_accueil',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Voir les membres de la salle',
                              'Modifier les paramètres de la salle',
                              "Être prêt",
                              inquirer.Separator(),
                              'Quitter la salle',
                          ]
            },
        ]

    def display_info(self):
        print(f"Vous êtes dans le salon de la salle {self.id_salle}.")

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.question)
            if self.reponse["Salon_accueil"] == 'Voir les membres de la salle':
                return self.voir_membres_salle()
            elif self.reponse["Salon_accueil"] == 'Modifier les paramètres de la salle':
                import Vues.menu_Parametres as MPara
                MParametre1 = MPara.Menu_Parametre(self.pseudo, self.id_salle, self.game,  self.est_chef)
                return MParametre1.make_choice()
            elif self.reponse["Salon_accueil"] == "Être prêt":
                self.choix_couleur(self.get_liste_couleurs_dispo())
                if self.est_chef == True:
                    self.etre_pret_chef()
                else:
                    self.etre_pret()
                return self.demander_tour()
            else: #'Quitter la salle'
                return self.retour()
            break

    def retour(self):
        self.question_retour = [
            {
                'type' : 'list',
                'name' : 'salon_retour',
                'message' : f"Vous allez retourner au menu précédant. Vous allez donc quitter la salle {self.id_salle}. Etes vous sur? ",
                          'choices' : [
                              "Oui",
                              "Non"
                          ]
            },
        ]
        while True:
            self.reponse_retour = inquirer.prompt(self.question_retour)
            if self.reponse_retour["salon_retour"] == "Oui":
                dataPost = {"pseudo":self.pseudo, "id_salle": self.id_salle, "est_chef_salle": self.est_chef}
                res = requests.delete("http://localhost:9090/home/game/room", data=json.dumps(dataPost))
                if res.status_code == 401:
                    print("Vous êtes le chef de la salle! Vous ne pouvez pas la quitter tant qu'un autre utilisateur s'y trouve encore. Un capitaine quitte toujours son navire en dernier n'est-ce pas?")
                    return self.make_choice()
                elif res.status_code == 200:
                    import Vues.menu_Choix_Mode_Jeu as MCMJ
                    Retour = MCMJ.Menu_Choix_Mode_Jeu_Connecte(pseudo=self.pseudo, jeu=self.game)
                    Retour.display_info()
                    return Retour.make_choice()

            else: #'non'
                return self.make_choice()

    def voir_membres_salle(self):
        dataPost = {'id_salle': self.id_salle}
        res = requests.get("http://localhost:9090/home/game/room", data=json.dumps(dataPost))

        if res.status_code == 200:
            liste_membres = res.json()["liste_membres"]
            print("\n" + tabulate(liste_membres, headers=["Pseudo"], tablefmt="grid"))
            return self.make_choice()


    def get_liste_couleurs_dispo(self):
        dataPost = {'id_salle':self.id_salle}
        res = requests.get("http://localhost:9090/home/game/room/colors", data=json.dumps(dataPost))

        if res.status_code == 200:
            liste_couleurs_dispos = res.json()["liste_couleurs_dispos"]
            return liste_couleurs_dispos
        elif res.status_code == 403:
            print("Vous ne pouvez pas être pret car vous êtes seuls dans la salle. Il faut être au moins 2.")
            return self.make_choice()

    def choix_couleur(self, liste_couleurs_dispos):
        answer = inquirer.prompt([
            {
                'type': 'list',
                'name': 'couleur',
                'message': 'Quelle couleur voulez vous choisir pour jouer?',
                'choices': liste_couleurs_dispos,
            },
        ])
        couleur_choisie = answer['couleur']

        dataPost = {'id_salle':self.id_salle, 'pseudo':self.pseudo, 'couleur':couleur_choisie}
        res = requests.post("http://localhost:9090/home/game/room/colors", data=json.dumps(dataPost))

        if res.status_code == 409: #la couleur a été choisie entre temps
            print("La couleur demandée a été choisie entre temps par un autre utilisateur. Veuillez réessayer svp.")
            return self.choix_couleur(self.get_liste_couleurs_dispo())


    def etre_pret(self):
        dataPost = {'pseudo':self.pseudo,'id_salle':self.id_salle, 'est_chef':self.est_chef}
        res = requests.post("http://localhost:9090/home/game/room/turns", data=json.dumps(dataPost))
        if res.status_code == 200:
            print("Vous êtes prets!")

    def is_everyone_ready(self):
        tout_le_monde_pret = False
        dataPost = {'pseudo': self.pseudo, 'id_salle': self.id_salle, 'est_chef': self.est_chef}
        while not tout_le_monde_pret:
            # -- on requete pour savoir si tout le monde est pret dans la salle
            res = requests.get("http://localhost:9090/home/game/room/launch", data=json.dumps(dataPost))
            # -- si on récupère un "tout le monde est pret", on lance la partie
            if res.status_code == 200:
                tout_le_monde_pret = True
            else:
                print('en attente que tous les participants soient prets pour lancer la partie.')
                time.sleep(2)
        return tout_le_monde_pret

    def etre_pret_chef(self):
        self.etre_pret()
        everyone_ready = False
        while not everyone_ready:
            if self.is_everyone_ready():
                everyone_ready = True
                print("Tous les participants sont pret. La partie va pouvoir démarer.")

        dataPost = {'id_salle': self.id_salle}
        res = requests.post("http://localhost:9090/home/game/room/launch", data=json.dumps(dataPost))  # dao pour modifier dans la table Partie le statut à en cours
        if res.status_code == 200:
            #la partie est lancée, on peut requeter pour savoir si c'est son tour
            print("jusque la tout va bien, plus qu'a demander son tour sans arret")


    def demander_tour(self):
        mon_tour = False
        dataPost = {'pseudo': self.pseudo, 'id_salle': self.id_salle}
        while not mon_tour:
            res = requests.get("http://localhost:9090/home/game/room/turns", data=json.dumps(dataPost))
            if res.json()["message"] == "ton tour":
                mon_tour = True
            time.sleep(2)
        return mon_tour