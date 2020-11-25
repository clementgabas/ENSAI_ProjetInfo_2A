import PyInquirer as inquirer

from Vues.abstractView import AbstractView

from Vues.usefulfonctions.printFunctions import timePrint as print
from tabulate import tabulate


# Création du menu ami.

class Menu_Ami(AbstractView):
    def __init__(self, pseudo="user"):
        self.questions = [
            {
                'type': 'list',
                'name': 'menu_Ami',
                'message': "Que souhaitez-vous faire ?",
                'choices': [
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
        # print("Bienvenue sur le menu ami")
        pass

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)

            if self.reponse["menu_Ami"] == "Ajouter un ami":
                return self.menu_ajout_ami()
            elif self.reponse["menu_Ami"] == "Supprimer un ami":
                return self.menu_supp_ami()
            elif self.reponse["menu_Ami"] == "Afficher ma liste d\'amis":
                return self.menu_voir_liste_ami()
            elif self.reponse["menu_Ami"] == "Revenir au menu précédent":
                import Vues.menu_Profil as MP
                Retour = MP.Menu_Profil(self.pseudo)
                Retour.display_info()
                return Retour.make_choice()
            else:
                print("erreur")
            break

    def menu_ajout_ami(self):
        self.ajoutAmiQ = [
            {
                'type': 'input',
                'name': 'pseudo_ami',
                'message': "Veuillez fournir le pseudo de l'ami à ajouter à la liste des amis :",
            }
        ]
        while True:
            self.ajoutAmiR = inquirer.prompt(self.ajoutAmiQ)
            pseudo_ami = self.ajoutAmiR["pseudo_ami"].lower()
            from Player.UserClass import User
            User1 = User(self.pseudo)
            Resultat = User1.ajout_ami(pseudo_ami)
            self.print_message(Resultat)
            if Resultat["Statut"] == False:
                return (self.menu_echec_ajout_ami())
            elif Resultat["Statut"] == True:
                return(self.make_choice())
            else:
                print("Erreur non prévue")
                return (self.menu_echec_ajout_ami())

    def menu_echec_ajout_ami(self):
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
                return self.menu_ajout_ami()
            elif self.echecAjoutAmiR["Retour"] == "Retourner au menu de la liste des amis":
                return self.make_choice()
            else:
                print("Erreur dans echec_ajout_ami")
            break

    def menu_supp_ami(self):
        self.suppAmiQ = [
            {
                'type': 'input',
                'name': 'ami_supp',
                'message': "Veuillez fournir le pseudo de l'ami à supprmier de la liste des amis.",
            }
        ]
        while True:
            self.suppAmiR = inquirer.prompt(self.suppAmiQ)
            pseudo_ami = self.suppAmiR["ami_supp"].lower()

            from Player.UserClass import User
            User1 = User(self.pseudo)
            Resultat = User1.supp_ami(pseudo_ami)
            self.print_message(Resultat)
            if Resultat["Statut"] == False:
                return (self.menu_echec_supp_ami())
            elif Resultat["Statut"] == True:
                return (self.make_choice())
            else:
                print("Erreur non prévue")
                return (self.menu_echec_supp_ami())

    def menu_echec_supp_ami(self):
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
                return self.menu_supp_ami()
            elif self.echecsuppAmiR["Retour"] == "Retourner au menu de la liste des amis":
                return self.make_choice()
            else:
                print("Erreur dans echec_supp_ami")
            break

    def menu_voir_liste_ami(self):

        from Player.UserClass import User
        User1 = User(self.pseudo)
        Resultat = User1.afficher_amis()
        self.print_message(Resultat)
        if Resultat["Statut"] == False:
            return (self.make_choice())
        elif Resultat["Statut"] == True:
            self.afficher_liste_amis(liste_amis = Resultat["Liste_amis"])
            return (self.make_choice())
        else:
            print("Erreur non prévue")
            return (self.make_choice())

    def afficher_liste_amis(self, liste_amis):
        return print("\n" + tabulate(liste_amis, headers=["Pseudo", "Date d'ajout", "Est connecté?", "En partie?"],
                                  tablefmt="grid"))



if __name__ == "__main__":
    menu_Ami1 = Menu_Ami()
    menu_Ami1.display_info()
    menu_Ami1.make_choice()

# Comment