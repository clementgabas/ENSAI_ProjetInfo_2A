#Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print

#Création du menu Créer compte

class Menu_Creer_Compte(AbstractView):
    def display_info(self):
        print("Bienvenue sur le menu de création de compte")
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
        self.questionsPseudo = [
            {
                'type': 'input',
                'name': 'pseudo',
                'message': "Veuillez insérer votre pseudo",
            },]
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["Password"] != self.reponse["password_Check"]:
                print("Les mot de passes ne correspondent pas.")
                return self.make_choice_retour()
                
            #on simule l'API.
            #elle prend en entrée l'id et le mdp et elle vérifie si c'est bon.
            is_id_free = True
            id_mdp_legal = True
            has_API_worked = True

            #ensuite elle demande un pseudo et vérifie si il est libre
            self.reponsePseudo = inquirer.prompt(self.questionsPseudo)
            pseudo = self.reponsePseudo['pseudo']

            is_pseudo_legit = True
            is_pseudo_free = True

            print("Compte créer avec succès. Veuillez vous authentifiez svp")
            import Vues.menu_Connexion as MC
            Co = MC.Menu_Connexion()
            Co.display_info()
            return Co.make_choice()

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
                print("Erreur dans menu_Creer_Comtpe.Menu_CreerCompte.make_choice_retour")
            break

if __name__ == "__main__": 
    menu_Creer_Compte1  = Menu_Creer_Compte()
    menu_Creer_Compte1.display_info()
    menu_Creer_Compte1.make_choice()

# Les réponses des utilisateurs sont stockés dans : menu_Creer_Compte1.reponse["Identifiant"] et (menu_Creer_Compte1.reponse["Password"]) il faudra ensuite les comparer aux id et mdp stockés en base avant
#de permttre l'authentification.
