from jeuxservice.jeux.abstractgame import AbstractGame
from jeuxservice.plateau.oiegrid import Tray          
from jeuxservice.plateau.oiegrid import Dice
from jeuxservice.plateau.oiegrid import Box


class Game(AbstractGame):

    def __init__(self):  
        AbstractJeu.__init__(self)
        self.nbDice = 2
        self.nbFace = 6
        self.nbBox = 63
        self.gameTurn = 0
        self.numberOfPlayer = 0
        self.playerWin = False
        self.nbBoxOnLine = 8

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
            sumofdiceLabel = str(self.gooseTray._diceresult[0])
            for i in range(1, self.gooseTray.Get_numOfDice()):
                sumofdiceLabel += "+" + str(self.gooseTray._diceresult[i])
            print("    lancer de dés:", sumofdiceLabel, "=",
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

    def PlaySimul(self, playerName, numbox, waitingTime):
        for player in self.listOfPlayers:
            if player._name == playerName:
                player.set_waitingturn(waitingTime)  
                player.set_actualbox(numbox)  
                break