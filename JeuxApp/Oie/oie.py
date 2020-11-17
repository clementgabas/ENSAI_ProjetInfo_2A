#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""

Created on Fri Oct 09 11:08:42 2020



@author: romanepares

"""

import random

# -- gestion de l'affichage couleur dans le cmd.exe de Windows.

# -- Si vous utilisez ansicon.exe ou un terminal de commande prennant en charge les séquences ANSI, ce package n'est pas nécessaire.

import colorama

colorama.init()


class Player():
    """

    Classe qui gère les paramètres du joueur

    """

    _name = ""  # pseudo

    _color = ""  # couleur pion

    _nbwaitingturn = 1  # nb tours d'attente

    _actualbox = 0  # case actuelle

    _previousbox = 0  # case d'où l'on vient

    def __init__(self):
        """
        Initialisation en entrant le pseudo et la couleur du pion
        """

    def Set_Param(self, name, color):
        self._name = name
        self._color = color

    def set_waitingturn(self, nbwaitingturn):
        """

        Modifier le nombre de tours d'attente

        """

        self._nbwaitingturn = nbwaitingturn

    def get_waitingturn(self):
        """

        Obtenir le nombre de tours d'attente

        """

        return self._nbwaitingturn

    def test_waitingturn(self):
        """

        Tester si le joueur doit encore attendre ou peut jouer

        Retourne True ou False

        Si >1, je le retranche de 1 et je teste pour voir si = à 0

        Valeur par défaut c'est 1

         """

        if self._nbwaitingturn > 1:
            self._nbwaitingturn = self._nbwaitingturn - 1

        return self._nbwaitingturn - 1 == 0

    def freeze_waiting(self):
        """

        Geler le joueur afin qu'il ne joue pas (quand ca devrait être son tour, mais qu'il doit passer son tour)

        """

        self._nbwaitingturn = -1

    def get_actualbox(self):
        """

        Obtenir la case où il se situe actuellement

        """

        return self._actualbox

    def set_actualbox(self, box):
        """
        Définir la case où il se situe
        """
        self._actualbox = box

    def add_dice(self, value):
        """

        Par rapport case actuelle, additionne valeur des dés

        """

        self._actualbox = self._actualbox + value


class Dice:
    """

    Permet de gérer les dés : le lancer, le nb de dés, le nombre de valeurs (faces)

    """

    _numofdice = 0  # nb de dés

    _diceresult = []  # stocker le résultat de chaque dé (sa dimension varie en fct du nb de dés)

    _numoffaces = 0  # nb de faces par dé

    def __init__(self, numofdice, numoffaces):

        """

        Initialisation de la classe dé

        Définir nb dés et nb faces

        En fct nb dés, on définit la dimension du tableau _diceresult

        """

        self._numofdice = numofdice

        self._numoffaces = numoffaces

        for i in range(self._numofdice):
            self._diceresult.append(0)

    def throw(self):

        """

        Jeté de dés : pour chaque dé, on fait un random (entre 1 et nb faces) et on stocke ce résultat dans _diceresult

        """

        for i in range(self._numofdice):
            self._diceresult[i] = random.randint(1, self._numoffaces)

    def dicevalue(self, num):

        """

        Demande le résultat d'un lancer de dé en donnant l'id du dé (_dicevalue[0] donne le premier dé)

        """

        return self._diceresult[num]

    def sumofdices(self):

        """

        Renvoie somme de tous les dés

        """

        s = 0

        for i in range(self._numofdice):
            s = s + self._diceresult[i]

        return s


class Tray(Dice):
    """

    Plateau qui hérité de la classe dé

    Sert à définir le nombre de cases, les particularités des cases

    """

    _nbBox = 1  # nb de cases

    _boxList = []  # tableau de classes 'box'

    def __init__(self, numofdice, numoffaces, nbBox):

        """

        Initialisation nb dés, nb faces et le nb de cases

        """

        self._nbBox = nbBox

        Dice.__init__(self, numofdice, numoffaces)

        # Dimensione le tableau _boxList en fonction de _nbBox

        for i in range(self._nbBox + 1):
            box = Box("None")  # On instancie une classe box

            self._boxList.append(box)  # Qui est ajoutée au tableau _boxList

    def Set_GameByDefault(self):

        """

        On definit les regles par defaut du jeu de l'oie

        """

        self.set_rules(6, "Bridge")

        self.set_rules(9, "Goose")

        self.set_rules(12, "Bridge")

        self.set_rules(14, "Goose")

        self.set_rules(18, "Goose")

        self.set_rules(19, "Hotel")

        self.set_rules(23, "Goose")

        self.set_rules(26, "Dice63")

        self.set_rules(27, "Goose")

        self.set_rules(31, "Well")

        self.set_rules(32, "Goose")

        self.set_rules(36, "Goose")

        self.set_rules(41, "Goose")

        self.set_rules(42, "Labyrinth")

        self.set_rules(45, "Goose")

        self.set_rules(50, "Goose")

        self.set_rules(52, "Jail")

        self.set_rules(53, "Dice54")

        self.set_rules(54, "Goose")

        self.set_rules(58, "Skull")

        self.set_rules(59, "Goose")

    def set_rules(self, boxnumber, boxtype):

        """

        Affecte une règle à une case

        Prend num case et sa règle

        """

        box = self._boxList[boxnumber]  # Récupère l'instance de la box dans le tableau

        box.setType(boxtype)  # Et on lui affecte la règle

    def get_type(self, boxnumber):

        """

        Obtenir la règle d'une case en donnant son numéro

        """

        box = self._boxList[boxnumber]

        return box._boxType

    def search_box(self, start, end, test):

        """

        Cherche la prochaine case ayant pour règle la valeur de test (par rapport au start et au end)

        """

        for i in range(start, end):

            # recherche la première case (suivante) qui a la règle 'test'

            if self.get_type(i) == test:
                return i

        return -1

    def compute_dice(self):

        """

        recherche de combinaison de dés

        """

        dice1 = 0

        dice2 = 0

        # recherche de la combinaison 6 + 3

        for i in range(self._numofdice):

            if self._diceresult[i] == 6:

                dice1 = 1

            elif self._diceresult[i] == 3:

                dice2 = 1

        if dice1 == 1 and dice2 == 1:

            # on recherche la case Dice63

            foundbox = self.search_box(0, self._nbBox, "Dice63")

            if foundbox != -1:
                return foundbox, 1  # retourne le tuple: index de la case Dice63 , combinaison speciale trouve == 1

        dice1 = 0

        dice2 = 0

        # recherche de la combinaison 5 + 4

        for i in range(self._numofdice):

            if self._diceresult[i] == 5:

                dice1 = 1

            elif self._diceresult[i] == 4:

                dice2 = 1

        if dice1 == 1 and dice2 == 1:

            # on recherche la case Dice54

            foundbox = self.search_box(0, self._nbBox, "Dice54")

            if foundbox != -1:
                return foundbox, 1  # retourne le tuple: index de la case Dice54 , combinaison speciale trouve == 1

        return -1, 0  # retourne le tuple: index fictif , combinaison speciale non trouve == 0

    def compute_rule(self, boxnumber, previousbox):

        """

        Recherche de cases speciales

        """

        # return tuple type/box/nextturn

        box = self._boxList[boxnumber]

        if box._boxType == "Goose":

            return 1, boxnumber + self.sumofdices(), 1

        elif box._boxType == "Bridge":

            foundbox = self.search_box(boxnumber + 1, self._nbBox, "Bridge")

            if foundbox != -1:
                return 1, foundbox, 1

            return boxnumber, 1



        elif box._boxType == "Hotel":

            return 1, boxnumber, 4



        elif box._boxType == "Jail":

            return 2, boxnumber, 0, previousbox, 1



        elif box._boxType == "Well":

            return 2, boxnumber, 0, boxnumber, 1



        elif box._boxType == "Labyrinth":

            return 1, boxnumber - 12, 1



        elif box._boxType == "Skull":

            return 1, 0, 1

        return 0, boxnumber, 1

    def compute_lastbox(self, boxnumber):

        """

        Gérer fin du plateau pour qu'un dé trop grand revienne en arrière

        """

        if boxnumber > self._nbBox:
            boxnumber = self._nbBox - (boxnumber - self._nbBox)

        return boxnumber

    def test_If_Win(self, boxnumber):

        """

        Tester case finale pour voir si victoire

        """

        return boxnumber == self._nbBox


class Box:
    """
    Définit une case par sa règle
    """
    def __init__(self, boxType):
        """
        Initialise en mettant la règle de la case
        """
        self._boxType = boxType

    def setType(self, boxType):
        """
        Affecter une règle
        """
        self._boxType = boxType

class Game:
    gameTurn = 0
    numberOfPlayer = 0
    playerWin = False
    nbBoxOnLine = 8

    def __init__(self):
        self.listOfPlayers = []
        self.nbDice = 2
        self.nbFace = 6
        self.nbBox = 63

    def Init(self):
        endRequest = False
        while not endRequest:
            request = ""
            while (request not in ("S", "M", "s", "m")):
                request = input("Quel type de partie ? Standard (S) ou Modifiée (M) :")
            if request in ("S", "s"):
                endRequest = True
            elif request in ("M", "m"):
                while not endRequest:
                    endRequestDice = False
                    while not endRequestDice:
                        _nbdice = input("Nombre de des (entre 2 et 5) :")
                        try:
                            val_nbdice = int(_nbdice)
                            if 2 <= val_nbdice <= 5:
                                self.nbDice = val_nbdice
                                endRequestDice = True
                            else:
                                print("Le nombre de des n'est pas valide !")
                        except ValueError:
                            print("La saisie n'est pas un nombre !")
                    endRequestFace = False
                    while not endRequestFace:
                        _nbface = input("Nombre de faces des des (entre 4 et 10) :")
                        try:
                            val_nbface = int(_nbface)
                            if 4 <= val_nbface <= 10:
                                self.nbFace = val_nbface
                                endRequestFace = True
                            else:
                                print("Le nombre de face des des n'est pas valide !")
                        except ValueError:
                            print("La saisie n'est pas un nombre !")
                    endRequest = True
        self.gooseTray = Tray(self.nbDice, self.nbFace, self.nbBox)  # 2 dés, 6 face, 63 cases par defaut
        self.gooseTray.Set_GameByDefault()
        print("\n Début de partieeeeeeeeee ! \n")

    def NewGameTurn(self):
        self.gameTurn += 1
        print("\n**********")
        print("* tour", self.gameTurn, "*")
        print("**********")
        return self.gameTurn

    def Set_NbBoxOnLineOfGrid(self, _nbBoxOnLine):
        self.nbBoxOnLine = _nbBoxOnLine

    def set_Players(self, playerClass):
        self.numberOfPlayer += 1
        self.listOfPlayers.append(playerClass)

    def Get_NumberPlayers(self):
        return self.numberOfPlayer

    def Get_PlayerName(self):
        return self.listOfPlayers[self.actualPlayerIndex]._name

    def Get_Box(self):
        self.listOfPlayers[self.actualPlayerIndex].get_actualbox()

    def Get_WaitTime(self):
        return self.listOfPlayers[self.actualPlayerIndex].get_waitingturn()

    def Set_CurrentPlayer(self, numPlayer):
        self.actualPlayerIndex = numPlayer

    def Get_Color(self, _color):
        if _color == "Rouge":
            return "\033[30;41;1m"  # \033[0m"
        elif _color == "Vert":
            return "\033[30;42;1m"  # \033[0m"
        elif _color == "Jaune":
            return "\033[30;43;1m"  # \033[0m"
        elif _color == "Bleu":
            return "\033[30;44;1m"  # \033[0m"
        elif _color == "Magenta":
            return "\033[30;45;1m"  # \033[0m"
        elif _color == "Cyan":
            return "\033[30;46;1m"  # \033[0m"
        elif _color == "Noir":
            return "\033[30;40;1m"  # \033[0m"

    def Get_TextColor(self, _color):
        if _color == "Rouge":
            return "\033[31;49;1m"  # \033[0m"
        elif _color == "Vert":
            return "\033[32;49;1m"  # \033[0m"
        elif _color == "Jaune":
            return "\033[33;49;1m"  # \033[0m"
        elif _color == "Bleu":
            return "\033[34;49;1m"  # \033[0m"
        elif _color == "Magenta":
            return "\033[35;49;1m"  # \033[0m"
        elif _color == "Cyan":
            return "\033[36;40;1m"  # \033[0m"
        elif _color == "Noir":
            return "\033[30;40;1m"  # \033[0m"

    def Set_NormalColor(self):
        return "\033[0m"

    def ShowTray(self):
        self.printTray()

    def printTray(self):
        print(self.Set_NormalColor())
        caseWidth = 11
        lineType = "|"
        linePlayer = "|"
        lineNumber = "|"
        separator = "-"
        l = self.nbBoxOnLine
        for k in range(self.nbBoxOnLine):
            separator = separator + "------------"
        max = len(self.gooseTray._boxList) - 1
        for i in range(max, -1, -1):
            addType = " "
            box = self.gooseTray._boxList[i]
            if box._boxType != "None":
                addType = addType + box._boxType
            for h in range(caseWidth - len(addType)):
                addType = addType + " "
            lineType = lineType + addType + "|"
            # creation des joueurs
            addPlayer = " "
            nbPlayer = 0  # compte le nombre de joueur pour decrementer de 1 la largeur de case
            for player in self.listOfPlayers:
                if player.get_actualbox() == i:
                    addPlayer = addPlayer + self.Get_Color(player._color) + " \033[0m "
                    nbPlayer = nbPlayer + 2
            for h in range(caseWidth - nbPlayer - 2):
                addPlayer = addPlayer + " "
            linePlayer = linePlayer + addPlayer + " |"
            # creation du numero de case
            if i == 0:
                addNumber = "  Départ"
            elif i == max:
                addNumber = "    Fin"
            else:
                addNumber = "    " + str(i)
            for h in range(caseWidth - len(addNumber)):
                addNumber = addNumber + " "
            lineNumber = lineNumber + addNumber + "|"
            l = l - 1
            if l == 0 and i != 0:
                self.Set_NormalColor()
                print(separator)
                print(lineType)
                print(linePlayer)
                print(lineNumber)
                lineType = "|"
                linePlayer = "|"
                lineNumber = "|"
                l = self.nbBoxOnLine
        self.Set_NormalColor()
        print(separator)
        print(lineType)
        print(linePlayer)
        print(lineNumber)
        print(separator)

    def TestIfWin(self):
        if self.playerWin:
            print("*******", self.listOfPlayers[self.actualPlayerIndex]._name + " - " +
                  self.listOfPlayers[self.actualPlayerIndex]._color, " a gagné!!!! *******")
            return True
        else:
            return False
        return self.playerWin

    def Play(self):
        currentPlayer = self.listOfPlayers[self.actualPlayerIndex]
        print(self.Get_TextColor(currentPlayer._color))
        print("Tour du joueur : " + currentPlayer._name + " - " + currentPlayer._color)
        input(currentPlayer._name + " appuyez sur entrée pour lancer les dés!")
        if currentPlayer.test_waitingturn() == 1:  # test si le joueur ne doit pas passer son tour
            actualBox = currentPlayer.get_actualbox()  # récupère sa case actuelle
            self.gooseTray.throw()  # lancer les dés
            print("    lancer de dés:", self.gooseTray._diceresult[0], "+", self.gooseTray._diceresult[1], "=",
            self.gooseTray.sumofdices())  # affiche par ex 2+3 = 5
            currentPlayer.add_dice(self.gooseTray.sumofdices())  # on ajoute dés à case actuelle
            currentPlayer.set_actualbox(self.gooseTray.compute_lastbox(
                currentPlayer.get_actualbox()))  # on déplace le joeur sur new case & on vérifie qu'il ne dépasse pas la dernière case
            print("        Va sur la case:", currentPlayer.get_actualbox())
            # Teste victoire joueur ?
            if self.gooseTray.test_If_Win(currentPlayer.get_actualbox()) == 1:
                self.playerWin = True
            else:
                # Si pas victoire, renvoie résultat du test combinaison spéciale de dés
                resultDiceRules = self.gooseTray.compute_dice()
                # On regarde s'il a fait une combinaison spéciale de dés (par exemple doubles)
                if resultDiceRules[1] == 1:
                    print("        dé spécial:", resultDiceRules)
                    currentPlayer.set_actualbox(resultDiceRules[0])
                    print("        Va sur la case:", currentPlayer.get_actualbox())
                else:
                    if currentPlayer.get_waitingturn() == -1:
                        print("    pas de lancer - attente de délivrance")
                    else:
                        ruletest = 1
                        while ruletest > 0:
                            resultBoxRules = self.gooseTray.compute_rule(currentPlayer.get_actualbox(), actualBox)
                            ruletest = resultBoxRules[0] == 1 and resultBoxRules[1] != actualBox and resultBoxRules[
                                1] < self.gooseTray._nbBox
                            if resultBoxRules[0] != 0:
                                print("        case spéciale:", self.gooseTray.get_type(currentPlayer.get_actualbox()))
                            if resultBoxRules[0] == 1:  # case speciale concerne seulement le joueur
                                currentPlayer.set_actualbox(self.gooseTray.compute_lastbox(resultBoxRules[1]))
                                currentPlayer.set_waitingturn(resultBoxRules[2])
                                ruletest = currentPlayer.get_waitingturn() == 1
                                print("        Va sur la case:", currentPlayer.get_actualbox())
                            elif resultBoxRules[0] == 2:  # case speciale concerne aussi un autre joueur
                                currentPlayer.set_actualbox(resultBoxRules[1])
                                currentPlayer.freeze_waiting()
                                for k in range(self.numberOfPlayer):
                                    if k != j:  # il ne s'agit pas du joueur en cours
                                        player = self.listOfPlayers[k]
                                        if player.get_actualbox() == currentPlayer.get_actualbox():
                                            # il s'agit du joueur sur la meme case
                                            # on lui applique les regle de la case liberee
                                            player.set_actualbox(
                                                resultBoxRules[3])  # on affecte l'ancienne case du joueur actif
                                            print(
                                                "        Le joueur " + player._name + " - " + currentPlayer._color + " va sur la case: " + str(
                                                    resultBoxRules[2]))
                                            player.set_waitingturn(resultBoxRules[4])  # le joueur redemarre
                                            break
                if self.gooseTray.test_If_Win(currentPlayer.get_actualbox()) == 1:
                    self.playerWin = True
            # Set_NormalColor()
            self.Set_NormalColor()
        else:
            if currentPlayer.get_waitingturn() == -1:
                print("    pas de lancer - attente de délivrance")
            else:
                print("    pas de lancer - attente:", currentPlayer.get_waitingturn() - 1, "tours")
        print("        Termine le tour sur la case: ", currentPlayer.get_actualbox())

# ***************************MAIN*******************************

gameGoose = Game()
player = Player()
player.Set_Param("Player1", "Rouge")
gameGoose.set_Players(player)
player = Player()
player.Set_Param("Player2", "Bleu")
gameGoose.set_Players(player)
player = Player()
player.Set_Param("Player3", "Jaune")
gameGoose.set_Players(player)
player = Player()
player.Set_Param("Player4", "Vert")
gameGoose.set_Players(player)

gameGoose.Set_NbBoxOnLineOfGrid(8)
gameGoose.Init()
gameGoose.ShowTray()

endOfGame = False  # Booléen pour continuer la partie en fct de si elle est terminée (s'arrête à 1)
while endOfGame == False:
    num_coup = gameGoose.NewGameTurn()  # ***bdd***
    for j in range(gameGoose.Get_NumberPlayers()):
        gameGoose.Set_CurrentPlayer(j)  # affecte le joueur actuel (celui qui joue)
        pseudo_joueur = gameGoose.Get_PlayerName()  # ***bdd***
        gameGoose.Play()
        position = gameGoose.Get_Box()  # ***bdd***
        waitTime = gameGoose.Get_WaitTime()  # ***bdd***
        endOfGame = gameGoose.TestIfWin()
        if endOfGame == True:
            break
    gameGoose.ShowTray()