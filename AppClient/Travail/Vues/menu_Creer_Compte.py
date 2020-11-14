#Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print
from travailMDP.testmdp import *

import requests
import json
#Création du menu Créer compte

class Menu_Creer_Compte(AbstractView):
    def display_info(self):
        print("Bienvenue sur le menu de création de compte")
    def make_choice(self):
        self.questions = [
            {
                'type': 'input',
                'name': 'identifiant',
                'message': "Veuillez insérer votre identifiant",
            },
            {
                'type': 'password',
                'name': 'Password',
                'message': "Veuillez insérer votre mot de passe",
            },
            {
                'type': 'password',
                'name': 'password_Check',
                'message': "Veuillez confirmer votre mot de passe",
            },

            {
                'type': 'input',
                'name': 'pseudo',
                'message': "Veuillez insérer votre pseudo",
            }
        ]
        while True:
            self.reponse = inquirer.prompt(self.questions)
            from Player.UserBaseClass import UserBase
            UserBase1 = UserBase()
            Resultat = UserBase1.creer_compte(self.reponse["identifiant"].lower(), self.reponse["Password"], self.reponse["password_Check"], self.reponse["pseudo"].lower())
            if Resultat["Statut"] == False:
                return(self.make_choice_retour())
            elif Resultat["Statut"] == True:
                import Vues.menu_Connexion as MC
                Co = MC.Menu_Connexion()
                Co.display_info()
                return Co.make_choice()

    def make_choice_retour(self):
        self.questions_retour = [
            {
                'type': 'list',
                'name': 'Retour',
                'message': "Que souhaitez-vous faire ?",
                    'choices': [
                        'Réessayer',
                        'Retourner à l\'accueil',
                    ]
            },
        ]
        while True:
            self.reponse_retour = inquirer.prompt(self.questions_retour)
            if self.reponse_retour['Retour'] == "Réessayer":
                return self.make_choice()
            elif self.reponse_retour['Retour'] == "Retourner à l'accueil":
                import Vues.menu_Accueil as MA
                Retour = MA.Menu_Accueil()
                Retour.display_info()
                return Retour.make_choice()
            else:
                print("Erreur dans menu_Creer_Comtpe.Menu_CreerCompte.make_choice_retour")
            break

if __name__ == "__main__":

    menu_Creer_Compte1  = Menu_Creer_Compte()
    menu_Creer_Compte1.display_info()
    menu_Creer_Compte1.make_choice()



# Les réponses des utilisateurs sont stockés dans : menu_Creer_Compte1.reponse["Identifiant"] et (menu_Creer_Compte1.reponse["Password"]) il faudra ensuite les comparer aux id et mdp stockés en base avant
#de permttre l'authentification.



# Les réponses des utilisateurs sont stockés dans : menu_Creer_Compte1.reponse["Identifiant"] et (menu_Creer_Compte1.reponse["Password"]) il faudra ensuite les comparer aux id et mdp stockés en base avant
#de permttre l'authentification.
