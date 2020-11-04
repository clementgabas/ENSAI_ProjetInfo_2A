# Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print
import requests
import json
from tabulate import tabulate


# Création du menu ami.

class Menu_Ami(AbstractView):
    def __init__(self, pseudo="user"):
        self.questions = [
            {
                'type': 'list',
                'name': 'menu_Ami',
                'message': "Que souhaitez-vous faire ?",
                'choices': [
                    'Ajouter un ami',
                    'Supprimer un ami',
                    'Afficher ma liste d\'amis',
                    inquirer.Separator(),
                    'Revenir au menu précédent',
                ]
            },
        ]
        self.pseudo = pseudo

    def display_info(self):
        # print("Bienvenue sur le menu ami")
        pass

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)

            if self.reponse["menu_Ami"] == "Ajouter un ami":
                return self.ajout_ami()
            elif self.reponse["menu_Ami"] == "Supprimer un ami":
                return self.supp_ami()
            elif self.reponse["menu_Ami"] == "Afficher ma liste d\'amis":
                return self.voir_liste_ami()
            elif self.reponse["menu_Ami"] == "Revenir au menu précédent":
                import Vues.menu_Profil as MP
                Retour = MP.Menu_Profil(self.pseudo)
                Retour.display_info()
                return Retour.make_choice()
            else:
                print("erreur")
            break

    def ajout_ami(self):
        self.ajoutAmiQ = [
            {
                'type': 'input',
                'name': 'pseudo_ami',
                'message': "Veuillez fournir le pseudo de l'ami à ajouter à la liste des amis :",
            }
        ]
        while True:
            self.ajoutAmiR = inquirer.prompt(self.ajoutAmiQ)
            pseudo_ami = self.ajoutAmiR["pseudo_ami"]
            if pseudo_ami == self.pseudo:
                print("Vous ne pouvez pas vous ajouter vous meme comme ami.")
                return self.echec_ajout_ami()

            dataPost = {'pseudo': self.pseudo, 'pseudo_ami': pseudo_ami}
            # -- connexion à l'API
            res = requests.post('http://localhost:9090/home/main/profil/friends', data=json.dumps(dataPost))
            if res.status_code == 404:
                print(f"Le pseudo a ajouter à votre liste d'ami ({pseudo_ami}) n'existe pas.")
                return self.echec_ajout_ami()
            if res.status_code == 208:
                print(f"Le lien d'amitié avec {pseudo_ami} existe déjà.")
                return self.make_choice()
            if res.status_code == 200:
                print(f"Votre nouvel ami ({pseudo_ami}) a bien été ajouté à votre liste d'amis.")
                return self.make_choice()
            elif res.status_code == 500:
                return print("erreur dans le code de l'api")
            else:
                print("erreur non prévue : " + str(res.status_code))
                return self.make_choice_retour()

    def echec_ajout_ami(self):
        self.echecAjoutAmiQ = [
            {
                'type': 'list',
                'name': 'Retour',
                'message': "Que souhaitez-vous faire ?",
                'choices': [
                    'Réessayer',
                    'Retourner au menu de la liste des amis',
                ]
            },
        ]
        while True:
            self.echecAjoutAmiR = inquirer.prompt(self.echecAjoutAmiQ)
            if self.echecAjoutAmiR["Retour"] == "Réessayer":
                return self.ajout_ami()
            elif self.echecAjoutAmiR["Retour"] == "Retourner au menu de la liste des amis":
                return self.make_choice()
            else:
                print("Erreur dans echec_ajout_ami")
            break

    def supp_ami(self):
        self.suppAmiQ = [
            {
                'type': 'input',
                'name': 'ami_supp',
                'message': "Veuillez fournir le pseudo de l'ami à supprmier de la liste des amis.",
            }
        ]
        while True:
            self.suppAmiR = inquirer.prompt(self.suppAmiQ)
            pseudo_ami = self.suppAmiR["ami_supp"]

            if pseudo_ami == self.pseudo:
                print("Vous ne pouvez pas vous supprimer vous meme comme ami.")
                return self.echec_ajout_ami()

            dataPost = {'pseudo': self.pseudo, 'pseudo_ami': pseudo_ami}
            # -- connexion à l'API
            res = requests.delete('http://localhost:9090/home/main/profil/friends', data=json.dumps(dataPost))
            if res.status_code == 404:
                print(f"Le pseudo a supprimer de votre liste d'ami ({pseudo_ami}) n'existe pas.")
                return self.echec_ajout_ami()
            if res.status_code == 208:
                print(f"Le lien d'amitié avec {pseudo_ami} n'existe pas.")
                return self.make_choice()
            if res.status_code == 200:
                print(f"Votre ancien ami ({pseudo_ami}) a bien été supprimé de votre liste d'amis.")
                return self.make_choice()
            elif res.status_code == 500:
                return print("erreur dans le code de l'api")
            else:
                print("erreur non prévue : " + str(res.status_code))
                return self.make_choice_retour()

    def echec_supp_ami(self):
        self.echecSuppAmiQ = [
            {
                'type': 'list',
                'name': 'Retour',
                'message': "Que souhaitez-vous faire ?",
                'choices': [
                    'Réessayer',
                    'Retourner au menu de la liste des amis',
                ]
            },
        ]
        while True:
            self.echecSuppAmiR = inquirer.prompt(self.echecSuppAmiQ)
            if self.echecSuppAmiR["Retour"] == "Réessayer":
                return self.supp_ami()
            elif self.echecsuppAmiR["Retour"] == "Retourner au menu de la liste des amis":
                return self.make_choice()
            else:
                print("Erreur dans echec_supp_ami")
            break

    def voir_liste_ami(self):

        dataPost = {'pseudo': self.pseudo}
        # -- connexion à l'API
        res = requests.get('http://localhost:9090/home/main/profil/friends', data=json.dumps(dataPost))

        if res.status_code == 200:
            liste_amis = res.json()["liste_amis"]
            print("\n" + tabulate(liste_amis, headers=["Pseudo", "Date d'ajout", "Est connecté?"], tablefmt="grid"))

            return self.make_choice()
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            return self.make_choice()
        elif res.status_code == 500:
            return print("erreur dans le code de l'api")
        else:
            print("erreur non prévue : " + str(res.status_code))
            return self.make_choice_retour()


if __name__ == "__main__":
    menu_Ami1 = Menu_Ami()
    menu_Ami1.display_info()
    menu_Ami1.make_choice()

# Comment