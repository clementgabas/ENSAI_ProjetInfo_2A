import PyInquirer as inquirer

from Vues.abstractView import AbstractView
import Vues.menu_Salle as MS


#Création du menu des classements.

class Menu_Choix_Mode_Jeu_Connecte(AbstractView):
    def __init__(self, pseudo = "user", jeu="p4"):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Choix_Mode_Jeu_Connecte',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Jouer avec des amis',
                              'Jouer contre des inconnus selon les règles officielles',
                              inquirer.Separator(),
                              'Revenir au menu précédent',
                          ]
            },
        ]
        self.pseudo = pseudo
        self.game = jeu.lower()

    def display_info(self):
        #print("Bienvenue sur le menu de choix du jeu")
        pass #on a rien d'intéressant à dire ici

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)

            if self.reponse["menu_Choix_Mode_Jeu_Connecte"] == "Jouer avec des amis":
                print(f"Vous avez choisi de jouer avec des amis au {self.game}.")
                Amis = MS.Menu_Salle(pseudo=self.pseudo, jeu=self.game, ami_anonyme = "ami")
                Amis.display_info()
                return Amis.make_choice()

            elif self.reponse["menu_Choix_Mode_Jeu_Connecte"] == "Jouer contre des inconnus selon les règles officielles":
                print(f"Vous avez décidé de jouer contre des inconnus selon les règles officielles au {self.game}")
                Anonymes = MS.Menu_Salle(pseudo=self.pseudo, jeu=self.game, ami_anonyme = "anonyme")
                Anonymes.display_info()
                return Anonymes.make_choice()


            elif self.reponse["menu_Choix_Mode_Jeu_Connecte"] == "Revenir au menu précédent":
                print("Vous allez être redirigés vers le menu précédent.")
                import Vues.menu_Choix_Jeu as MCJ
                Retour = MCJ.Menu_Choix_Jeu_Connecte(pseudo = self.pseudo)
                Retour.display_info()
                return Retour.make_choice()

            else:
              print("Réponse invalide dans le menu_Choix_Mode_Jeu.menu_Choix_Mode_Jeu_Connecte.make_choice() ... Boucle break")
            break

class Menu_Choix_Mode_Jeu_Anonyme(AbstractView):
    def __init__(self, jeu="p4"):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Choix_Mode_Jeu_Anonyme',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Jouer contre des inconnus selon les règles officielles',
                              inquirer.Separator(),
                              'Revenir au menu précédent',
                          ]
            },
        ]
        if jeu.lower() == "oie":
            self.game = "Jeu de l'Oie"
        elif jeu.lower() == "p4":
            self.game = "Puissance 4"
        else:
            self.game = "erreur sur le jeu"

    def display_info(self):
        #print("Bienvenue sur le menu de choix du jeu")
        pass #on a rien d'intéressant à dire ici

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["menu_Choix_Mode_Jeu_Anonyme"] == "Jouer contre des inconnus selon les règles officielles":
                print("Vous avez décidé de jouer contre des inconnus selon les règles officielles au {self.game}")
                print("*** On a pas encore cette view là. On devrait logiquement quitter l'appli. *** ")
            elif self.reponse["menu_Choix_Mode_Jeu_Anonyme"] == "Revenir au menu précédent":
                print("Vous allez être redirigés vers le menu précédent.")
                import menu_Choix_Jeu as MCJ
                Retour = MCJ.Menu_Choix_Jeu_Anonyme()
                Retour.display_info()
                return Retour.make_choice()
            else:
              print("Réponse invalide dans le menu_Choix_Mode_Jeu.menu_Choix_Mode_Jeu_Anonyme.make_choice() ... Boucle break")
            break



if __name__ == "__main__": 
    menu_Choix_Mode_Jeu_Connecte1 = Menu_Choix_Mode_Jeu_Connecte()
    menu_Choix_Mode_Jeu_Anonyme1 = Menu_Choix_Mode_Jeu_Anonyme()