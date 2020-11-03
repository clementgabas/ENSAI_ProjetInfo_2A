#Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView
import Vues.menu_Choix_Jeu as MCJ
import Vues.menu_Profil as MPro

from printFunctions import timePrint as print
import requests
import json

#Création du menu pour les utilisateurs connectés

class Menu_User_Co(AbstractView):
    def __init__(self, pseudo="user"):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'Menu_Co',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Jouer',
                              'Accéder au profil',
                              inquirer.Separator(),
                              'Se déconnecter',
                          ]
            },
        ]
        self.pseudo = pseudo
    def display_info(self):
        print(f"{self.pseudo}, vous êtes connectés. Bienvenue!")

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)

            if self.reponse["Menu_Co"] == "Jouer":
                Play = MCJ.Menu_Choix_Jeu_Connecte(self.pseudo)
                Play.display_info()
                return Play.make_choice()

            elif self.reponse["Menu_Co"] == "Accéder au profil":
                Profil = MPro.Menu_Profil(self.pseudo)
                Profil.display_info()
                return Profil.make_choice()

            elif self.reponse["Menu_Co"] == "Se déconnecter":

                dataPost = {'pseudo': self.pseudo}
                # -- connexion à l'API
                res = requests.get('http://localhost:9090/home/deconnexion', data=json.dumps(dataPost))

                if res.status_code == 200:
                    import Vues.menu_Accueil as MA
                    Deco = MA.Menu_Accueil()
                    print("Déconnexion réussie")
                    Deco.display_info()
                    return Deco.make_choice()
                elif res.status_code == 404:
                    print("erreur, l'api n'a pas été trouvée")
                    return self.make_choice()
                elif res.status_code == 500:
                    return print("erreur dans le code de l'api")
                else:
                    print("erreur non prévue : " + str(res.status_code))
                    return self.make_choice()
            else:
                print("Réponse invalide dans le menu_Utilisateur.Menu_User_Co.make_choice() ... Boucle break")
            break

if __name__ == "__main__": 
    menu_User_Co1 = Menu_User_Co()
    menu_User_Co1.display_info()
    menu_User_Co1.make_choice()