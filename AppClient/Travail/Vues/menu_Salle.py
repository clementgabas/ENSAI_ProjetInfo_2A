#Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print


#Création du menu des classements.

class Menu_Salle(AbstractView):
    def __init__(self, pseudo = "user", jeu = "p4"):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Salle',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Créer une salle',
                              'Rejoindre une salle',
                              inquirer.Separator(),
                              'Revenir au menu précédent',
                          ]
            },
        ]
        self.pseudo = pseudo
        if jeu.lower() == "oie":
            self.game = "Jeu de l'Oie"
        elif jeu.lower() == "p4":
            self.game = "Puissance 4"
        else:
            self.game = "erreur sur le jeu"

    def display_info(self):
        pass #on a rien d'intéressant à dire ici

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["menu_Salle"] == "Créer une salle":
                print("Vous avez choisi de créer une salle")
                print("*** On a pas encore la suite. On devrait donc quitter l'appli ***")
            elif self.reponse["menu_Salle"] == "Rejoindre une salle":
                print("Vous avez décidé de rejoindre une salle")
                print("*** On a pas encore la suite. On devrait donc quitter l'appli ***")
            elif self.reponse["menu_Salle"] == "Revenir au menu précédent":
                print("Vous allez être redirigé vers le menu précédent.")
                import Vues.menu_Choix_Mode_Jeu as MCMJ
                Retour = MCMJ.Menu_Choix_Mode_Jeu_Connecte(pseudo = self.pseudo, jeu=self.game)
                Retour.display_info()
                return Retour.make_choice()
            else:
              print("Réponse invalide dans le menu_Salle.Menu_Salle.make_choice() ... Boucle break")
            break



if __name__ == "__main__": 
    menu_Salle1 = Menu_Salle()
    menu_Salle1.display_info()
    menu_Salle1.make_choice()