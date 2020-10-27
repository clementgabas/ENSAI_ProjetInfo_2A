# Importation des modules
from datetime import datetime

import PyInquirer as inquirer
from abstractView import AbstractView
import menu_Creer_Compte as MCC
import menu_Connexion as MC
import menu_Choix_Jeu as MCJ


# Création du menu_Principal

class Menu_Acceuil(AbstractView):
    def __init__(self):
        self.questions = [
            {
                'type': 'list',
                'name': 'Accueil',
                'message': "Que souhaitez-vous faire ?",
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
        print(f"[{str(datetime.now())}]: Bienvenue dans l'accueil de l'application.")

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)

            if self.reponse["Accueil"] == "Me connecter":
                Co = MC.Menu_Connexion()
                Co.display_info()
                return Co.make_choice()

            elif self.reponse["Accueil"] == "Jouer en tant qu\'anonyme":
                #jsp si il faut mettre la classe choix_mode_jeu_conencte ou choix_mode_jeu_anonyme..
                #Jeu = MCJ.Menu_Choix_Mode_Jeu_Connecte()
                #return Jeu.make_choice()
                pass

            elif self.reponse["Accueil"] == "Créer un compte utilisateur":
                CrCompte = MCC.Menu_Creer_Compte()
                CrCompte.display_info()
                return CrCompte.make_choice()

            elif self.reponse["Accueil"] == "Quitter l\'application":
                return print(f"[{str(datetime.now())}]: Cya! Merci et à bientôt!")

            else:
                print(f"[{str(datetime.now())}]: réponse invalide dans le menu_Acceuil.Menu_Acceuil.make_choice() ... Boucle break")
            break

if __name__ == "__main__": 
    Menu_P1 = Menu_Acceuil()
    Menu_P1.display_info()
    Menu_P1.make_choice()
