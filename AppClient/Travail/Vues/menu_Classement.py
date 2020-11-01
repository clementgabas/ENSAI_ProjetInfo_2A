#Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print

#Création du menu des classements.

class Menu_Classement(AbstractView):
    def __init__(self):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Classement',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Afficher le classement général',
                              'Afficher le classement du jeu de l\'oie',
                              'Afficher le classement du puissance 4',
                              'Accéder à ses statistiques personnelles',
                              inquirer.Separator(),
                              'Revenir au menu précédent',
                          ]
            },
        ]
        
    def display_info(self):
        #print("Bienvenue sur le menu ami")
        pass

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["menu_Classement"] == "Afficher le classement général":
                print("Vous avez choisi d\'afficher le classement général")
            elif self.reponse["menu_Classement"] == "Afficher le classement du jeu de l\'oie":
                print("Vous avez décidé d\'afficher le classement du jeu de l\'oie")
            elif self.reponse["menu_Classement"] == "Afficher le classement du puissance 4":
                print("Vous avez choisi d\'afficher le classement du puissance 4")
            elif self.reponse["menu_Classement"] == "Accéder à ses statistiques personnelles":
                print("Vous avez choisi d\'accéder à vos statistiques personnelles")
            elif self.reponse["menu_Classement"] == "Revenir au menu précédent":
                print("Vous allez être redirigé vers le menu précédent.")
                break



if __name__ == "__main__": 
    menu_Classement1 = Menu_Classement()
    menu_Classement1.display_info()
    menu_Classement1.make_choice()
