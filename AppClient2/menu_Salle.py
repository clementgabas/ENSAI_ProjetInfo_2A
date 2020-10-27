#Importation des modules
import PyInquirer as inquirer
from abstractView import AbstractView

from datetime import datetime


#Création du menu des classements.

class Menu_Salle(AbstractView):
    def __init__(self, jeu):
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
                print(f"[{str(datetime.now())}]: Vous avez choisi de créer une salle")
                print("*** On a pas encore la suite. On devrait donc quitter l'appli ***")
            elif self.reponse["menu_Salle"] == "Rejoindre une salle":
                print(f"[{str(datetime.now())}]: Vous avez décidé de rejoindre une salle")
                print("*** On a pas encore la suite. On devrait donc quitter l'appli ***")
            elif self.reponse["menu_Salle"] == "Revenir au menu précédent":
                print(f"[{str(datetime.now())}]: Vous allez être redirigé vers le menu précédent.")
                import menu_Choix_Mode_Jeu as MCMJ
                Retour = MCMJ.Menu_Choix_Mode_Jeu_Connecte(self.game)
                Retour.display_info()
                return Retour.make_choice()
            else:
              print(f"[{str(datetime.now())}]: réponse invalide dans le menu_Salle.Menu_Salle.make_choice() ... Boucle break")
            break



if __name__ == "__main__": 
    menu_Salle1 = Menu_Salle()