#Importation des modules
import PyInquirer as inquirer
from abstractView import AbstractView

#Création du menu de connexion

class menu_Connexion(AbstractView):
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
            if menu_Connexion1.reponse["Identifiant"] == "1" and menu_Connexion1.reponse["Password"] == "2":
                print("Connexion réussie")
                import menu_Utilisateur_Co as MUC
                MUC.menu_User_Co1.make_choice()
                break
            else:
                print("Identifiant ou mot de passe incorrect. Veuillez réessayer")
menu_Connexion1 = menu_Connexion()


# Les réponses des utilisateurs sont stockés dans : menu_Connexion1.reponse["Identifiant"] et (menu_Connexion1.reponse["Password"]) il faudra ensuite les comparer aux id et mdp stockés en base avant
#de permttre l'authentification.
