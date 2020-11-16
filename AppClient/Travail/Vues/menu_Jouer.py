import PyInquirer as inquirer
from Vues.abstractView import AbstractView
from Player.PlayerClass import Player
import time

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
        self.print_grille(Resultat["Grille"])

        Resultat1 = Player1.demander_si_vainqueur()
        if not Resultat1["Statut"]:
            win, self_win = False, False

            Resultat2 = Player1.jouer_son_tour(self.jouer_son_tour())
            self.print_message(Resultat2)
            if not Resultat2["Statut"]:
                return self.jouer_un_tour()

            Resultat3 = Player1.demander_grille()
            self.print_message(Resultat3)
            self.print_grille(Resultat3["Grille"])

            Resultat4 = Player1.demander_si_vainqueur()
            if Resultat4["Statut"]:
                win, self_win = True, True
        else:
            win, self_win = True, False
        return {"win": win, "self_win": self_win}



    def print_grille(self, _grid):
        self.nbcolumn, self.nbline = 7, 7

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
                    line = line + " X |"

                elif _grid[j][i] == 2:
                    line = line + " O |"

            print(line)
            print(separator)
            line = "|"
        print(abscisse)


    def jouer_son_tour(self):
        action = inquirer.prompt(self.action_jouer)
        #actoion --> {'action': '2'}
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
        return self.passer_tour(win_bool=True)

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

    def passer_tour(self, win_bool=False):
        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.passer_tour()
        self.print_message(Resultat)
        if Resultat["Statut"] and not win_bool:
            return self.jouer()
        elif Resultat["Statut"] and win_bool:
            pass
        else:
            print(f"erreur dans le passage de tour pour le joueur {self.pseudo}")


    def quitter_partie(self):
        pass