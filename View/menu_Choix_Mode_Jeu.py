#Importation des modules
import PyInquirer as inquirer
from View.abstractView import AbstractView

#Création du menu des classements.

class menu_Choix_Mode_Jeu_Connecte(AbstractView):
    def __init__(self):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Choix_Mode_Jeu_Connecte',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Jouer avec des amis',
                              'Jouer contre des inconnus selon les règles officielles',
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
            if self.reponse["menu_Choix_Mode_Jeu_Connecte"] == "Jouer avec des amis":
                import menu_Salle as MS
                MS.menu_Salle1.make_choice()
            elif self.reponse["menu_Choix_Mode_Jeu_Connecte"] == "Jouer contre des inconnus selon les règles officielles":
                print("Vous avez décidé de jouer contre des inconnus selon les règles officielles")
            elif self.reponse["menu_Choix_Mode_Jeu_Connecte"] == "Revenir au menu précédent":
                print("Vous allez être redirigé vers le menu précédent.")
                break

menu_Choix_Mode_Jeu_Connecte1 = menu_Choix_Mode_Jeu_Connecte()

class menu_Choix_Mode_Jeu_Anonyme(AbstractView):
    def __init__(self):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Choix_Mode_Jeu_Anonyme',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Jouer contre des inconnus selon les règles officielles',
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
            if self.reponse["menu_Choix_Mode_Jeu_Anonyme"] == "Jouer contre des inconnus selon les règles officielles":
                print("Vous avez décidé de jouer contre des inconnus selon les règles officielles")
            elif self.reponse["menu_Choix_Mode_Jeu_Anonyme"] == "Revenir au menu précédent":
                print("Vous allez être redirigé vers le menu précédent.")
                break

menu_Choix_Mode_Jeu_Anonyme1 = menu_Choix_Mode_Jeu_Anonyme()