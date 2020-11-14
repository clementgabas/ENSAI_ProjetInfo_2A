import PyInquirer as inquirer
from Vues.abstractView import AbstractView


from printFunctions import timePrint as print
import requests
import json


class Jouer(AbstractView):
    def __init__(self, pseudo, id_salle, jeu, est_chef):
        self.pseudo = pseudo.lower()
        self.game = jeu.lower()
        self.id_salle = id_salle
        self.est_chef = est_chef

        if self.game == 'oie':
            self.action_jouer = [
                {
                    'type': 'input',
                    'name': 'action jeu oie',
                    'message' : "Pour jeter les dés, veuillez appuyer sur la touche entrée."
                }
            ]
        elif self.game == 'p4':
            self.action_jouer = [
                {
                    'type': 'input',
                    'name': 'action jeu p4',
                    'message': "Veuillez saisir le numéro de la colonne dans laquelle vous souhaitez jouer votre pion."
                }
            ]
        else:
            self.action_jouer = [{'type':'list', 'message':'bug dans classe jouer.'}]

    def get_choix_joueur(self):
        action = inquirer.prompt(self.action_jouer)
        return action

    def get_plateau_de_jeu(self):
        #-- requetage de l'api pour récupérer le plateau de jeu afin de pouvoir l'afficher
        pass

    def print_plateau_de_jeu(self):
        plateau = self.get_plateau_de_jeu()
        #-- on fait notre blabla mais au final on affiche le tableau de jeu
        pass

    def jouer_son_tour(self):
        #1) on récupère et affiche le tableau de jeu
        self.print_plateau_de_jeu()

        #2) en demande au user son action
        action = self.get_choix_joueur()

        #3) on envoit à l'api l'action du joueur afin qu'elle puisse nous dire si le coup est valide et pris en compte ou s'il doit rejouer
        dataPost = {'pseudo': self.pseudo, 'id_salle': self.id_salle, 'coup': action}
        res = requests.post(addresse, data=json.dumps(dataPost))

        if res.status_code == 200: #le coup est valide et a donc été enregistré et joué
            print("Le coup a bien été pris en compte.")
        elif res.status_code == 401: #le coup n'est pas valide et il faut donc rejouer
            raison = res.json()["raison"]
            print(f"Le coup n'est pas valide pour la raison suivante : {str(raison)}. Merci de rejouer.")
            return self.jouer_son_tour()

    def get_etat_partie(self):
        #1) on requete l'api pour qu'elle vérifie si la partie est finie
        dataPost = {'id_salle': self.id_salle}
        res = requests.get(addresse, json.dumps(dataPost))

        etat_partie = res.json()['etat partie']
        if etat_partie == 'en cours': #la partie n'est pas finie
            pass
        elif etat_partie == 'finie':
            winner = res.json()["winner"]
            print(f"La partie est finie, le vainqueur est {winner}!")

    def jouer(self):
        self.jouer_son_tour()
        self.get_etat_partie()


