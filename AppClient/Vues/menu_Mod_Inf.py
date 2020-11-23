import PyInquirer as inquirer

from Vues.abstractView import AbstractView

from Vues.usefulfonctions.printFunctions import timePrint as print

from tabulate import tabulate
#Création du menu de mofidification des informations.

class Menu_Modif_Inf(AbstractView):
    def __init__(self, pseudo = "user"):
        self.questions = [
            {
                'type' : 'list',
                'name' : 'menu_Modif_Info',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Modifier mon pseudo',
                              'Modifier mon mot de passe',
                              'Accéder à ses statistiques personnelles',
                              'Réinitialiser ses statistiques personnelles',
                              inquirer.Separator(),
                              'Revenir au menu précédent',
                          ]
            },
        ]
        self.pseudo = pseudo
    def display_info(self):
        #print("Bienvenue sur le menu de modification des informations")
        pass
    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["menu_Modif_Info"] == "Modifier mon pseudo":
                return self.menu_modif_pseudo()
            elif self.reponse["menu_Modif_Info"] == "Modifier mon mot de passe":
                return self.menu_modif_mdp()
            elif self.reponse["menu_Modif_Info"] == "Accéder à ses statistiques personnelles" :
                return self.menu_affich_stat_perso()
            elif self.reponse["menu_Modif_Info"] == "Réinitialiser ses statistiques personnelles" :
                return self.menu_reinit_stat_perso()
            elif self.reponse["menu_Modif_Info"] == "Revenir au menu précédent":
                import Vues.menu_Profil as MP
                Retour = MP.Menu_Profil(self.pseudo)
                Retour.display_info()
                return Retour.make_choice()
            else:
                print("Une erreur est survenur dans menu_Mod_Inf.make_choice")
            break

    def menu_modif_mdp(self):
        self.mdpQ = [
            {
                'type' : 'password',
                'name' : 'Old_Password',
                'message' : "Veuillez insérer votre mot de passe actuel : ",
            },
            {
                'type': 'password',
                'name': 'New_Password',
                'message': "Veuillez insérer votre nouveau mot de passe : ",
            },
            {
                'type': 'password',
                'name': 'Password_Check',
                'message': "Veuillez confirmer votre nouveau mot de passe : ",
            },
        ]
        while True:
            self.mdpR = inquirer.prompt(self.mdpQ)
            old_mdp = self.mdpR["Old_Password"]
            new_mdp1, new_mdp2 = self.mdpR["New_Password"], self.mdpR["Password_Check"]

            from Player.UserClass import User
            User1 = User(self.pseudo)
            Resultat = User1.modifier_mdp(old_mdp,new_mdp1,new_mdp2)
            self.print_message(Resultat)
            if Resultat["Statut"] == True:
                return (self.make_choice())
            elif Resultat["Statut"] == False:
                return (self.menu_echec_modif_mdp())
            else:
                print("Erreur non prévue")
                return (self.menu_echec_modif_mdp())

    def menu_echec_modif_mdp(self):
        self.echecMdpQ = [
            {
                'type': 'list',
                'name': 'Retour',
                'message': "Que souhaitez-vous faire ?",
                    'choices': [
                        'Réessayer',
                        'Retourner au menu des informations personnelles',
                    ]
            },
        ]
        while True:
            self.echecMdpR = inquirer.prompt(self.echecMdpQ)
            if self.echecMdpR["Retour"] == "Réessayer":
                return self.menu_modif_mdp()
            elif self.echecMdpR["Retour"] == "Retourner au menu des informations personnelles":
                return self.make_choice()
            else:
                print("Erreur dans echec_modif_mdp")
            break

    def menu_modif_pseudo(self):
            self.mdpQ = [
                {
                    'type' : 'input',
                    'name' : 'New_Pseudo',
                    'message' : "Veuillez insérer votre nouveau pseudo : ",
                },
            ]
            while True:
                print(f"Votre pseudo actuel est {self.pseudo}.")
                self.mdpR = inquirer.prompt(self.mdpQ)
                new_pseudo = self.mdpR["New_Pseudo"].lower()

                from Player.UserClass import User
                User1 = User(self.pseudo)
                Resultat = User1.modifier_pseudo(new_pseudo)
                self.print_message(Resultat)
                if Resultat["Statut"] == True:
                    self.pseudo = new_pseudo
                    return(self.make_choice())
                elif Resultat["Statut"] == False:
                    return(self.menu_echec_modif_pseudo())
                else:
                    print("Erreur non prévue")
                    return (self.menu_echec_modif_pseudo())

    def menu_echec_modif_pseudo(self):
        self.echecPseudoQ = [
            {
                'type': 'list',
                'name': 'Retour',
                'message': "Que souhaitez-vous faire ?",
                    'choices': [
                        'Réessayer',
                        'Retourner au menu des informations personnelles',
                    ]
            },
        ]
        while True:
            self.echecPseudoR = inquirer.prompt(self.echecPseudoQ)
            if self.echecPseudoR["Retour"] == "Réessayer":
                return self.menu_modif_pseudo()
            elif self.echecPseudoR["Retour"] == "Retourner au menu des informations personnelles":
                return self.make_choice()
            else:
                print("Erreur dans echec_modif_pseudo")
            break

    def menu_affich_stat_perso(self):

        from Player.UserClass import User
        User1 = User(self.pseudo)
        Resultat = User1.acceder_stats_perso()
        self.print_message(Resultat)
        if Resultat["Statut"] == True:
            self.print_stat_perso(Resultat["stat_perso"])
            return (self.make_choice())
        elif Resultat["Statut"] == False:
            return (self.make_choice())
        else:
            print("Erreur non prévue")
            return (self.make_choice())

    def print_stat_perso(self, stat_perso):
        print("\n" + tabulate(stat_perso, headers=["Nombre de parties jouées", "Nombre de parties gagnées",
                                                   "Pourcentage de parties gagnées"], tablefmt="grid"))

    def menu_reinit_stat_perso(self):
        self.Verif_choixQ = [
            {
                'type': 'list',
                'name': 'Retour',
                'message': "Etes-vous sûr.e de vouloir réinitialiser vos statistiques personnelles ?",
                'choices': [
                    'Oui',
                    'Non',
                ]
            },
        ]
        while True:
            self.Verif_choixR = inquirer.prompt(self.Verif_choixQ)
            if self.Verif_choixR["Retour"] == "Non" :
                print("Abandon")
                return self.make_choice()
            elif self.Verif_choixR["Retour"] == "Oui" :
                from Player.UserClass import User
                User1 = User(self.pseudo)
                Resultat = User1.reinitialiser_stats_perso()
                self.print_message(Resultat)
                if Resultat["Statut"] == True:
                    return (self.make_choice())
                elif Resultat["Statut"] == False:
                    return (self.make_choice())
                else:
                    print("Erreur non prévue")
                    return (self.make_choice())
            else:
                print("erreur non prévue : " + str(res.status_code))
                return(self.make_choice())



if __name__ == "__main__": 
    menu_Modif1 = Menu_Modif_Inf()
    menu_Modif1.display_info()
    menu_Modif1.make_choice()