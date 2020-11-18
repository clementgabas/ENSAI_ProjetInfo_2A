from jeuxservice.jeux.abstractgame import AbstractGame
from jeuxservice.plateau.p4grid import Grid


class Game(Abstractgame):

    def __init__(self):  
        AbstractJeu.__init__(self)
        self.nbcolumn = 10
        self.nbline = 10
        self.nbToken = 4
        self.gameTurn = 0              
        self.numberOfPlayer = 0
        self.actualPlayerIndex = 0
        self.val_column_input = -1

    def printGrid(self):
        line = "|"
        separator = "-"
        abscisse = " "

        for k in range(self.nbcolumn):
            separator = separator + "-----"

            if k == 0:
                abscisse = 2 * abscisse + str(k) + "    "

            elif k >= 10:
                abscisse = abscisse + str(k) + "   "

            else:
                abscisse = abscisse + str(k) + "    "

        print(separator)
        for i in range(self.nbline - 1, -1, -1):
            for j in range(self.nbcolumn):

                if self.power4Grid._gridList[j][i] == 0:
                    line = line + "    |"

                elif self.power4Grid._gridList[j][i] == 1:
                    line = line + " \033[30;43;1m  \033[0m |"

                elif self.power4Grid._gridList[j][i] == 2:
                    line = line + " \033[30;41;1m  \033[0m |"

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
                endRequestCol = False
                while not endRequest:
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
        self.numberOfPlayer += 1
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
        if not self.power4Grid.TestIfWin() and self.power4Grid.TestEndOfGame():
            print("Personne ne gagne")
            return True
        else:
            return False

    def Play(self):
        test_input = False

        while test_input == False:
            column_input = input(
                self.listOfPlayers[
                    self.actualPlayerIndex]._name + " choisissez une colonne pour votre jeton (allant de 0 à " + str(
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

    def PlaySimul(self, column, playerName):
        for player in self.listOfPlayers:
            if player._name == playerName:
                if player._color == "Jaune":
                    self.power4Grid.Throw(column, 1)    
                elif player._color == "Rouge":
                    self.power4Grid.Throw(column, 2)  
        