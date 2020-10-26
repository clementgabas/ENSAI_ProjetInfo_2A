#Importation des modules
import PyInquirer as inquirer
from abstractView import AbstractView

#Création du menu profil

class Menu_Profil(AbstractView):
    def __init__(self):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Profil',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Modifier mes informations personnelles',
                              'Accéder à ma liste d\'amis',
                              'Accéder au classement',
                              inquirer.Separator(),
                              'Revenir au menu précédent',
                          ]
            },
        ]
    def display_info(self):
        print("Bienvenue sur le menu profil")
    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["menu_Profil"] == "Modifier mes informations personnelles":
                print("Vous avez choisi de modifier vos informations personnelles")
                import menu_Mod_Inf as MMI
                MMI.menu_Modif1.make_choice()
            elif self.reponse["menu_Profil"] == "Accéder à ma liste d\'amis":
                print("Vous avez décidé d'accéder à votre liste d\'amis")
                import menu_Amis as MA
                MA.menu_Ami1.make_choice()
            elif self.reponse["menu_Profil"] == "Accéder au classement":
                print("Vous avez décidé d'accéder à votre classement")
                import menu_Classement as MC
                MC.menu_Classement1.make_choice()
            elif self.reponse["menu_Profil"] == "Revenir au menu précédent":
                print("Vous allez être redirigé vers le menu précédent.")
                break

menu_Profil1 = Menu_Profil()
