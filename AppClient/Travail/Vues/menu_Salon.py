import PyInquirer as inquirer
from Vues.abstractView import AbstractView
import Vues.menu_Jouer as Play

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
                return self.menu_voir_membres_salle()
            elif self.reponse["Salon_accueil"] == 'Modifier les paramètres de la salle':
                import Vues.menu_Parametres as MPara
                MParametre1 = MPara.Menu_Parametre(self.pseudo, self.id_salle, self.game,  self.est_chef)
                return MParametre1.make_choice()
            elif self.reponse["Salon_accueil"] == "Être prêt":
                pass
            else: #'Quitter la salle'
                return self.menu_retour()
            break

    def menu_retour(self):
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
                from Player.PlayerClass import Player
                Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
                Resultat = Player1.quitter_salle()
                if Resultat["Statut"] == True:
                    import Vues.menu_Choix_Mode_Jeu as MCMJ
                    Retour = MCMJ.Menu_Choix_Mode_Jeu_Connecte(pseudo=self.pseudo, jeu=self.game)
                    Retour.display_info()
                    return Retour.make_choice()
                elif Resultat["Statut"] == False:
                    return (self.make_choice())
                else:
                    print("Erreur non prévue")
                    return (self.make_choice())

            else: #'non'
                return self.make_choice()


    def menu_voir_membres_salle(self):
        from Player.PlayerClass import Player
        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.voir_membres_salle()
        if Resultat["Statut"] == True:
            return(self.make_choice())
        elif Resultat["Statut"] == False:
            return (self.make_choice())
        else:
            print("Erreur non prévue")
            return (self.make_choice())


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
                time.sleep(0.5)
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




    def jouer(self):
        monTour = False
        while not monTour:
            monTour = self.demander_tour()
            time.sleep(0.5)
        Action = Play.Jouer(self.pseudo, self.id_salle, self.game,  self.est_chef)
        Action.jouer()
        return self.passer_tour()



    def demander_tour(self):
        dataPost = {'pseudo': self.pseudo, 'id_salle': self.id_salle}
        res = requests.get("http://localhost:9090/home/game/room/turns", data=json.dumps(dataPost))
        if res.status_code == 200:
            mon_tour = True
            print("C'est votre tour de jouer.")
        elif res.status_code == 449:
            mon_tour = False
            print("ce n'est pas votre tour de jouer")
        else:
            print("erreur dans demander_tour")
        return mon_tour

    def passer_tour(self):
        dataPost = {'pseudo': self.pseudo, 'id_salle': self.id_salle}
        requests.put("http://localhost:9090/home/game/room/turns", data=json.dumps(dataPost))
        return self.jouer()
