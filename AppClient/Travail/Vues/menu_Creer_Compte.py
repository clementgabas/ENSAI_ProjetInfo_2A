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
                'type' : 'password',
                'name' : 'Password',
                'message' : "Veuillez insérer votre mot de passe",
            },
            {
                'type': 'password',
                'name': 'password_Check',
                'message': "Veuillez confirmer votre mot de passe",
            }
        ]
        self.questionsPseudo = [
            {
                'type': 'input',
                'name': 'pseudo',
                'message': "Veuillez insérer votre pseudo",
            },]
        while True:


            self.reponse = inquirer.prompt(self.questions)

            identifiant, mdp, mdp2 = self.reponse["identifiant"].lower(), self.reponse["Password"], self.reponse["password_Check"]

            if mdp != mdp2:
                print("Les mot de passes ne correspondent pas.")
                return self.make_choice_retour()
            if identifiant is "" or mdp is "":
                print("L'identifiant ou le mot de passe n'a pas été précisé.")
                return self.make_choice_retour()
            if not anti_SQl_injection(identifiant) or not anti_SQl_injection(mdp):
                return self.make_choice_retour()

            #if not is_mdp_legal(mdp):
                #return self.make_choice_retour()
            hmdp = hacherMotDePasse(mdp)

            #ensuite elle demande un pseudo
            self.reponsePseudo = inquirer.prompt(self.questionsPseudo)
            pseudo = self.reponsePseudo['pseudo'].lower()
            if not anti_SQl_injection(pseudo):
                return self.make_choice_retour()
            #création du data pour le corps du post de l'api
            dataPost = {'username' : identifiant, "hpassword" : hmdp, "pseudo" : pseudo}

            #-- connexion à l'API
            res = requests.post('http://localhost:9090/home/users', data=json.dumps(dataPost))

            if res.status_code == 409:
                if "User" in res.json()['message']:
                    print("L'identifiant est déjà utilisé par un autre membre.")
                elif "Pseudo" in res.json()['message']:
                    print("Le pseudo est déjà utilisé par un autre membre")
                else:
                    print("error")
                return self.make_choice_retour()
            elif res.status_code == 404:
                print("erreur, l'api n'a pas été trouvée")
                return self.make_choice_retour()
            elif res.status_code == 500:
                return print("erreur dans le code de l'api")
            elif res.status_code == 200:
                print("Compte créé avec succès. Veuillez vous authentifiez svp")
                import Vues.menu_Connexion as MC
                Co = MC.Menu_Connexion()
                Co.display_info()
                return Co.make_choice()
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
                print("Erreur dans menu_Creer_Comtpe.Menu_CreerCompte.make_choice_retour")
            break

if __name__ == "__main__":

    menu_Creer_Compte1  = Menu_Creer_Compte()
    menu_Creer_Compte1.display_info()
    menu_Creer_Compte1.make_choice()



# Les réponses des utilisateurs sont stockés dans : menu_Creer_Compte1.reponse["Identifiant"] et (menu_Creer_Compte1.reponse["Password"]) il faudra ensuite les comparer aux id et mdp stockés en base avant
#de permttre l'authentification.
