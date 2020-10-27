#Importation des modules
import PyInquirer as inquirer
from abstractView import AbstractView
import menu_Choix_Jeu as MCJ
import menu_Profil as MPro

from datetime import datetime



#Création du menu pour les utilisateurs connectés

class Menu_User_Co(AbstractView):
    def __init__(self):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'Menu_Co',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Jouer',
                              'Accéder au profil',
                              inquirer.Separator(),
                              'Se déconnecter',
                          ]
            },
        ]
    def display_info(self):
        print(f"[{str(datetime.now())}]: 'Pseudo', vous êtes connectés. Bienvenue!")

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)

            if self.reponse["Menu_Co"] == "Jouer":
                Play = MCJ.Menu_Choix_Jeu_Connecte()
                Play.display_info()
                return Play.make_choice()

            elif self.reponse["Menu_Co"] == "Accéder au profil":
                Profil = MPro.Menu_Profil()
                Profil.display_info()
                return Profil.make_choice()

            elif self.reponse["Menu_Co"] == "Se déconnecter":
                print(f"[{str(datetime.now())}]: Déconnexion réussie")

            else:
                print(f"[{str(datetime.now())}]: réponse invalide dans le menu_Utilisateur.Menu_User_Co.make_choice() ... Boucle break")
            break

if __name__ == "__main__": 
    menu_User_Co1 = Menu_User_Co()
    menu_User_Co1.display_info()
    menu_User_Co1.make_choice()
