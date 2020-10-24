#Importation des modules
import PyInquirer as inquirer
from View.abstractView import AbstractView

#Création du menu Créer compte

class Menu_Choix_Jeu(AbstractView):
    def display_info(self):
        print("Bienvue sur le menu de choix de jeu")
    def __init__(self):
        self.questions = [
             {
                'type': 'list',
                'name': 'choix_Jeu',
                'message': "A quel jeu souhaitez-vous jouer ?",
                'choices': [
                    'Le jeu de l\'oie',
                    inquirer.Separator(),
                    'Le puissance 4',
                    ]
                },
            ]
    def make_choice(self):
        self.reponse = inquirer.prompt(self.questions)
        if self.reponse["choix_Jeu"] == "Le jeu de l\'oie":
            print("En attente d'autres joueurs.")
        if self.reponse["choix_Jeu"] == "Le puissance 4":
            print("En attente d'autres joueurs.")

menu_Choix_Jeu1  = Menu_Choix_Jeu()
