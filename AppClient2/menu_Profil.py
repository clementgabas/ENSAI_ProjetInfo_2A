#Importation des modules
import PyInquirer as inquirer
from abstractView import AbstractView
import menu_Mod_Inf as MMI
import menu_Amis as MA
import menu_Classement as MC


from printFunctions import timePrint as print

#Création du menu profil

class Menu_Profil(AbstractView):
    def __init__(self):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Profil',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Accéder à mes informations personnelles',
                              'Accéder à ma liste d\'amis',
                              'Accéder aux classements',
                              inquirer.Separator(),
                              'Revenir au menu précédent',
                          ]
            },
        ]

    def display_info(self):
        #print("Bienvenue sur le menu profil")
        pass

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)

            if self.reponse["menu_Profil"] == "Accéder à mes informations personnelles":
            	InfPerso = MMI.Menu_Modif_Inf()
            	InfPerso.display_info()
            	return InfPerso.make_choice()

            elif self.reponse["menu_Profil"] == "Accéder à ma liste d\'amis":
                Amis = MA.menu_Amis()
                Amis.display_info()
                return Amis.make_choice()

            elif self.reponse["menu_Profil"] == "Accéder au classement":
            	Classement = MC.Menu_Classement()
            	Classement.display_info()
            	return Classement.make_choice()

            elif self.reponse["menu_Profil"] == "Revenir au menu précédent":
            	import menu_Utilisateur_Co as MUC
            	Retour = MUC.Menu_User_Co()
            	Retour.display_info()
            	return Retour.make_choice()
            else:
            	print("Erreur dans menu_Profil.Menu_Profil.make_choice")
            break



if __name__ == "__main__": 
    menu_Profil1 = Menu_Profil()
    menu_Profil1.display_info()
    menu_Profil1.make_choice()
