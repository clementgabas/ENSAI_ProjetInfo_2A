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
                return self.creer_salle()
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


    def creer_salle(self):
        dataPost = {'pseudo_chef_salle': self.pseudo, 'game': self.game}
        res = requests.post('http://localhost:9090/home/game/room', data=json.dumps(dataPost))

        if res.status_code == 200:
            id_salle = res.json()['id_salle']
            print(f"Une salle (numéro {id_salle}) vient d'être créée. Vos amis peuvent la rejoindre via son numéro.")
        else:
            return self.echec_creer_salle()

    def echec_creer_salle(self):
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
                return self.creer_salle()
            elif self.reponse_retour['Retour'] == "Revenir au menu précédent":
                return self.make_choice()
            else:
                print("Erreur dans menu_salle.echec_creer_salle")
            break



if __name__ == "__main__": 
    menu_Salle1 = Menu_Salle()
    menu_Salle1.display_info()
    menu_Salle1.make_choice()