import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print
import requests
import json

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
                              'Revenir au menu précédent',
                          ]
            },
        ]

        def display_info(self):
            print(f"Vous êtes dans le salon de la salle {self.id_salle}.")

        def make_choice(self):
            while True:
                self.reponse = inquirer.prompt(self.questions)

                if self.reponse["Salon_accueil"] == 'Voir les membres de la salle':
                    pass
                elif self.reponse["Salon_accueil"] == 'Modifier les paramètres de la salle':
                    pass
                elif self.reponse["Salon_accueil"] == "Lancer la partie":
                    pass
                else: #'Revenir au menu précédent'
                    print("Vous allez être redirigés vers le menu précédent.")
                    import Vues.menu_Choix_Mode_Jeu as MCMJ
                    Retour = MCMJ.Menu_Choix_Mode_Jeu_Connecte(pseudo=self.pseudo, jeu=self.game)
                    Retour.display_info()
                    return Retour.make_choice()
                break

        def voir_membres_salle(self):
            dataPost = {'id_salle': self.id_salle}
            #res = requests.get(f"http://localhost:9090/home/game/room/{self.id_salle}", data=json.dumps(dataPost))






