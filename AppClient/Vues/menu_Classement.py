#Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print
import requests
import json
from tabulate import tabulate

#Création du menu des classements.

class Menu_Classement(AbstractView):
    def __init__(self, pseudo = "user"):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Classement',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Afficher le classement général',
                              'Afficher le classement du jeu de l\'oie',
                              'Afficher le classement du puissance 4',
                              inquirer.Separator(),
                              'Revenir au menu précédent',
                          ]
            },
        ]
        self.pseudo = pseudo
    def display_info(self):
        #print("Bienvenue sur le menu des classements")
        pass

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)

            if self.reponse["menu_Classement"] == "Afficher le classement général":
                return self.aff_class_gen()
            elif self.reponse["menu_Classement"] == "Afficher le classement du jeu de l\'oie":
                return self.aff_class_oie()
            elif self.reponse["menu_Classement"] == "Afficher le classement du puissance 4":
                return self.aff_class_p4()
            elif self.reponse["menu_Classement"] == "Revenir au menu précédent":
                import Vues.menu_Profil as MP
                Retour = MP.Menu_Profil(self.pseudo)
                Retour.display_info()
                return Retour.make_choice()            
            else:
                print("erreur")
            break

    def make_choice_retour(self):
        self.questions_retour = [
            {
                'type': 'list',
                'name': 'Retour',
                'message': "Que souhaitez-vous faire ?",
                    'choices': [
                        'Réessayer',
                        'Revenir au menu precedent',
                    ]
            },
        ]
        while True:
            self.reponse_retour = inquirer.prompt(self.questions_retour)
            if self.reponse_retour['Retour'] == "Réessayer":
                return self.make_choice()
            elif self.reponse_retour['Retour'] == "Revenir au menu precedent":
                import Vues.menu_Profil as MP
                Retour = MP.Menu_Accueil()
                Retour.display_info()
                return Retour.make_choice()
            else:
                print("Erreur dans menu_Classement.Menu_Classement.make_choice_retour")
            break

    def aff_class_gen(self):
        from Player.UserClass import User
        User1 = User(self.pseudo)
        Resultat = User1.aff_classement_general()
        self.print_message(Resultat)
        if Resultat["Statut"] == True:
            self.print_classement(Resultat["classement_general"])
            self.print_classement(Resultat["classement_general_amis"])
            return(self.make_choice())
        elif Resultat["Statut"] == False:
            return(self.make_choice_retour())
        else:
            print("Erreur non prévue")
            return(self.make_choice_retour())


    def aff_class_oie(self):
        from Player.UserClass import User
        User1 = User(self.pseudo)
        Resultat = User1.aff_classement_jeu_oie()
        self.print_message(Resultat)
        if Resultat["Statut"] == True:
            self.print_classement(Resultat["classement_jeu"])
            self.print_classement(Resultat["classement_jeu_amis"])
            return (self.make_choice())
        elif Resultat["Statut"] == False:
            return (self.make_choice_retour())
        else:
            print("Erreur non prévue")
            return (self.make_choice_retour())



    def aff_class_p4(self):
        from Player.UserClass import User
        User1 = User(self.pseudo)
        Resultat = User1.aff_classement_P4()
        self.print_message(Resultat)
        if Resultat["Statut"] == True:
            self.print_classement(Resultat["classement_jeu"])
            self.print_classement(Resultat["classement_jeu_amis"])
            return (self.make_choice())
        elif Resultat["Statut"] == False:
            return (self.make_choice_retour())
        else:
            print("Erreur non prévue")
            return (self.make_choice_retour())

    def print_classement(self, classement):
        return print("Classement mondial \n" + tabulate(classement,
                                                 headers=["Classement", "Pseudo", "nombre de point",
                                                          "Nombre de parties jouées",
                                                          "Nombre de parties gagnées"],
                                                 tablefmt="grid"))

if __name__ == "__main__":
    menu_Classement1 = Menu_Classement()
    menu_Classement1.display_info()
    menu_Classement1.make_choice()

