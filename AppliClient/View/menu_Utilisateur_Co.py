#Importation des modules
import PyInquirer as inquirer
from View.abstractView import AbstractView

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
        print("Bienvenue sur le menu des utilisateurs connectés")
    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["Menu_Co"] == "Jouer":
                print("Vous avez choisi de jouer")
                import menu_Choix_Jeu as MCJ
                MCJ.menu_Choix_Jeu_Connecte1.make_choice()
            elif self.reponse["Menu_Co"] == "Accéder au profil":
                print("Vous avez décidé d'accéder à voter profil")
                import menu_Profil as MPro
                MPro.menu_Profil1.make_choice()
            elif self.reponse["Menu_Co"] == "Se déconnecter":
                print("Déconnexion réussie")
                break
if __name__ == "__main__": 
    menu_User_Co1 = Menu_User_Co()
