import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print
import requests
import json
from tabulate import tabulate

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
                              "Lancer la partie",
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
            elif self.reponse["Salon_accueil"] == "Lancer la partie":
                pass
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