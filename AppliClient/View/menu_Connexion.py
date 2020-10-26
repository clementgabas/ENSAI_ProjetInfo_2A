#Importation des modules
import PyInquirer as inquirer
from View.abstractView import AbstractView
import View.menu_Utilisateur_Co as MUC


#Création du menu de connexion

class Menu_Connexion(AbstractView):
    def display_info(self):
        print("Bienvenue sur le menu de connexion")
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

            identifiant, mdp = menu_Connexion1.reponse["Identifiant"], menu_Connexion1.reponse["Password"]

            #fonction de connexion

            #if connexion :
                #Co = MUC.Menu_User_Co()
                #return Co.make_choice()
            #else:
                #print("Id ou mdp incorrect. Veuillez reessayer")
                #return self.make_choice


if __name__ == "__main__": 
    menu_Connexion1 = Menu_Connexion()


# Les réponses des utilisateurs sont stockés dans : menu_Connexion1.reponse["Identifiant"] et (menu_Connexion1.reponse["Password"]) il faudra ensuite les comparer aux id et mdp stockés en base avant
#de permttre l'authentification.
