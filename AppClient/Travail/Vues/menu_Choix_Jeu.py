#Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView
import Vues.menu_Choix_Mode_Jeu as MCMJ

from printFunctions import timePrint as print


#Création du menu Créer compte

class Menu_Choix_Jeu_Connecte(AbstractView):
    def __init__(self, pseudo="user"):
        self.questions = [
             {
                'type': 'list',
                'name': 'choix_Jeu_Connecte',
                'message': "A quel jeu souhaitez-vous jouer ?",
                'choices': [
                    'Le jeu de l\'oie',
                    'Le puissance 4',
                    inquirer.Separator(),
                    'Revenir au menu précédent',
                    ]
                },
            ]
        self.pseudo = pseudo
    def display_info(self):
        pass #on a rien d'intéressant à print ici.

    def make_choice(self):
        self.reponse = inquirer.prompt(self.questions)

        if self.reponse["choix_Jeu_Connecte"] == "Le jeu de l\'oie":
            jeu = "Oie"

        elif self.reponse["choix_Jeu_Connecte"] == "Le puissance 4":
            jeu = "P4"

        elif self.reponse["choix_Jeu_Connecte"] == "Revenir au menu précédent":
            print("Vous allez être redirigé vers le menu précédent.")
            import Vues.menu_Utilisateur_Co as MUC
            Retour = MUC.Menu_User_Co()
            Retour.display_info()
            return Retour.make_choice()

        else:
            return print("Erreur dans le choix du jeu dans menu_Choix_Jeu.menu_Choix_Jeu_Connecte.make_choice()")

        Jouer = MCMJ.Menu_Choix_Mode_Jeu_Connecte(jeu)
        Jouer.display_info()
        return Jouer.make_choice()


class Menu_Choix_Jeu_Anonyme(AbstractView):
    def __init__(self):
        self.questions = [
             {
                'type': 'list',
                'name': 'choix_Jeu_Anonyme',
                'message': "A quel jeu souhaitez-vous jouer ?",
                'choices': [
                    'Le jeu de l\'oie',
                    'Le puissance 4',
                    inquirer.Separator(),
                    'Revenir au menu précédent'
                    ]
                },
            ]
    def display_info(self):
        pass #on a rien d'intéressant à print ici.

    def make_choice(self):
        self.reponse = inquirer.prompt(self.questions)

        if self.reponse["choix_Jeu_Anonyme"] == "Le jeu de l\'oie":
            jeu = "Oie"
        elif self.reponse["choix_Jeu_Anonyme"] == "Le puissance 4":
            jeu = "P4"
        elif self.reponse["choix_Jeu_Anonyme"] == "Revenir au menu précédent":
            print("Vous allez être redirigés vers le menu précédent.")
            print("*** A faire ***")
            #Retour =
            pass 
        else:
            return print("Erreur dans le choix du jeu dans menu_Choix_Jeu.menu_Choix_Jeu_Anonyme.make_choice()")

        Jouer = MCMJ.Menu_Choix_Mode_Jeu_Anonyme(jeu)
        Jouer.display_info()
        return Jouer.make_choice()




if __name__ == "__main__":
    while True: 
        choix = input("Voulez-vous tester : \n 1. Menu_Choix_Jeu_Connecte \n 2. Menu_Choix_Jeu_Anonyme")
        if str(choix) == 1:
            menu_Choix_Jeu_Connecte1 = Menu_Choix_Jeu_Connecte()
            menu_Choix_Jeu_Connecte1.display_info()
            menu_Choix_Jeu_Connecte1.make_choice()
        elif str(choix) ==2:
            menu_Choix_Jeu_Anonyme1 = Menu_Choix_Jeu_Anonyme()
            menu_Choix_Jeu_Anonyme1.display_info()
            menu_Choix_Jeu_Anonyme1.make_choice()
        else:
            print("CHOIX INVALIDE. RECOMMENCEZ SVP!")
        break

