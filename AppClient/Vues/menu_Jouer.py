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

        print("\n")

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
            print("\n")

        elif self.game.lower() == 'oie':
            #-- on récupère une grille sous la forme du dico suivant :
            #-- {'pseudo1' : {'Joueur' : pseudo, 'Couleur' : color, 'Ordre_de_jeu' : ordre, 'nbwaitingturn' : nbwaitingturn, 'actualbox' : actualbox, 'previousbox' : previousbox}
            nbBoxByLine = 8  # **************************************
            nbBox = 63
            caseWidth = 13
            lineType = "|"
            linePlayer = "|"
            lineNumber = "|"
            separator = "-"
            l = nbBoxByLine  # **************************************
            for k in range(nbBoxByLine):  # **************************************
                separator = separator + "--------------"

            def set_boxList():
                boxList = []
                for i in range(nbBox + 1):
                    if i in (12, 6): #on a sorti la case 6
                        box = "Bridge"
                    elif i in (23,):
                        box = "Hotel"
                    elif i in (26,):
                        box = "Dice63"
                    elif i in (31,):
                        box = "Well"
                    elif i in (42,):
                        box = "Labyrinth"
                    elif i in (52,):
                        box = "Jail"
                    elif i in (53,):
                        box = "Dice54"
                    elif i in (58,):
                        box = "skull"
                    elif i in (14, 18, 23, 27, 32, 36, 41, 45, 50, 54, 59):
                        box = "Goose"
                    else:
                        box = "None"
                    boxList.append(box)
                return boxList

            boxList = set_boxList()
            for i in range(nbBox, -1, -1):
                addType = ""
                box = boxList[i]
                if box != "None":
                    mid = int((caseWidth - len(addType)) / 2)
                    for h in range(mid - int(len(box) / 2)):
                        addType = addType + " "
                    addType = addType + box
                for h in range(caseWidth - len(addType)):
                    addType = addType + " "
                lineType = lineType + addType + "|"
                # creation des joueurs
                addPlayer = ""
                #nbPlayer = 0  # compte le nombre de joueur pour decrementer de 3 la largeur de case
                playerPrint = ""
                playerLenght = 0
                for joueur in _grid:
                    player = _grid[joueur]
                    # print(player)
                    if int(player["actualbox"]) == i:
                        playerPrint = playerPrint + get_symbole_couleur(str(player["Couleur"]))
                        playerLenght = playerLenght + 3
                midPlayer = int((caseWidth - playerLenght)/2)
                for h in range(midPlayer):
                    addPlayer = addPlayer + " "
                addPlayer = addPlayer + playerPrint
                for n in range(caseWidth - playerLenght - midPlayer):
                    addPlayer = addPlayer + " "
                linePlayer = linePlayer + addPlayer + "|"
                # creation du numero de case
                addNumber = ""
                if i == 0:
                    addNumber = "    Départ   "
                elif i == nbBox:
                    addNumber = "     Fin     "
                else:
                    midNumber = int((caseWidth - len(str(i))) / 2)
                    for g in range(midNumber):
                        addNumber = addNumber + " "
                    addNumber = addNumber + str(i)
                    for h in range(caseWidth - len(addNumber)):
                        addNumber = addNumber + " "
                lineNumber = lineNumber + addNumber + "|"
                l = l - 1
                if l == 0 and i != 0:
                    print(separator)
                    print(lineType)
                    print(linePlayer)
                    print(lineNumber)
                    lineType = "|"
                    linePlayer = "|"
                    lineNumber = "|"
                    l = nbBoxByLine  # **************************************
            print(separator)
            print(lineType)
            print(linePlayer)
            print(lineNumber)
            print(separator)
            # print("Pour le moment, on a la grille comme ca mais on va la print joliement tkt")
            # print(_grid)

    def jouer_son_tour(self):
        action = inquirer.prompt(self.action_jouer)
        if self.game.lower() == 'p4':
            pass
            #actoion --> {'action': '2'}
        elif self.game.lower() == 'oie':
            dice1, dice2 = rd.randint(1, 6), rd.randint(1, 6)
            print(f"Vous avez jeter un {dice1} et un {dice2}")
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
        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef,)
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