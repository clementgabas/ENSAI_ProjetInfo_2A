#Importation des modules
import PyInquirer as inquirer
from abstractView import AbstractView

#Création du menu de mofidification des informations.

class Menu_Modif_Inf(AbstractView):
    def __init__(self):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Modif_Info',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Modifier mon identifiant',
                              'Modifier mon pseudo',
                              'Modifier mon mot de passe',
                              inquirer.Separator(),
                              'Revenir au menu précédent',
                          ]
            },
        ]
    def display_info(self):
        print("Bienvenue sur le menu de modification des informations")
    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["menu_Modif_Info"] == "Modifier mon identifiant":
                print("Vous avez choisi de modifier votre identifiant")
            elif self.reponse["menu_Modif_Info"] == "Modifier mon pseudo":
                print("Vous avez décidé de modifier votre pseudo")
            elif self.reponse["menu_Modif_Info"] == "Modifier mon mot de passe":
                print("Vous avez choisi de modifier votre mot de passe")
            elif self.reponse["menu_Modif_Info"] == "Revenir au menu précédent":
                print("Vous allez être redirigé vers le menu précédent.")
                break

menu_Modif1 = Menu_Modif_Inf()