#Importation des modules
import PyInquirer as inquirer
from abstractView import AbstractView

#Création du menu Créer compte

class Menu_Choix_Jeu_Connecte(AbstractView):
    def display_info(self):
        print("Bienvue sur le menu de choix de jeu")
    def __init__(self):
        self.questions = [
             {
                'type': 'list',
                'name': 'choix_Jeu_Connecte',
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
        if self.reponse["choix_Jeu_Connecte"] == "Le jeu de l\'oie":
            import menu_Choix_Mode_Jeu as MCMJ
            MCMJ.menu_Choix_Mode_Jeu_Connecte1.make_choice()
        if self.reponse["choix_Jeu_Connecte"] == "Le puissance 4":
            import menu_Choix_Mode_Jeu as MCMJ
            MCMJ.menu_Choix_Mode_Jeu_Connecte1.make_choice()

menu_Choix_Jeu_Connecte1  = Menu_Choix_Jeu_Connecte()

class Menu_Choix_Jeu_Anonyme(AbstractView):
    def display_info(self):
        print("Bienvue sur le menu de choix de jeu")
    def __init__(self):
        self.questions = [
             {
                'type': 'list',
                'name': 'choix_Jeu_Anonyme',
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
        if self.reponse["choix_Jeu_Anonyme"] == "Le jeu de l\'oie":
            import menu_Choix_Mode_Jeu as MCMJ
            MCMJ.menu_Choix_Mode_Jeu_Anonyme1.make_choice()
        if self.reponse["choix_Jeu_Anonyme"] == "Le puissance 4":
            import menu_Choix_Mode_Jeu as MCMJ
            MCMJ.menu_Choix_Mode_Jeu_Anonyme1.make_choice()

menu_Choix_Jeu_Anonyme1  = Menu_Choix_Jeu_Anonyme()