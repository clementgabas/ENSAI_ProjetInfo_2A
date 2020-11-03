#Importation des modules
import PyInquirer as inquirer
from Vues.abstractView import AbstractView

from printFunctions import timePrint as print
import requests
import json
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
                return self.modif_pseudo()
            elif self.reponse["menu_Modif_Info"] == "Modifier mon mot de passe":
                return self.modif_mdp()
            elif self.reponse["menu_Modif_Info"] == "Revenir au menu précédent":
                import Vues.menu_Profil as MP
                Retour = MP.Menu_Profil(self.pseudo)
                Retour.display_info()
                return Retour.make_choice()
            else:
                print("Une erreur est survenur dans menu_Mod_Inf.make_choice")
            break

    def modif_mdp(self):
        self.mdpQ = [
            {
                'type' : 'password',
                'name' : 'Old_Password',
                'message' : "Veuillez insérer votre ancien mot de passe",
            },
            {
                'type': 'password',
                'name': 'New_Password',
                'message': "Veuillez insérer votre nouveau mot de passe",
            },
            {
                'type': 'password',
                'name': 'Password_Check',
                'message': "Veuillez confirmer votre mot de passe",
            },
        ]
        while True:
            self.mdpR = inquirer.prompt(self.mdpQ)
            old_mdp = self.mdpR["Old_Password"]
            new_mdp1, new_mdp2 = self.mdpR["New_Password"], self.mdpR["Password_Check"]

            if new_mdp1 != new_mdp2:
                print("Les deux nouveaux mots de passes ne correspondent pas.")
                return self.echec_modif_mdp()
            print("*** PHASE DE MODIF DU MOT DE PASSE DANS L API... ON SIMULE ICI ***")

            #on envoit à l'api ancien et nouveau mdp. Elle vérifie si l'ancien est bon puis si le nouveau est valide. Enfin elle effectue les changement et return True
            is_old_correct = True
            is_new_legit = True
            has_API_worked = True

            if not is_old_correct:
                print("L'ancien mot de passe donné n'est pas bon.")
                return self.echec_modif_mdp()
            if not is_new_legit:
                print("Le nouveau mot de passe ne vérifie pas les conditions (au moins 8 caractères, une minuscule, une majuscule, un chiffre et un caractère spécial.")
                return self.echec_modif_mdp()
            if has_API_worked:
                print("Votre mot de passe a bien été modifié!")
                return self.make_choice()
            else:
                prin("Une erreur est survenue dans la communication avec l' dans modif_mdp.")
                return self.make_choice()
            break

    def echec_modif_mdp(self):
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
                return self.modif_mdp()
            elif self.echecMdpR["Retour"] == "Retourner au menu des informations personnelles":
                return self.make_choice()
            else:
                print("Erreur dans echec_modif_mdp")
            break

    def modif_pseudo(self):
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

                if new_pseudo == self.pseudo:
                    print("Le nouveau pseudo est identique à l'ancien.")
                    return self.echec_modif_pseudo()

                dataPost = {'old_pseudo': self.pseudo, 'new_pseudo': new_pseudo}
                res = request.put('http://localhost:9090/home/main/profil/user', data=json.dumps(dataPost))

                if res.status_code == 409:
                    print("Le pseudo demandé est déjà utilisé.")
                    return self.echec_modif_pseudo()
                elif res.status_code == 200:
                    print("Le pseudo a été mis à jour.")
                    return self.make_choice()
                elif res.status_code == 404:
                    print("erreur, l'api n'a pas été trouvée")
                    return self.echec_modif_pseudo()
                elif res.status_code == 500:
                    return print("erreur dans le code de l'api")
                else:
                    print("erreur non prévue : " + str(res.status_code))
                    return self.echec_modif_pseudo()

    def echec_modif_pseudo(self):
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
                return self.modif_pseudo()
            elif self.echecPseudoR["Retour"] == "Retourner au menu des informations personnelles":
                return self.make_choice()
            else:
                print("Erreur dans echec_modif_pseudo")
            break



if __name__ == "__main__": 
    menu_Modif1 = Menu_Modif_Inf()
    menu_Modif1.display_info()
    menu_Modif1.make_choice()