#Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print

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
                              'Accéder à ses statistiques personnelles',
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
            elif self.reponse["menu_Classement"] == "Accéder à ses statistiques personnelles":
                return self.aff_stat_perso()
            elif self.reponse["menu_Classement"] == "Revenir au menu précédent":
                import Vues.menu_Profil as MP
                Retour = MP.Menu_Profil(self.pseudo)
                Retour.display_info()
                return Retour.make_choice()            
            else:
                print("erreur")
            break


    def aff_class_gen(self):
        print("*** ON SIMULE QUE L API AFFICHE LE CLASSEMENT GENERAL TOUS JEUX CONFONDUS ***")
        return self.make_choice()

    def aff_class_oie(self):
        print("*** API affiche le top du classement et votre position ***")
        return self.make_choice()

    def aff_class_p4(self):
        print("*** API affiche le top du classement et votre position ***")
        return self.make_choice()

    def aff_stat_perso(self):
        print("*** API AFFICHE NBR DE PARTIES PAR JEU ET NBRE DE VICTOIRE (ET RATIO DE VICTOIRE) ***")
        return self.make_choice()






if __name__ == "__main__": 
    menu_Classement1 = Menu_Classement()
    menu_Classement1.display_info()
    menu_Classement1.make_choice()
