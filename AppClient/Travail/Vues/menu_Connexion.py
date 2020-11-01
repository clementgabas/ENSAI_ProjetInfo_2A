#Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView
import Vues.menu_Utilisateur_Co as MUC

from printFunctions import timePrint as print


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
            identifiant, mdp = self.reponse["Identifiant"], self.reponse["Password"]
            
            #A cette étape, on requete l'API pour savoir si oui ou non on peut se connecter grâce aux id et mdp donnés.

            #en fonction de ce que renvoit l'API :
            # si l'API répond connexion = True, on se connecte
            # sinon, on réessaye

            #Dans notre cas, on simule que la connexion renvoit True
            print("**** On simmule que la connection se passe bien car on a pas encore coder l'authentification ****")
            connexion = True

            if connexion :
                Co = MUC.Menu_User_Co()
                Co.display_info()
                return Co.make_choice()
            else:
                print("Id ou mdp incorrect.")
                return self.make_choice_retour()




            #on envoit au serveur id et mdp et on lui demande si on peut se connecter.

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
