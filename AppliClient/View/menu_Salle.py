#Importation des modules
import PyInquirer as inquirer
from View.abstractView import AbstractView

#Création du menu des classements.

class menu_Salle(AbstractView):
    def __init__(self):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Salle',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Créer une salle',
                              'Rejoindre une salle',
                              inquirer.Separator(),
                              'Revenir au menu précédent',
                          ]
            },
        ]
    def display_info(self):
        print("Bienvenue sur le menu de choix du jeu")
    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["menu_Salle"] == "Créer une salle":
                print("Vous avez choisi de créer une salle")
            elif self.reponse["menu_Salle"] == "Rejoindre une salle":
                print("Vous avez décidé de rejoindre une salle")
            elif self.reponse["menu_Salle"] == "Revenir au menu précédent":
                print("Vous allez être redirigé vers le menu précédent.")
                break

menu_Salle1 = menu_Salle()