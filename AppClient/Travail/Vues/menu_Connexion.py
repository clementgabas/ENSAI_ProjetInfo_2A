#Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView
import Vues.menu_Utilisateur_Co as MUC

from printFunctions import timePrint as print
from travailMDP.testmdp import *

import requests
import json

#Création du menu de connexion

class Menu_Connexion(AbstractView):
    def display_info(self):
        print("Vous êtes sur le menu de connexion")

    def make_choice(self):
        self.questions = [
            {
                'type': 'input',
                'name': 'Identifiant',
                'message': "Veuillez insérer votre identifiant",
            },
            {
                'type' : 'password',
                'name' : 'Password',
                'message' : "Veuillez insérer votre mot de passe",
            }
        ]
        while True:
            self.reponse = inquirer.prompt(self.questions)
            identifiant, mdp = self.reponse["Identifiant"].lower(), self.reponse["Password"]

            if identifiant == "" or mdp == "":
                print("L'identifiant ou le mot de passe n'a pas été précisé.")
                return self.make_choice_retour()
            if not anti_SQl_injection(identifiant) or not anti_SQl_injection(mdp):
                return self.make_choice_retour()

            dataPost = {'username': identifiant, "password": mdp}

            # -- connexion à l'API
            res = requests.get('http://localhost:9090/home/connexion', data=json.dumps(dataPost))

            if res.status_code == 200 :
                pseudo = res.json()["pseudo"]
                print("Connection réussie")
                Co = MUC.Menu_User_Co(pseudo)
                Co.display_info()
                return Co.make_choice()
            elif res.status_code == 404:
                print("erreur, l'api n'a pas été trouvée")
                return self.make_choice_retour()
            elif res.status_code == 500:
                return print("erreur dans le code de l'api")
            elif res.status_code == 401:
                print("Identifiant ou mot de passe incorrect.")
                return self.make_choice_retour()
            elif res.status_code == 403:
                print("L'utilisateur est déjà conecté.")
                return self.make_choice_retour()
            else:
                print("erreur non prévue : "+ str(res.status_code))
                return self.make_choice_retour()

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
                print("Erreur dans menu_Connexion.Menu_Connexion.make_choice_retour")
            break

if __name__ == "__main__": 
    menu_Connexion1 = Menu_Connexion()
    menu_Connexion1.display_info()
    menu_Connexion1.make_choice()


# Les réponses des utilisateurs sont stockés dans : menu_Connexion1.reponse["Identifiant"] et (menu_Connexion1.reponse["Password"]) il faudra ensuite les comparer aux id et mdp stockés en base avant
#de permttre l'authentification.
