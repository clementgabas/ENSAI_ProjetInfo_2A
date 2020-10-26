# Importation des modules
import PyInquirer as inquirer
from datetime import datetime
from View.abstractView import AbstractView
import View.menu_Creer_Compte as MCC
import View.menu_Connexion as MC
import View.menu_Choix_Jeu as MCJ


# Création du menu_Principal

class Menu_Principal(AbstractView):
    def __init__(self):
        self.questions = [
            {
                'type': 'list',
                'name': 'Accueil',
                'message': "Bienvenue dans le menu principal de l'applicaition. \n Que souhaitez-vous faire ?",
                'choices': [
                    'Me connecter',
                    'Jouer en tant qu\'anonyme',
                    'Créer un compte utilisateur',
                    inquirer.Separator(),
                    'Quitter l\'application',
                ]
            },
        ]

    def display_info(self):
        print(f"{str(datetime.now())} : Bienvenue sur le menu principal")

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["Accueil"] == "Me connecter":
                MC.menu_Connexion1.make_choice()
            elif self.reponse["Accueil"] == "Jouer en tant qu\'anonyme":
                MCJ.menu_Choix_Jeu_Anonyme1.make_choice()
            elif self.reponse["Accueil"] == "Créer un compte utilisateur":
                MCC.menu_Creer_Compte1.make_choice()
            elif self.reponse["Accueil"] == "Quitter l\'application":
                print(f"{str(datetime.now())}  : Cya! Merci et à bientôt!")
                break

if __name__ == "__main__": 
    Menu_P1 = Menu_Principal()
    Menu_P1.make_choice()
