import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print
from travailMDP.testmdp import *
import requests
import json

class UserBase():
    def creer_compte(self,identifiant,mdp,mdp2,pseudo):
            if mdp != mdp2:
                print("Les mot de passes ne correspondent pas.")
                Resultat = {"Statut": False}
                return (Resultat)
            if identifiant == "" or mdp == "":
                print("L'identifiant ou le mot de passe n'a pas été précisé.")
                Resultat = {"Statut": False}
                return (Resultat)
            if not anti_SQl_injection(identifiant) or not anti_SQl_injection(mdp) or not anti_SQl_injection(pseudo):
                Resultat = {"Statut": False}
                return (Resultat)
            # if not is_mdp_legal(mdp):
            # return self.make_choice_retour()
            hmdp = hacherMotDePasse(mdp)

            # création du data pour le corps du post de l'api
            dataPost = {'username': identifiant, "hpassword": hmdp, "pseudo": pseudo}
            # -- connexion à l'API
            res = requests.post('http://localhost:9090/home/users', data=json.dumps(dataPost))

            if res.status_code == 409:
                if "User" in res.json()['message']:
                    print("L'identifiant est déjà utilisé par un autre membre.")
                elif "Pseudo" in res.json()['message']:
                    print("Le pseudo est déjà utilisé par un autre membre")
                else:
                    print("error")
                Resultat = {"Statut": False}
                return (Resultat)
            elif res.status_code == 404:
                print("erreur, l'api n'a pas été trouvée")
                Resultat = {"Statut": False}
                return (Resultat)
            elif res.status_code == 500:
                print("erreur dans le code de l'api")
                Resultat = {"Statut": False}
                return (Resultat)
            elif res.status_code == 200:
                print("Compte créé avec succès. Veuillez vous authentifiez svp")
                Resultat = {"Statut": True}
                return (Resultat)
            else:
                print("erreur non prévue : " + str(res.status_code))
                Resultat = {"Statut": False}
                return (Resultat)

    def connexion(self,identifiant,mdp,):
        if identifiant == "" or mdp == "":
            print("L'identifiant ou le mot de passe n'a pas été précisé.")
            Resultat = {"Statut": False}
            return (Resultat)
        if not anti_SQl_injection(identifiant) or not anti_SQl_injection(mdp):
            Resultat = {"Statut": False}
            return (Resultat)
        dataPost = {'username': identifiant, "password": mdp}

        # -- connexion à l'API
        res = requests.get('http://localhost:9090/home/connexion', data=json.dumps(dataPost))
        if res.status_code == 200:
            pseudo = res.json()["pseudo"]
            print("Connection réussie")
            Resultat = {"Statut" : True, "pseudo" : pseudo}
            return(Resultat)
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            Resultat = {"Statut": False}
            return(Resultat)
        elif res.status_code == 500:
            print("erreur dans le code de l'api")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 401:
            print("Identifiant ou mot de passe incorrect.")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 403:
            print("L'utilisateur est déjà conecté.")
            Resultat = {"Statut": False}
            return (Resultat)
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut": False}
            return (Resultat)
