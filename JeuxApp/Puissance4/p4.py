#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 09:12:37 2020

@author: romanepares
"""

class Player:
    _name = ""
    _color = ""
    _token = 0

    def __init__(self, name, color):
        self._name = name
        self._color = color
        if self._color == "Jaune": #Croix A MODIFIER
            self._token = 1
        elif self._color == "Rouge": #Rond A MODIFIER
            self._token = 2


    def Get_Token(self):
        return self._token



class Grid:
    _gridList = []
    _win = 0
    #RedToken = 1
    #YellowToken = 2

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
                        result[2] = result[2] + 1 # on increment le nombre de jetons alignes
                    else:
                        continueTest[4] = 0  # interruption de couleur - on arrete de chercher a gauche en bas
            
            if x + i < self._numHeight and y + i < self._numHeight:  # pas de debordement hors de la grille a droite et en haut
                if continueTest[5] == 1:  # on continue car pas d'interruption de couleur par le haut
                    if self._gridList[x + i][y + i] == tokenColor:  # le jeton est de la bonne couleur
                        result[2] = result[2] + 1 # on increment le nombre de jetons alignes
                    else:
                        continueTest[5] = 0  # interruption de couleur - on arrete de chercher a droite en haut
            
            #test diagonale descendante - on scrute vers le haut a gauche et le bas a droite
            if x - i >= 0 and y + i < self._numHeight:  # pas de debordement hors de la grille a gauche et en haut
                if continueTest[6] == 1:  # on continue car pas d'interruption de couleur par le bas a gauche
                    if self._gridList[x - i][y + i] == tokenColor:  # le jeton est de la bonne couleur
                        result[3] = result[3] + 1 # on increment le nombre de jetons alignes
                    else:
                        continueTest[6] = 0  # interruption de couleur - on arrete de chercher en haut a gauche
            
            if x + i < self._numHeight and y - i >= 0:  # pas de debordement hors de la grille a droite et en bas
                if continueTest[7] == 1:  # on continue car pas d'interruption de couleur par le haut a droite
                    if self._gridList[x + i][y - i] == tokenColor:  # le jeton est de la bonne couleur
                        result[3] = result[3] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[7] = 0  # interruption de couleur - on arrete de chercher en bas a gauche
            
            if self._sum(continueTest) == 0: #  il n'y a plus de jeton de couleur alignes
                break
            
            for j in result:
                if j == self._tokenWinNumber:  # le nombre de jetons alignes est le bon
                    self._win = 1
                    break


    def TestIfWin(self):
        return self._win


    def TestEndOfGame(self):
        result = 1
        for i in range(self._numWidth):
            result = result and self._gridList[i][self._numHeight - 1] == 0
        return result


    def ClearGrid(self):
        self._win = 0
        for k in range(self._numWidth):
            for l in range(self._numHeight):
                self._gridList[k][l] = 0


    def getGrid(self):
        return self._gridList


    def _sum(self, arr):
        sum=0
        for i in arr:
            sum = sum + i
        return sum



def printGrid(_grid, nbline, nbcol):
    line = "|"
    separator = "-"
    for k in range(nbcol):
        separator = separator + "----"
    print(separator)
    for i in range(nbline - 1, -1, -1):
        for j in range(nbcol):
            if _grid[j][i] == 0:
                line = line + "   |"
            elif _grid[j][i] == 1:
                line = line + " X |"
            elif _grid[j][i] == 2:
                line = line + " O |"
        print(line)
        line = "|"
    print(separator)
    
    

# Param par défaut
nbcolumn = 10 #peut etre defini par input
nbline = 10 #peut etre defini par input
power4Grid = Grid(nbline, nbcolumn, 4) # nb lignes, nb colonnes, nb jetons alignés
listOfPlayers = []
numberOfPlayer = 2 # deux joueurs
player = Player("Player1", "Jaune") # écrit couleur dans classe A MODIFIER
listOfPlayers.append(player)
player = Player("Player2", "Rouge") # écrit couleur dans classe A MODIFIER
listOfPlayers.append(player)


endOfGame = False  # Booléen pour continuer la partie en fct de si elle est terminée (s'arrête à 1)
gameturn = 0  # indique le tour de jeu


while endOfGame == False:
    gameturn = gameturn + 1  # incrémente le tour
    print("\n**********")
    print("* tour", gameturn, "*")
    print("**********")

    for j in range(numberOfPlayer):
        currentplayer = listOfPlayers[j]  # récupère le joueur actuel (celui qui joue)
        test_input = False
        
        while test_input == False:
            column_input = input(currentplayer._name + " choisissez une colonne pour votre jeton :")
            try:
                val_column_input = int(column_input)
                test_input = True
            except ValueError:
                print("Le numero de colonne n'est pas valide !")
        power4Grid.Throw(val_column_input, currentplayer.Get_Token())
        printGrid(power4Grid.getGrid(), nbline, nbcolumn)
        
        if power4Grid.TestIfWin():
            endOfGame = True
            break
print(currentplayer._name + " gagne la partie !")




