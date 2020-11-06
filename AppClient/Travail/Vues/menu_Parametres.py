import PyInquirer as inquirer
import requests
import json


class Menu_Parametre():
    def __init__(self,pseudo, id_salle, jeu, est_chef):
        self.pseudo = pseudo.lower()
        self.game = jeu.lower()
        self.id_salle = id_salle
        self.est_chef = est_chef
        self.parametre = {"duree_tour" :30,"condition_victoire" : 4, "Taille_plateau" : "7 x 6"}

    def display_info(self):
        pass

    def make_choice(self):
        if self.game == "p4":
            self.questions_parametre_partie_perso = [
                {
                    'type': 'list',
                    'name': 'menu_Param_Perso',
                    'message': "Quel paramètre souhaitez-vous modifier ?",
                    'choices': [
                        'Durée des tours',
                        'Condition de victoire',
                        'Taille du plateau',
                        inquirer.Separator(),
                        'Sauvegarder les paramètres et revenir au salon',
                        'Abandonner et revenir au salon',
                    ]
                },
            ]

            while True:
                self.reponse_partie_perso = inquirer.prompt(self.questions_parametre_partie_perso)
                if self.reponse_partie_perso["menu_Param_Perso"] == "Durée des tours":
                    questions_tour_perso = [
                        {
                            'type': 'list',
                            'name': 'menu_Tour_Perso',
                            'message': "Veuilliez choisir la durée d'un tour.",
                            'choices': [
                                '10 secondes',
                                '15 secondes',
                                '20 secondes',
                            ]
                        },
                    ]
                    self.parametre["duree_tour"] = inquirer.prompt(questions_tour_perso)["menu_Tour_Perso"]

                elif self.reponse_partie_perso["menu_Param_Perso"] == "Condition de victoire":
                    questions_Cond_Vict_perso = [
                        {
                            'type': 'list',
                            'name': 'menu_Cond_Vict_Perso',
                            'message': "Veuilliez choisir le nombre de jetons à aligner pour remporter la partie.",
                            'choices': [
                                '3',
                                '4',
                                '5',
                            ]
                        },
                    ]
                    self.parametre["condition_victoire"] = inquirer.prompt(questions_Cond_Vict_perso)["menu_Cond_Vict_Perso"]

                elif self.reponse_partie_perso["menu_Param_Perso"] == "Taille du plateau":
                    questions_Taille_Plateau_perso = [
                        {
                            'type': 'list',
                            'name': 'menu_Taille_Plateau_Perso',
                            'message': "Veuilliez choisir la durée d'un tour.",
                            'choices': [
                                '6 x 5',
                                '7 x 6',
                                '8 x 7',
                            ]
                        },
                    ]
                    self.parametre["Taille_plateau"] = inquirer.prompt(questions_Taille_Plateau_perso)["menu_Taille_Plateau_Perso"]

                elif self.reponse_partie_perso["menu_Param_Perso"] == "Sauvegarder les paramètres et revenir au salon":
                    self.creer_partie_perso_P4()

                elif self.reponse_partie_perso["menu_Param_Perso"] == "Abandonner et revenir au salon":
                    import Vues.menu_Salon as MS
                    Retour = MS.Salon(self.pseudo, self.id_salle, self.game, self.est_chef)
                    Retour.display_info()
                    return Retour.make_choice()

    def display_info(self):
        pass


    def creer_partie_standard_P4(self):
        dataPost = {"id_salle": self.id_salle, "duree_tour" : self.parametre["duree_tour"],
                    "condition_victoire" : self.parametre["condition_victoire"], "Taille_plateau" : self.parametre["Taille_plateau"]}
        res = requests.post('http://localhost:9090/home/game/room/settings', data=json.dumps(dataPost))
        if res.status_code == 200:
            print("Votre partie est définie  selon des paramètres standard.")
            import Vues.menu_Salon as MS
            Retour = MS.Salon(self.pseudo, self.id_salle, self.game, self.est_chef)
            Retour.display_info()
            return Retour.make_choice()

        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            return self.make_choice()

        elif res.status_code == 500:
            return print("erreur dans le code de l'api")

        else:
            print("erreur non prévue : " + str(res.status_code))
            return self.make_choice_retour()

    def creer_partie_perso_P4(self):
        dataPost = {"id_Partie": self.id_salle, "duree_tour" : self.parametre["duree_tour"], "condition_victoire" : self.parametre["condition_victoire"], "Taille_plateau" : self.parametre["Taille_plateau"]}
        res = requests.post('http://localhost:9090/home/game/room/settings', data=json.dumps(dataPost))
        if res.status_code == 200:
            print(f"Votre partie est définie  selon des les paramètres suivants : \n  Durée des tours : {self.parametre['duree_tour']} secondes \n Condition de victoire : Aligner {self.parametre['condition_victoire']} jetons \n Taille du plateau : {self.parametre['Taille_plateau']}")
            import Vues.menu_Salon as MS
            Retour = MS.Salon(self.pseudo, self.id_salle, self.game, self.est_chef)
            Retour.display_info()
            return Retour.make_choice()

        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            return self.make_choice()

        elif res.status_code == 500:
            return print("erreur dans le code de l'api")

        else:
            print("erreur non prévue : " + str(res.status_code))
            return self.make_choice()
