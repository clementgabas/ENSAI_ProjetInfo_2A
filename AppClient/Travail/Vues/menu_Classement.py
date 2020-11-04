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


    def aff_class_gen(self):
        # -- connexion à l'API
        res = requests.get('http://localhost:9090/home/main/profil/classment')

        if res.status_code == 200:
            classement_general = res.json()["classement_general"]
            print("\n" + tabulate(classement_general, headers=["Pseudo", "score"], tablefmt="grid"))

            return self.make_choice()
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            return self.make_choice()
        elif res.status_code == 500:
            return print("erreur dans le code de l'api")
        else:
            print("erreur non prévue : " + str(res.status_code))
            return self.make_choice_retour()

    def aff_class_oie(self):
        # -- connexion à l'API
        res = requests.get('http://localhost:9090/home/main/profil/classment')

        if res.status_code == 200:
            classement_jeu_oie = res.json()["classement_jeu_oie"]
            print("\n" + tabulate(classement_jeu_oie, headers=["Pseudo", "score"], tablefmt="grid"))

            return self.make_choice()
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            return self.make_choice()
        elif res.status_code == 500:
            return print("erreur dans le code de l'api")
        else:
            print("erreur non prévue : " + str(res.status_code))
            return self.make_choice_retour()

    def aff_class_p4(self):
        # -- connexion à l'API
        res = requests.get('http://localhost:9090/home/main/profil/classment')

        if res.status_code == 200:
            classement_p4 = res.json()["classement_p4"]
            print("\n" + tabulate(classement_p4, headers=["Pseudo", "score"], tablefmt="grid"))

            return self.make_choice()
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            return self.make_choice()
        elif res.status_code == 500:
            return print("erreur dans le code de l'api")
        else:
            print("erreur non prévue : " + str(res.status_code))
            return self.make_choice_retour()






if __name__ == "__main__": 
    menu_Classement1 = Menu_Classement()
    menu_Classement1.display_info()
    menu_Classement1.make_choice()
