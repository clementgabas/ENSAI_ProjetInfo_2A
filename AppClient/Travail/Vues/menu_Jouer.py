import PyInquirer as inquirer
from Vues.abstractView import AbstractView
from Player.PlayerClass import Player
import time
import random as rd
import colorama
colorama.init()

#from printFunctions import timePrint as print



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
                    'name': 'action',
                    'message' : "Pour jeter les dés, veuillez appuyer sur la touche entrée."
                }
            ]
        elif self.game == 'p4':
            self.action_jouer = [
                {
                    'type': 'input',
                    'name': 'action',
                    'message': "Veuillez saisir le numéro de la colonne dans laquelle vous souhaitez jouer votre pion."
                }
            ]
        else:
            self.action_jouer = [{'type':'list', 'message':'bug dans classe jouer.'}]


    def jouer_un_tour(self):
        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.demander_grille()
        self.print_message(Resultat)
        self.print_grille(Resultat["Grille"], Resultat["liste_couleur_ordonnee"])

        Resultat1 = Player1.demander_si_vainqueur()
        if not Resultat1["Statut"]:
            win, self_win = False, False

            Resultat2 = Player1.jouer_son_tour(self.jouer_son_tour())
            self.print_message(Resultat2)
            if not Resultat2["Statut"]:
                return self.jouer_un_tour()

            Resultat3 = Player1.demander_grille()
            self.print_message(Resultat3)
            self.print_grille(Resultat3["Grille"], Resultat3["liste_couleur_ordonnee"])

            Resultat4 = Player1.demander_si_vainqueur()
            if Resultat4["Statut"]:
                win, self_win = True, True
        else:
            win, self_win = True, False
        return {"win": win, "self_win": self_win}



    def print_grille(self, _grid, liste_couleur_ordonnee):
        self.nbcolumn, self.nbline = 7, 7

        def get_symbole_couleur(_color):
            if _color == "rouge":
                return " \033[30;41;1m  \033[0m"
            elif _color == "vert":
                return " \033[30;42;1m  \033[0m"
            elif _color == "jaune":
                return " \033[30;43;1m  \033[0m"
            elif _color == "bleu":
                return " \033[30;44;1m  \033[0m"
            elif _color == "magenta":
                return " \033[30;45;1m  \033[0m"
            elif _color == "cyan":
                return " \033[30;46;1m  \033[0m"
            elif _color == "blanc":
                return " \033[30;47;1m  \033[0m"

        if self.game.lower() == "p4":
            line = "|"
            separator = "-"
            abscisse = " "
            for k in range(self.nbline):
                separator = separator + "----"

                if k == 0:
                    abscisse = 2 * abscisse + str(k) + "   "

                elif k >= 10:
                    abscisse = abscisse + str(k) + "  "

                else:
                    abscisse = abscisse + str(k) + "   "

            print(separator)
            for i in range(self.nbcolumn - 1, -1, -1):
                for j in range(self.nbline):

                    if _grid[j][i] == 0:
                        line = line + "   |"

                    elif _grid[j][i] == 1:
                        carre_col = get_symbole_couleur(liste_couleur_ordonnee[0][0])
                        line = line + carre_col + "|"

                    elif _grid[j][i] == 2:
                        carre_col = get_symbole_couleur(liste_couleur_ordonnee[1][0])
                        line = line + carre_col + "|"

                print(line)
                print(separator)
                line = "|"
            print(abscisse)
        elif self.game.lower() == 'oie':
            pass

    def jouer_son_tour(self):
        action = inquirer.prompt(self.action_jouer)
        if self.game.lower() == 'p4':
            pass
            #actoion --> {'action': '2'}
        elif self.game.lower() == 'oie':
            dice1, dice2 = rd.randint(1, 6), rd.danint(1, 6)
            dice1 += dice2*0.1
            action = {'action': dice1}
            #action --> {'action': 1.6 ou 3.2 ou 2.3
        return action

    def jouer(self):
        monTour = False
        count = 0
        while not monTour:
            count += 1
            if count == 1:
                print("Ce n'est pas votre tour.. Merci de patienter en attendant votre tour.")
            monTour = self.demander_tour()
            time.sleep(0.5)
        print("C'est votre tour!")
        dico = self.jouer_un_tour()
        win, self_win = dico["win"], dico["self_win"]
        if not win:
            return self.passer_tour()
        else:
            if self_win:
                print("Vous avez gagné!")
            else:
                print("Vous avez perdu!")
            print("Il faut gérer les points!")
        return self.passer_tour(win_bool=True, self_win=self_win)

    def demander_tour(self):
        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.demander_tour()
        #self.print_message(Resultat)
        if Resultat["Statut"]:
            #c'est votre tour de jouer
            pass
        elif not Resultat["Statut"]:
            pass
        else:
            print("erreur dans menu_salon.demander_tour")
        return Resultat["Statut"]

    def passer_tour(self, win_bool=False, self_win=False):
        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.passer_tour()
        self.print_message(Resultat)
        if Resultat["Statut"] and not win_bool:
            return self.jouer()
        elif Resultat["Statut"] and win_bool:
            return self.gestion_fin_partie(self_win)
        else:
            print(f"erreur dans le passage de tour pour le joueur {self.pseudo}")

    def gestion_fin_partie(self, self_win):
        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.gestion_fin_partie(self_win)
        self.print_message(Resultat)
        if Resultat["Statut"]:
            print("Vous allez être renvoyés vers le menu principal")
            import Vues.menu_Utilisateur_Co as MUC
            Retour = MUC.Menu_User_Co(self.pseudo)
            Retour.display_info()
            return Retour.make_choice()
        else:
            print("erreur dans menuJouer.gestion_fin_partie")