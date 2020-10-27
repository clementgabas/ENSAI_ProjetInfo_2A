#Importation des modules
import PyInquirer as inquirer
from abstractView import AbstractView
import menu_Utilisateur_Co as MUC

from datetime import datetime


#Création du menu de connexion

class Menu_Connexion(AbstractView):
    def display_info(self):
        print(f"[{str(datetime.now())}]: Vous êtes sur le menu de connexion")

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
            identifiant, mdp = self.reponse["Identifiant"], self.reponse["Password"]
            
            #A cette étape, on requete l'API pour savoir si oui ou non on peut se connecter grâce aux id et mdp donnés.

            #en fonction de ce que renvoit l'API :
            # si l'API répond connexion = True, on se connecte
            # sinon, on réessaye

            #Dans notre cas, on simule que la connexion renvoit True
            print(f"[{str(datetime.now())}]: **** On simmule que la connection se passe bien car on a pas encore coder l'authentification ****")
            connexion = True

            if connexion :
                Co = MUC.Menu_User_Co()
                Co.display_info()
                return Co.make_choice()
            else:
                print(f"[{str(datetime.now())}]: Id ou mdp incorrect. Veuillez reessayer")
                return self.make_choice




            #on envoit au serveur id et mdp et on lui demande si on peut se connecter.



if __name__ == "__main__": 
    menu_Connexion1 = Menu_Connexion()
    menu_Connexion1.display_info()
    menu_Connexion1.make_choice()


# Les réponses des utilisateurs sont stockés dans : menu_Connexion1.reponse["Identifiant"] et (menu_Connexion1.reponse["Password"]) il faudra ensuite les comparer aux id et mdp stockés en base avant
#de permttre l'authentification.
