import requests
import json
from tabulate import tabulate
from travailMDP.testmdp import *

class User():

    def __init__(self, pseudo):
        self.pseudo = pseudo

    def deconnexion(self):
        dataPost = {'pseudo': self.pseudo}
        # -- connexion à l'API
        res = requests.get('http://localhost:9090/home/deconnexion', data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = {"Statut" : True}
            return(Resultat)
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            Resultat = {"Statut" : False}
            return(Resultat)
        elif res.status_code == 500:
            print("erreur dans le code de l'api")
            Resultat = {"Statut": False}
            return (Resultat)
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut" : False}
            return(Resultat)


    def ajout_ami(self,pseudo_ami):
        if pseudo_ami == self.pseudo:
            print("Vous ne pouvez pas vous ajouter vous meme comme ami.")
            Resultat = {"Statut": False}
            return (Resultat)
        dataPost = {'pseudo': self.pseudo, 'pseudo_ami': pseudo_ami}
        # -- connexion à l'API
        res = requests.post('http://localhost:9090/home/main/profil/friends', data=json.dumps(dataPost))
        if res.status_code == 404:
            print(f"Le pseudo a ajouter à votre liste d'ami ({pseudo_ami}) n'existe pas.")
            Resultat = {"Statut": False}
            return (Resultat)
        if res.status_code == 208:
            print(f"Le lien d'amitié avec {pseudo_ami} existe déjà.")
            Resultat = {"Statut": False}
            return (Resultat)
        if res.status_code == 200:
            print(f"Votre nouvel ami ({pseudo_ami}) a bien été ajouté à votre liste d'amis.")
            Resultat = {"Statut": True}
            return (Resultat)
        elif res.status_code == 500:
            print("erreur dans le code de l'api")
            Resultat = {"Statut": False}
            return (Resultat)
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut": False}
            return (Resultat)

    def supp_ami(self,pseudo_ami):
        if pseudo_ami == self.pseudo:
            print("Vous ne pouvez pas vous supprimer vous meme comme ami.")
            Resultat = {"Statut": False}
            return (Resultat)

        dataPost = {'pseudo': self.pseudo, 'pseudo_ami': pseudo_ami}
        # -- connexion à l'API
        res = requests.delete('http://localhost:9090/home/main/profil/friends', data=json.dumps(dataPost))
        if res.status_code == 404:
            print(f"Le pseudo a supprimer de votre liste d'ami ({pseudo_ami}) n'existe pas.")
            Resultat = {"Statut": False}
            return (Resultat)
        if res.status_code == 208:
            print(f"Le lien d'amitié avec {pseudo_ami} n'existe pas.")
            Resultat = {"Statut": False}
            return (Resultat)
        if res.status_code == 200:
            print(f"Votre ancien ami ({pseudo_ami}) a bien été supprimé de votre liste d'amis.")
            Resultat = {"Statut": True}
            return (Resultat)
        elif res.status_code == 500:
            print("erreur dans le code de l'api")
            Resultat = {"Statut": False}
            return (Resultat)
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut": False}
            return (Resultat)

    def afficher_amis(self):

        dataPost = {'pseudo': self.pseudo}
        # -- connexion à l'API
        res = requests.get('http://localhost:9090/home/main/profil/friends', data=json.dumps(dataPost))

        if res.status_code == 200:
            liste_amis = res.json()["liste_amis"]
            print("\n" + tabulate(liste_amis, headers=["Pseudo", "Date d'ajout", "Est connecté?", "En partie?"],
                                  tablefmt="grid"))
            Resultat = {"Statut": True}
            return (Resultat)
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 500:
            print("erreur dans le code de l'api")
            Resultat = {"Statut": False}
            return (Resultat)
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut": False}
            return (Resultat)

    def modifier_mdp(self,old_mdp,new_mdp1,new_mdp2):
        if new_mdp1 != new_mdp2:
            print("Les deux nouveaux mots de passes ne correspondent pas.")
            Resultat = {"Statut": False}
            return (Resultat)
        if new_mdp1 == "":
            print("Veuillez fournir un nouveau mot de passe svp.")
            Resultat = {"Statut": False}
            return (Resultat)
        if not anti_SQl_injection(new_mdp1):
            Resultat = {"Statut": False}
            return (Resultat)

        # if not is_mdp_legal(new_mdp1):
        # return self.echec_modif_mdp()

        dataPost = {'pseudo': self.pseudo, 'old_password': old_mdp, 'new_password': new_mdp1}
        res = requests.put('http://localhost:9090/home/main/profil/user/password', data=json.dumps(dataPost))

        if res.status_code == 401:
            print("Le mot de passe fournit ne correspond pas.")
            Resultat = {"Statut": False}
            return (Resultat)
        if res.status_code == 200:
            print("Le mot de passe a bien été modifié.")
            Resultat = {"Statut": True}
            return (Resultat)
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 500:
            print("erreur dans le code de l'api")
            Resultat = {"Statut": False}
            return (Resultat)
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut": False}
            return (Resultat)

    def modifier_pseudo(self,new_pseudo):

        if new_pseudo == self.pseudo:
            print("Le nouveau pseudo est identique à l'ancien.")
            Resultat = {"Statut": False}
            return (Resultat)

        dataPost = {'old_pseudo': self.pseudo, 'new_pseudo': new_pseudo}
        res = requests.put('http://localhost:9090/home/main/profil/user/pseudo', data=json.dumps(dataPost))

        if res.status_code == 409:
            print("Le pseudo demandé est déjà utilisé.")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 200:
            print("Le pseudo a été mis à jour.")
            self.pseudo = new_pseudo
            Resultat = {"Statut": True}
            return (Resultat)
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 500:
            return print("erreur dans le code de l'api")
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut": False}
            return (Resultat)

    def acceder_stats_perso(self):

        dataPost = {'pseudo': self.pseudo}
        # -- connexion à l'API
        res = requests.get('http://localhost:9090/home/main/profil/user/stat', data=json.dumps(dataPost))
        if res.status_code == 200:
            stat_perso = res.json()['Statistiques personnelles']
            parties_g = stat_perso[0][1]
            parties_j = stat_perso[0][0]
            pourc_partie_g = 0
            if parties_j != 0:
                pourc_partie_g = parties_g / parties_j * 100
            stat_perso[0].append("{} %".format(pourc_partie_g))
            print("\n" + tabulate(stat_perso, headers=["Nombre de parties jouées", "Nombre de parties gagnées",
                                                       "Pourcentage de parties gagnées"], tablefmt="grid"))
            Resultat = {"Statut": True}
            return (Resultat)
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 500:
            print("erreur dans le code de l'api")
            Resultat = {"Statut": False}
            return (Resultat)
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut": False}
            return (Resultat)

    def reinitialiser_stats_perso(self):
        dataPost = {'pseudo': self.pseudo}
        res = requests.put('http://localhost:9090/home/main/profil/user/stat', data=json.dumps(dataPost))
        if res.status_code == 200:
            print(" Vos statistiques ont bien été réinitialisées")
            Resultat = {"Statut": True}
            return (Resultat)
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 500:
            print("erreur dans le code de l'api")
            Resultat = {"Statut": False}
            return (Resultat)
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut": False}
            return (Resultat)

    def aff_classement_general(self):
        # -- connexion à l'API
        dataPost = {"pseudo": self.pseudo}
        res = requests.get('http://localhost:9090/home/main/profil/classment/general', data=json.dumps(dataPost))

        if res.status_code == 200:
            classement_general = res.json()["classement_general"]
            classement_general_amis = res.json()["classement_general_amis"]
            print("Classement mondial \n" + tabulate(classement_general,
                                                     headers=["Classement", "Pseudo", "nombre de point",
                                                              "Nombre de parties jouées",
                                                              "Nombre de parties gagnées"],
                                                     tablefmt="grid"))
            print("Classement entre amis \n" + tabulate(classement_general_amis,
                                                        headers=["Classement", "Pseudo", "nombre de point",
                                                                 "Nombre de parties jouées",
                                                                 "Nombre de parties gagnées"],
                                                        tablefmt="grid"))
            Resultat = {"Statut": True}
            return (Resultat)
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 500:
            print("erreur dans le code de l'api")
            Resultat = {"Statut": False}
            return (Resultat)
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut": False}
            return (Resultat)

    def aff_classement_jeu_oie(self):
        # -- connexion à l'API
        dataPost = {"nom_jeu": "Oie",
                    "pseudo": self.pseudo
                    }
        res = requests.get('http://localhost:9090/home/main/profil/classment/jeu', data=json.dumps(dataPost))

        if res.status_code == 200:
            classement_jeu = res.json()["classement_jeu"]
            classement_jeu_amis = res.json()["classement_jeu_amis"]
            print(
                "Classement mondial :\n" + tabulate(classement_jeu,
                                                    headers=["Classement", "Pseudo", "nombre de point",
                                                             "Nombre de parties jouées",
                                                             "Nombre de parties gagnées"],
                                                    tablefmt="grid"))
            print("Classement entre amis :\n" + tabulate(classement_jeu_amis,
                                                         headers=["Classement", "Pseudo", "nombre de point",
                                                                  "Nombre de parties jouées",
                                                                  "Nombre de parties gagnées"],
                                                         tablefmt="grid"))

            Resultat = {"Statut" : True}
            return(Resultat)
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 500:
            print("erreur dans le code de l'api")
            Resultat = {"Statut": False}
            return (Resultat)
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut": False}
            return (Resultat)

    def aff_classement_P4(self):
        # -- connexion à l'API
        dataPost = {"nom_jeu": "P4",
                    "pseudo": self.pseudo
                    }

        res = requests.get('http://localhost:9090/home/main/profil/classment/jeu', data=json.dumps(dataPost))

        if res.status_code == 200:
            classement_jeu = res.json()["classement_jeu"]
            classement_jeu_amis = res.json()["classement_jeu_amis"]
            print(
                "Classement mondial :\n" + tabulate(classement_jeu,
                                                    headers=["Classement", "Pseudo", "nombre de point",
                                                             "Nombre de parties jouées",
                                                             "Nombre de parties gagnées"],
                                                    tablefmt="grid"))
            print("Classement entre amis :\n" + tabulate(classement_jeu_amis,
                                                         headers=["Classement", "Pseudo", "nombre de point",
                                                                  "Nombre de parties jouées",
                                                                  "Nombre de parties gagnées"],
                                                         tablefmt="grid"))

            Resultat = {"Statut": True}
            return (Resultat)
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            Resultat = {"Statut": False}
            return (Resultat)
        elif res.status_code == 500:
            print("erreur dans le code de l'api")
            Resultat = {"Statut": False}
            return (Resultat)
        else:
            print("erreur non prévue : " + str(res.status_code))
            Resultat = {"Statut": False}
            return (Resultat)
