import PyInquirer as inquirer

from Vues.abstractView import AbstractView
from Player.PlayerClass import Player

from Vues.usefulfonctions.printFunctions import timePrint as print


#Création du menu des classements.

class Menu_Salle(AbstractView):
    def __init__(self, pseudo = "user", jeu = "p4", ami_anonyme="ami"):
      self.pseudo = pseudo
      self.game = jeu.lower()
      self.ami_anonyme = ami_anonyme.lower()
      if ami_anonyme == "ami":
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
      elif ami_anonyme == "anonyme":
          self.questions = [
              {
                  'type' : 'list',
                  'name' : 'menu_Salle',
                  'message' : "Que souhaitez-vous faire ?",
                            'choices' : [
                                'Jouer contre des inconnus',
                                inquirer.Separator(),
                                'Revenir au menu précédent',
                            ]
              },
          ]

    def display_info(self):
        pass #on a rien d'intéressant à dire ici

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["menu_Salle"] == "Créer une salle":
                return self.menu_creer_salle()
            elif self.reponse["menu_Salle"] == "Rejoindre une salle":
                return self.menu_rejoindre_salle()
            elif self.reponse["menu_Salle"] == "Jouer contre des inconnus":
                return self.menu_rejoindre_salle_anonyme()         
            elif self.reponse["menu_Salle"] == "Revenir au menu précédent":
                print("Vous allez être redirigés vers le menu précédent.")
                import Vues.menu_Choix_Mode_Jeu as MCMJ
                Retour = MCMJ.Menu_Choix_Mode_Jeu_Connecte(pseudo = self.pseudo, jeu=self.game)
                Retour.display_info()
                return Retour.make_choice()
            else:
              print("Réponse invalide dans le menu_Salle.Menu_Salle.make_choice() ... Boucle break")
            break


    def menu_creer_salle(self):
        Player1 = Player(self.pseudo, self.game, id_salle=None, chef_salle=None, ami_anonyme=self.ami_anonyme)
        Resultat = Player1.creer_salle()
        self.print_message(Resultat)

        if Resultat["Statut"]:
            import Vues.menu_Salon as MS
            salon = MS.Salon(self.pseudo, Resultat["id_salle"], self.game, True)
            salon.display_info()
            return(salon.make_choice())
        elif not Resultat["Statut"]:
            return(self.menu_echec_creer_salle())
        else:
            print("Erreur non prévue dans Menu_Salle.menu_creer_salle")
            return(self.menu_echec_creer_salle())

    def menu_echec_creer_salle(self):
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
                return self.menu_creer_salle()
            elif self.reponse_retour['Retour'] == "Revenir au menu précédent":
                return self.make_choice()
            else:
                print("Erreur dans menu_salle.echec_creer_salle")
            break

    def menu_rejoindre_salle(self, id_salle=None):
        if self.ami_anonyme == "ami":
            self.questions_rejoindre_salle = [
                {
                    'type': 'input',
                    'name': 'ide_salle',
                    'message': "Quelle salle souhaitez vous rejoindre ?"
                },
            ]
            self.reponse_rejoindre_salle = inquirer.prompt(self.questions_rejoindre_salle)
            id_salle = self.reponse_rejoindre_salle["ide_salle"]

        Player1 = Player(self.pseudo, self.game, None, None)
        Resultat = Player1.rejoindre_salle(id_salle)
        self.print_message(Resultat)

        if Resultat["Statut"]:
            import Vues.menu_Salon as MS
            salon = MS.Salon(self.pseudo, Resultat["id_salle"], self.game, False)
            salon.display_info()
            return (salon.make_choice())
        elif not Resultat["Statut"]:
            return (self.menu_echec_rejoindre_salle())
        else:
            print("Erreur non prévue dans Menu_Salle.menu_rejoindre_salle")
            return (self.menu_echec_rejoindre_salle())

    def menu_rejoindre_salle_anonyme(self):
        Player1 = Player(self.pseudo, self.game, id_salle=None, chef_salle=None, ami_anonyme="anonyme")
        Resultat = Player1.is_salle_anonyme_available()
        self.print_message(Resultat)
        if Resultat["Statut"]: #une salle est dispo
            self.menu_rejoindre_salle(Resultat["id_salle"])
        else:
            self.menu_creer_salle()



        # Resultat = Player1.rejoindre_salle_anonyme()
        # self.print_message(Resultat)
        # if Resultat["id_salle"] != -1:  #on a trouvé une salle anonyme
        #     import Vues.menu_Salon as MS
        #     salon = MS.Salon(self.pseudo, Resultat["id_salle"], self.game, False)
        #     salon.display_info()
        #     return (salon.make_choice())
        # else: #pas de salle anonyme dispo
        #     self.menu_creer_salle()

    def menu_echec_rejoindre_salle(self):
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
                return self.menu_rejoindre_salle()
            elif self.reponse_retour['Retour'] == "Revenir au menu précédent":
                return self.make_choice()
            else:
                print("Erreur dans menu_salle.echec_rejoindre_salle")
            break

if __name__ == "__main__": 
    menu_Salle1 = Menu_Salle()
    menu_Salle1.display_info()
    menu_Salle1.make_choice()