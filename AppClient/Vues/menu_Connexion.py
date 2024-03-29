import PyInquirer as inquirer

from Vues.abstractView import AbstractView

from Vues.usefulfonctions.printFunctions import timePrint as print


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
            from Player.UserBaseClass import UserBase
            UserBase1 = UserBase()
            Resultat = UserBase1.connexion(self.reponse["Identifiant"].lower(), self.reponse["Password"])
            self.print_message(Resultat)

            if Resultat["Statut"] == False:
                return (self.make_choice_retour())
            elif Resultat["Statut"] == True:
                import Vues.menu_Utilisateur_Co as MUC
                Co = MUC.Menu_User_Co(Resultat["pseudo"])
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
                print("Erreur dans menu_Connexion.Menu_Connexion.make_choice_retour")
            break

if __name__ == "__main__":
    menu_Connexion1 = Menu_Connexion()
    menu_Connexion1.display_info()
    menu_Connexion1.make_choice()


# Les réponses des utilisateurs sont stockés dans : menu_Connexion1.reponse["Identifiant"] et (menu_Connexion1.reponse["Password"]) il faudra ensuite les comparer aux id et mdp stockés en base avant
#de permttre l'authentification.

