#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 09:12:37 2020

@author: romanepares
"""

# -- gestion de l'affichage couleur dans le cmd.exe de Windows.
# -- Si vous utilisez ansicon.exe ou un terminal de commande prennant en charge les séquences ANSI, ce package n'est pas nécessaire.
#import colorama

#colorama.init()


class Player:
    _name = ""
    _color = ""
    _token = 0

    def Set_Param(self, name, color):
        self._name = name
        self._color = color
        if self._color == "Jaune":  # Croix A MODIFIER
            self._token = 1
        elif self._color == "Rouge":  # Rond A MODIFIER
            self._token = 2

    def Get_Token(self):
        return self._token


class Grid:
    _gridList = []
    _win = 0

    # RedToken = 1
    # YellowToken = 2

    def __init__(self, numHeight, numWidth, tokenWinNumber):
        self._numHeight = numHeight
        self._numWidth = numWidth
        self._tokenWinNumber = tokenWinNumber

        # init grid a 0
        for k in range(self._numWidth):
            self._gridList.append([0] * self._numHeight)

    def Throw(self, x, tokenColor):
        y = 0

        for i in range(self._numHeight):
            if self._gridList[x][i] == 0:
                self._gridList[x][i] = tokenColor
                y = i
                break
        result = [1, 1, 1, 1]
        continueTest = [1, 1, 1, 1, 1, 1, 1, 1]

        for i in range(1, self._tokenWinNumber):
            # test horizontal - on scrute la couleur des jetons a gauche puis a droite
            if x - i >= 0:  # pas de debordement hors de la grille a gauche
                if continueTest[0] == 1:  # on continue car pas d'interruption de couleur a gauche
                    if self._gridList[x - i][y] == tokenColor:  # le jeton est de la bonne couleur
                        result[0] = result[0] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[0] = 0  # interruption de couleur - on arrete de chercher a gauche

            if x + i < self._numWidth:  # pas de debordement hors de la grille a droite
                if continueTest[1] == 1:  # on continue car pas d'interruption de couleur a droite
                    if self._gridList[x + i][y] == tokenColor:  # le jeton est de la bonne couleur
                        result[0] = result[0] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[1] = 0  # interruption de couleur - on arrete de chercher a droite

            # test vertical - on scrute la couleur des jetons en bas puis en haut
            if y - i >= 0:  # pas de debordement hors de la grille en bas
                if continueTest[2] == 1:  # on continue car pas d'interruption de couleur par le bas
                    if self._gridList[x][y - i] == tokenColor:  # le jeton est de la bonne couleur
                        result[1] = result[1] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[2] = 0  # interruption de couleur - on arrete de chercher en bas

            if y + i < self._numHeight:  # pas de debordement hors de la grille en haut
                if continueTest[3] == 1:  # on continue car pas d'interruption de couleur par le haut
                    if self._gridList[x][y + i] == tokenColor:  # le jeton est de la bonne couleur
                        result[1] = result[1] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[3] = 0  # interruption de couleur - on arrete de chercher a droite

            # test diagonal montante - on scrute vers le bas a gauche et le haut a droite
            if x - i >= 0 and y - i >= 0:  # pas de debordement hors de la grille a gauche et en bas
                if continueTest[4] == 1:  # on continue car pas d'interruption de couleur par le bas
                    if self._gridList[x - i][y - i] == tokenColor:  # le jeton est de la bonne couleur
                        result[2] = result[2] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[4] = 0  # interruption de couleur - on arrete de chercher a gauche en bas

            if x + i < self._numHeight and y + i < self._numHeight:  # pas de debordement hors de la grille a droite et en haut
                if continueTest[5] == 1:  # on continue car pas d'interruption de couleur par le haut
                    if self._gridList[x + i][y + i] == tokenColor:  # le jeton est de la bonne couleur
                        result[2] = result[2] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[5] = 0  # interruption de couleur - on arrete de chercher a droite en haut

            # test diagonale descendante - on scrute vers le haut a gauche et le bas a droite
            if x - i >= 0 and y + i < self._numHeight:  # pas de debordement hors de la grille a gauche et en haut
                if continueTest[6] == 1:  # on continue car pas d'interruption de couleur par le bas a gauche
                    if self._gridList[x - i][y + i] == tokenColor:  # le jeton est de la bonne couleur
                        result[3] = result[3] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[6] = 0  # interruption de couleur - on arrete de chercher en haut a gauche

            if x + i < self._numHeight and y - i >= 0:  # pas de debordement hors de la grille a droite et en bas
                if continueTest[7] == 1:  # on continue car pas d'interruption de couleur par le haut a droite
                    if self._gridList[x + i][y - i] == tokenColor:  # le jeton est de la bonne couleur
                        result[3] = result[3] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[7] = 0  # interruption de couleur - on arrete de chercher en bas a gauche

            if self._sum(continueTest) == 0:  # il n'y a plus de jeton de couleur alignes
                break

            for j in result:
                if j == self._tokenWinNumber:  # le nombre de jetons alignes est le bon
                    self._win = 1
                    break

    def TestIfWin(self):
        return self._win

    def TestEndOfGame(self):
        result = True
        for i in range(self._numWidth):
            result = result and self._gridList[i][self._numHeight - 1] != 0
        return result

    def TestEndColumn(self, column):
        return self._gridList[column][self._numHeight - 1] != 0

    def ClearGrid(self):
        self._win = 0
        for k in range(self._numWidth):
            for l in range(self._numHeight):
                self._gridList[k][l] = 0

    def getGrid(self):
        return self._gridList

    def _sum(self, arr):
        sum = 0
        for i in arr:
            sum = sum + i
        return sum


class Game:
    gameTurn = 0
    numberOfPlayer = 2
    actualPlayerIndex = 0
    val_column_input = -1
    def __init__(self):
        self.listOfPlayers = []
        self.nbcolumn = 10
        self.nbline = 10
        self.nbToken = 4

    def printGrid(self):
        line = "|"
        separator = "-"
        abscisse = " "

        for k in range(self.nbcolumn):
            separator = separator + "----"

            if k == 0:
                abscisse = 2 * abscisse + str(k) + "   "

            elif k >= 10:
                abscisse = abscisse + str(k) + "  "

            else:
                abscisse = abscisse + str(k) + "   "

        print(separator)
        for i in range(self.nbline - 1, -1, -1):
            for j in range(self.nbcolumn):

                if self.power4Grid._gridList[j][i] == 0:
                    line = line + "   |"

                elif self.power4Grid._gridList[j][i] == 1:
                    line = line + " X |"

                elif self.power4Grid._gridList[j][i] == 2:
                    line = line + " O |"

            print(line)
            print(separator)
            line = "|"
        print(abscisse)

    def Init(self):
        endRequest = False

        while not endRequest:
            request = input("Quel type de partie ? Standard (S) ou Modifiée (M) :")

            while (request not in ("S", "M", "s", "m")):
                request = input("Quel type de partie ? Standard (S) ou Modifiée (M) :")

            if request in ("S", "s"):
                endRequest = True

            elif request in ("M", "m"):
                while not endRequest:
                    endRequestCol = False
                    while not endRequestCol:
                        _nbcol = input("Nombre de colonnes (entre 5 et 20) :")

                        try:
                            val_nbcol = int(_nbcol)
                            if 5 <= val_nbcol <= 20:
                                self.nbcolumn = val_nbcol
                                endRequestCol = True
                            else:
                                print("Le nombre de colonnes n'est pas valide !")

                        except ValueError:
                            print("La saisie n'est pas un nombre !")

                    endRequestLine = False

                    while not endRequestLine:
                        _nbLine = input("Nombre de lignes (entre 5 et 20) :")

                        try:
                            val_nbLine = int(_nbLine)
                            if 5 <= val_nbLine <= 20:
                                self.nbline = val_nbLine
                                endRequestLine = True
                            else:
                                print("Le nombre de lignes n'est pas valide !")

                        except ValueError:
                            print("La saisie n'est pas un nombre !")

                    endRequestToken = False

                    while not endRequestToken:
                        _nbToken = input("Nombre de jetons (entre 3 et 10) :")

                        try:
                            val_nbToken = int(_nbToken)
                            if 3 <= val_nbToken <= 10:
                                self.nbToken = val_nbToken
                                endRequestToken = True
                            else:
                                print("Le nombre de jetons n'est pas valide !")

                        except ValueError:
                            print("La saisie n'est pas un nombre !")

                    endRequest = True

        self.power4Grid = Grid(self.nbline, self.nbcolumn, self.nbToken)  # nb lignes, nb colonnes, nb jetons alignés

    def set_Players(self, playerClass):
        self.listOfPlayers.append(playerClass)

    def NewGameTurn(self):
        self.gameTurn += 1
        print("\n**********")
        print("* tour", self.gameTurn, "*")
        print("**********")
        return self.gameTurn

    def Get_NumberPlayers(self):
        return self.numberOfPlayer

    def Set_CurrentPlayer(self, numPlayer):
        self.actualPlayerIndex = numPlayer

    def Get_PlayerName(self):
        return self.listOfPlayers[self.actualPlayerIndex]._name

    def Get_NumberOfColumns(self):
        return self.nbcolumn

    def Get_ColumnNumber(self):
        return self.val_column_input

    def TestEndOfColumn(self, numColumn):
        return self.power4Grid.TestEndColumn(numColumn)

    def TestIfWin(self):
        if self.power4Grid.TestIfWin():
            print(self.listOfPlayers[self.actualPlayerIndex]._name + " gagne la partie!")
            return True
        else:
            return False

    def TestEndOfGame(self):
        if self.power4Grid.TestEndOfGame():
            print("Personne ne gagne")
            return True
        else:
            return False

    def Play(self):
            test_input = False

            while test_input == False:
                column_input = input(
                    self.listOfPlayers[self.actualPlayerIndex]._name + " choisissez une colonne pour votre jeton (allant de 0 à " + str(
                        self.nbcolumn - 1) + "):")
                try:
                    val_column_input = int(column_input)
                    if 0 <= val_column_input <= (self.nbcolumn - 1):
                        if self.power4Grid.TestEndColumn(val_column_input):
                            print("La colonne est pleine!")
                        else:
                            test_input = True

                except ValueError:
                    print("Le numero de colonne n'est pas valide !")
            self.power4Grid.Throw(val_column_input, self.listOfPlayers[self.actualPlayerIndex].Get_Token())
            self.printGrid()



# main

import os
import sys

sys.path.insert(1, '/Classes')

#from Game import *

#from game import Game


#main
gameP4 = Game()
gameP4.Init()
player1 = Player()
player1.Set_Param("Player1", "Jaune")
gameP4.set_Players(player1)

player2 = Player()
player2.Set_Param("Player2", "Rouge")
gameP4.set_Players(player2)

gameP4.Set_CurrentPlayer(0)
print(gameP4.Get_PlayerName())
gameP4.Set_CurrentPlayer(1)
print(gameP4.Get_PlayerName())

endOfGame = False  # Booléen pour continuer la partie en fct de si elle est terminée (s'arrête à 1)
print("\n Début de partieeeeeeeeee ! \n")
gameP4.printGrid()

while endOfGame == False:
    num_coup = gameP4.NewGameTurn()#***bdd***
    for j in range(gameP4.Get_NumberPlayers()):
        gameP4.Set_CurrentPlayer(j)  # affecte le joueur actuel (celui qui joue)
        pseudo_joueur = gameP4.Get_PlayerName()#***bdd***
        gameP4.Play()
        position = gameP4.Get_ColumnNumber()#***bdd***
        endOfGame = gameP4.TestIfWin()
        endOfGame |= gameP4.TestEndOfGame()
        if endOfGame == True:
            break