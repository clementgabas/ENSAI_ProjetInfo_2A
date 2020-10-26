#Importation des modules
import PyInquirer as inquirer
from View.abstractView import AbstractView
#Création du menu Créer compte

class Menu_Creer_Compte(AbstractView):
    def display_info(self):
        print("Bienvue sur le menu de création de compte")
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
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["Password"] != self.reponse["password_Check"]:
                print("Les mot de passes ne correspondent pas. Veuillez réessayer")
            else:
                print("Compte créer avec succès, vous allez être redirigé vers le menu principal")
                break


menu_Creer_Compte1  = Menu_Creer_Compte()

# Les réponses des utilisateurs sont stockés dans : menu_Creer_Compte1.reponse["Identifiant"] et (menu_Creer_Compte1.reponse["Password"]) il faudra ensuite les comparer aux id et mdp stockés en base avant
#de permttre l'authentification.
