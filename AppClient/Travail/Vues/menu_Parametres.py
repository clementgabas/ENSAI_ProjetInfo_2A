import PyInquirer as inquirer
from abc import ABC
import requests
import json

parametre_standard_P4 = {"duree_tour" :30,"condition_victoire" : 4,"Taille_plateau" :42}

class Abstract_Parametre(ABC):
    def __init__(self,id_Partie,id_Jeu):
        self.questions = [
            {
                'type': 'list',
                'name': 'menu_Parametre',
                'message': "Que souhaitez-vous faire ?",
                'choices': [
                    'Jouer une partie selon les règles officielles',
                    'Créer une partie personnalisée',
                    inquirer.Separator(),
                    'Revenir au menu précédent',
                ]
            },
        ]
        self.id_Partie = id_Partie
        self.id_Jeu = id_Jeu
        def display_info(self):
            pass  # on a rien d'intéressant à dire ici

        def make_choice(self):
            pass


class Menu_Parametre_P4(Abstract_Parametre):
    def __init__(self,id_Partie,id_Jeu,parametre_standard_P4):
        Abstract_Parametre.__init__(self,id_Partie,id_Jeu)
        self.parametre_standard_P4 = parametre_standard_P4

    def display_info(self):
        pass  # on a rien d'intéressant à dire ici

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.questions)
            if self.reponse["menu_Parametre"] == "Jouer une partie selon les règles officielles":
                    return creer_partie_standard_P4()
            elif self.reponse["menu_Parametre"] == "Créer une partie personnalisée":
                    return creer_partie_perso_P4()
            elif self.reponse["menu_Parametre"] == "Revenir au menu précédent":
                pass
                #print("Vous allez être redirigé vers le menu précédent.")
                #import Vues.Menu_Utilisateur_Co as MUC
                #Retour = MUC.Menu_Utilisateur_Co(pseudo=self.pseudo, jeu=self.game)
                #Retour.display_info()
                #return Retour.make_choice()
            else:
                print("Réponse invalide dans le Menu_Parametre.Menu_Parametre.make_choice()")
            break

    def creer_partie_standard_P4(self):
        dataPost = {"id_Partie": self.id_Partie, "id_jeu" : self.id_Jeu, "duree_tour" : parametre_standard_P4["duree_tour"],
                    "condition_victoire" : parametre_standard_P4["condition_victoire"], "Taille_plateau" : parametre_standard_P4["Taille_plateau"]}

        res = requests.post('http://localhost:9090/home/game/room/settings', data=json.dumps(dataPost))
        if res.status_code == 200:
            print("Votre partie est définie  selon des paramètres standard.")
        elif res.status_code == 404:
            print("erreur, l'api n'a pas été trouvée")
            return self.make_choice()
        elif res.status_code == 500:
            return print("erreur dans le code de l'api")
        else:
            print("erreur non prévue : " + str(res.status_code))
            return self.make_choice_retour()

    def creer_partie_perso_P4(self):
        parametre_perso = {}
        questions_parametre_partie_perso_P4 = [
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
                    'Revenir au menu précédent',

                ]
            },
        ]

        while True:
            reponse_partie_perso_P4 = inquirer.prompt(questions_parametre_partie_perso_P4)
            if reponse_partie_perso_P4["menu_Param_Perso"] == "Durée des tours":
                questions_tour_perso_P4 = [
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
                parametre_perso["duree_tour"] = inquirer.prompt(questions_tour_perso_P4)

            elif reponse_partie_perso_P4["menu_Param_Perso"] == "Condition de victoire":
                questions_Cond_Vict_perso_P4 = [
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
                parametre_perso["condition_victoire"] = inquirer.prompt(questions_Cond_Vict_perso_P4)

            elif reponse_partie_perso_P4["menu_Param_Perso"] == "Taille du plateau":
                questions_Taille_Plateau_perso_P4 = [
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
                parametre_perso["Taille_plateau"] = inquirer.prompt(questions_Taille_Plateau_perso_P4)

            elif reponse_partie_perso_P4["menu_Param_Perso"] == "Sauvegarder les paramètres et revenir au salon":
                print(parametre_perso)
                return(False)
            elif reponse_partie_perso_P4["menu_Param_Perso"] == "Revenir au menu précédent":
                pass

        dataPost = {"id_Partie": self.id_Partie, "id_jeu" : self.id_Jeu, "duree_tour" : 30, "condition_victoire" : 4, "Taille_plateau" : 42}
        res = requests.post('http://localhost:9090/home/game/room/settings', data=json.dumps(dataPost))

@app.route('/home/game/room/settings', methods=['POST']) #ajout de parametre

def ajout_param_partie_P4():
    request.get_json(force=True)
    id_Partie, id_jeu, duree_tour, condition_victoire, Taille_plateau  = request.json.get('id_Partie'), request.json.get('id_jeu'), request.json.get('duree_tour'), request.json.get('condition_victoire'),  request.json.get('Taille_plateau')
    DAOparametre.add_parametre(id_Partie, id_jeu, duree_tour, condition_victoire, Taille_plateau)
    print(f"Les paramètres suivants : Durée d'un tour : {duree_tour} secondes \n Condition de victoire : aligner {condition_victoire} jetons \n Taille du plateau : {Taille_plateau} \n ont a bien été définis pour la partie {id_Partie}")
    response = {"status_code": http_codes.ok, "message": "Paramètres enregistrés."}  # code 200
    return make_reponse(response, http_codes.ok)  # code 200
