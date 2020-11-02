#Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print

#Création du menu ami.

class Menu_Ami(AbstractView):
    def __init__(self, pseudo="user"):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Ami',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Ajouter un ami',
                              'Supprimer un ami',
                              'Afficher ma liste d\'amis',
                              inquirer.Separator(),
                              'Revenir au menu précédent',
                          ]
            },
        ]
        self.pseudo = pseudo
    def display_info(self):
        #print("Bienvenue sur le menu ami")
        pass
        
    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            
            if self.reponse["menu_Ami"] == "Ajouter un ami":
                return self.ajout_ami()
            elif self.reponse["menu_Ami"] == "Supprimer un ami":
                return self.supp_ami()
            elif self.reponse["menu_Ami"] == "Afficher ma liste d\'amis":
                return self.voir_liste_ami()
            elif self.reponse["menu_Ami"] == "Revenir au menu précédent":
                import Vues.menu_Profil as MP
                Retour = MP.Menu_Profil(self.pseudo)
                Retour.display_info()
                return Retour.make_choice()            
            else:
                print("erreur")
            break
                

    def ajout_ami(self):
        self.ajoutAmiQ = [
            {
                'type': 'input',
                'name': 'ami_add',
                'message': "Veuillez fournir le pseudo de l'ami à ajouter à la liste des amis.",
            }
        ]
        while True:
            self.ajoutAmiR = inquirer.prompt(self.ajoutAmiQ)
            pseudo_a_add = self.ajoutAmiR["ami_add"]

            #on fournit ce pseudo à l'api. Elle vérifie si il existe. Si il existe, elle l'ajoute à la liste de vos amis
            print("*** ON SIMULE QUE L API A BIEN FOCNTIONNE ***")
            does_pseudo_exist = True
            has_API_worked = True

            if not does_pseudo_exist:
                print("Le pseudo a ajouté à votre liste d'ami n'exsite pas.")
                return self.echec_ajout_ami()
            if has_API_worked:
                print("Votre nouvel ami a bien été ajouté à votre liste d'amis.")
                return self.make_choice()
            else:
                print("Erreur dans l'API add_friend.")
            break

    def echec_ajout_ami(self):
        self.echecAjoutAmiQ = [
            {
                'type': 'list',
                'name': 'Retour',
                'message': "Que souhaitez-vous faire ?",
                    'choices': [
                        'Réessayer',
                        'Retourner au menu de la liste des amis',
                    ]
            },
        ]
        while True:
            self.echecAjoutAmiR = inquirer.prompt(self.echecAjoutAmiQ)
            if self.echecAjoutAmiR["Retour"] == "Réessayer":
                return self.ajout_ami()
            elif self.echecAjoutAmiR["Retour"] == "Retourner au menu de la liste des amis":
                return self.make_choice()
            else:
                print("Erreur dans echec_ajout_ami")
            break

    def supp_ami(self):
        self.suppAmiQ = [
            {
                'type': 'input',
                'name': 'ami_supp',
                'message': "Veuillez fournir le pseudo de l'ami à supprmier de la liste des amis.",
            }
        ]
        while True:
            self.suppAmiR = inquirer.prompt(self.suppAmiQ)
            pseudo_a_supp = self.suppAmiR["ami_supp"]

            #on fournit ce pseudo à l'api. Elle vérifie si il existe dans votre liste d'amis. Si il existe, elle le supprime de la liste de vos amis
            print("*** ON SIMULE QUE L API A BIEN FOCNTIONNE ***")
            does_pseudo_exist = True
            is_pseudo_in_your_list = True
            has_API_worked = True

            if not does_pseudo_exist:
                print("Le pseudo à supprimer de votre liste d'ami n'exsite pas.")
                return self.echec_supp_ami()
            if not is_pseudo_in_your_list:
                print("Vous n'êtes pas ami avec cette personne")
                return self.echec_supp_ami()
            if has_API_worked:
                print("Votre nouvel ami a bien été supprimé de votre liste d'amis.")
                return self.make_choice()
            else:
                print("Erreur dans l'API supp_friend.")
            break
    def echec_supp_ami(self):
        self.echecSuppAmiQ = [
            {
                'type': 'list',
                'name': 'Retour',
                'message': "Que souhaitez-vous faire ?",
                    'choices': [
                        'Réessayer',
                        'Retourner au menu de la liste des amis',
                    ]
            },
        ]
        while True:
            self.echecSuppAmiR = inquirer.prompt(self.echecSuppAmiQ)
            if self.echecSuppAmiR["Retour"] == "Réessayer":
                return self.supp_ami()
            elif self.echecsuppAmiR["Retour"] == "Retourner au menu de la liste des amis":
                return self.make_choice()
            else:
                print("Erreur dans echec_supp_ami")
            break

    def voir_liste_ami(self):
        #l'API affiche votre liste d'ami
        print("*** ON SIMULE QUE L API AFFICHE LA LISTE D AMI")
        return self.make_choice()


if __name__ == "__main__": 
    menu_Ami1 = Menu_Ami()
    menu_Ami1.display_info()
    menu_Ami1.make_choice()

#Comment