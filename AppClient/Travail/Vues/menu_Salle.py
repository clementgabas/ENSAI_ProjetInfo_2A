#Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print
import requests
import json

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
        self.game = jeu.lower()

    def display_info(self):
        pass #on a rien d'intéressant à dire ici

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["menu_Salle"] == "Créer une salle":
                return self.menu_creer_salle()
            elif self.reponse["menu_Salle"] == "Rejoindre une salle":
                return self.menu_rejoindre_salle()
            elif self.reponse["menu_Salle"] == "Revenir au menu précédent":
                print("Vous allez être redirigé vers le menu précédent.")
                import Vues.menu_Choix_Mode_Jeu as MCMJ
                Retour = MCMJ.Menu_Choix_Mode_Jeu_Connecte(pseudo = self.pseudo, jeu=self.game)
                Retour.display_info()
                return Retour.make_choice()
            else:
              print("Réponse invalide dans le menu_Salle.Menu_Salle.make_choice() ... Boucle break")
            break


    def menu_creer_salle(self):
        from Player.PlayerClass import Player
        Player1 = Player(self.pseudo, self.game, None, None)
        Resultat = Player1.creer_salle()
        if Resultat["Statut"] == True:
            import Vues.menu_Salon as MS
            salon = MS.Salon(self.pseudo, Resultat["id_salle"], self.game, True)
            salon.display_info()
            return(salon.make_choice())
        elif Resultat["Statut"] == False:
            return(self.menu_echec_creer_salle())
        else:
            print("Erreur non prévue")
            return(self.menu_echec_creer_salle())

    def menu_echec_creer_salle(self):
        self.questions_retour = [
            {
                'type': 'list',
                'name': 'Retour',
                'message': "Que souhaitez-vous faire ?",
                'choices': [
                    'Réessayer',
                    'Revenir au menu précédent',
                ]
            },
        ]
        while True:
            self.reponse_retour = inquirer.prompt(self.questions_retour)
            if self.reponse_retour['Retour'] == "Réessayer":
                return self.menu_creer_salle()
            elif self.reponse_retour['Retour'] == "Revenir au menu précédent":
                return self.make_choice()
            else:
                print("Erreur dans menu_salle.echec_creer_salle")
            break

    def menu_rejoindre_salle(self):
        self.questions_rejoindre_salle = [
            {
                'type': 'input',
                'name': 'ide_salle',
                'message': "Quelle salle souhaitez vous rejoindre ?"
            },
        ]
        self.reponse_rejoindre_salle = inquirer.prompt(self.questions_rejoindre_salle)
        id_salle = self.reponse_rejoindre_salle["ide_salle"]

        from Player.PlayerClass import Player
        Player1 = Player(self.pseudo, self.game, None, None)
        Resultat = Player1.rejoindre_salle(id_salle)
        if Resultat["Statut"] == True:
            import Vues.menu_Salon as MS
            salon = MS.Salon(self.pseudo, Resultat["id_salle"], self.game, False)
            salon.display_info()
            return (salon.make_choice())
        elif Resultat["Statut"] == False:
            return (self.menu_echec_rejoindre_salle())
        else:
            print("Erreur non prévue")
            return (self.menu_echec_rejoindre_salle())

    def menu_echec_rejoindre_salle(self):
        self.questions_retour = [
            {
                'type': 'list',
                'name': 'Retour',
                'message': "Que souhaitez-vous faire ?",
                'choices': [
                    'Réessayer',
                    'Revenir au menu précédent',
                ]
            },
        ]
        while True:
            self.reponse_retour = inquirer.prompt(self.questions_retour)
            if self.reponse_retour['Retour'] == "Réessayer":
                return self.menu_rejoindre_salle()
            elif self.reponse_retour['Retour'] == "Revenir au menu précédent":
                return self.make_choice()
            else:
                print("Erreur dans menu_salle.echec_rejoindre_salle")
            break

if __name__ == "__main__": 
    menu_Salle1 = Menu_Salle()
    menu_Salle1.display_info()
    menu_Salle1.make_choice()