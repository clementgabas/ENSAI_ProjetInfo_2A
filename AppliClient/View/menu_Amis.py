#Importation des modules
import PyInquirer as inquirer
from AppliClient.View.abstractView import AbstractView

#Création du menu ami.

class Menu_Ami(AbstractView):
    def __init__(self):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Ami',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Afficher ma liste d\'amis',
                              'Ajouter un ami',
                              'Supprimer un ami',
                              inquirer.Separator(),
                              'Revenir au menu précédent',
                          ]
            },
        ]
    def display_info(self):
        print("Bienvenue sur le menu ami")
    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["menu_Ami"] == "Afficher ma liste d\'amis":
                print("Vous avez choisi de voir votre liste d\'amis")
            elif self.reponse["menu_Ami"] == "Ajouter un ami":
                print("Vous avez décidé d\'ajouter un ami")
            elif self.reponse["menu_Ami"] == "Supprimer un ami":
                print("Vous avez choisi de supprimer un ami")
            elif self.reponse["menu_Ami"] == "Revenir au menu précédent":
                print("Vous allez être redirigé vers le menu précédent.")
                break

menu_Ami1 = Menu_Ami()

#Comment