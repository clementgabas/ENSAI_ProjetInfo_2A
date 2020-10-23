#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 11:08:42 2020

@author: romanepares
"""

import random

class Player:
    _name = ""
    _color = ""
    _nbwaitingturn = 1
    _actualbox = 0
    _previousbox = 0

    def __init__(self, name, color):
        self._name = name
        self._color = color

    def set_waitingturn(self, nbwaitingturn):
        self._nbwaitingturn = nbwaitingturn

    def get_waitingturn(self):
        return self._nbwaitingturn

    def test_waitingturn(self):
        if self._nbwaitingturn > 1:
            self._nbwaitingturn = self._nbwaitingturn - 1
        return self._nbwaitingturn - 1 == 0

    def freeze_waiting(self):
        self._nbwaitingturn = -1

    def get_actualbox(self):
        return self._actualbox

    def set_actualbox(self, box):
        self._actualbox = box

    def add_dice(self, value):
        self._actualbox = self._actualbox + value

class Dice:
    _numofdice = 0
    _diceresult = []
    _numoffaces = 0

    def __init__(self, numofdice, numoffaces):
        self._numofdice = numofdice
        self._numoffaces = numoffaces
        for i in range(self._numofdice):
            self._diceresult.append(0)


    def throw(self):
        for i in range(self._numofdice):
            self._diceresult[i] = random.randint(1, self._numoffaces)

    def dicevalue(self, num):
        return self._diceresult[num]

    def sumofdices(self):
        s = 0
        for i in range(self._numofdice):
            s = s + self._diceresult[i]
        return s


class Tray(Dice):
    _nbBox = 1
    _boxList = []

    def __init__(self, numofdice, numoffaces, nbBox):
        self._nbBox = nbBox
        Dice.__init__(self, numofdice, numoffaces)
        for i in range(self._nbBox + 1):
            box = Box("None")
            self._boxList.append(box)

    def set_rules(self, boxnumber, boxtype):
        box = self._boxList[boxnumber]
        box.setType(boxtype)

    def get_type(self, boxnumber):
        box = self._boxList[boxnumber]
        return box._boxType

    def search_box(self, start, end, test):
        for i in range(start, end):
            # recherche le pont suivant
            if self.get_type(i) == test:
                return i
        return -1

    def compute_dice(self):
        dice1 = 0
        dice2 = 0
        for i in range(self._numofdice):
            if self._diceresult[i] == 6:
                dice1 = 1
            elif self._diceresult[i] == 3:
                dice2 = 1
        if dice1 == 1 and dice2 == 1:
            #on recherche la case Dice63
            foundbox = self.search_box(0, self._nbBox, "Dice63")
            if foundbox != -1:
                return foundbox, 1
        dice1 = 0
        dice2 = 0
        for i in range(self._numofdice):
            if self._diceresult[i] == 5:
                dice1 = 1
            elif self._diceresult[i] == 4:
                dice2 = 1
        if dice1 == 1 and dice2 == 1:
            # on recherche la case Dice54
            foundbox = self.search_box(0, self._nbBox, "Dice54")
            if foundbox != -1:
                return foundbox, 1
        return -1, 0

    def compute_rule(self, boxnumber, previousbox):
        #return tuple type/box/nextturn
        box = self._boxList[boxnumber]
        if box._boxType == "Goose":
            return 1, boxnumber + self.sumofdices(), 1
        elif box._boxType == "Bridge":
            foundbox = self.search_box(boxnumber + 1, self._nbBox, "Bridge")
            if foundbox != -1:
                return 1, foundbox, 1;
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
        if boxnumber > 63:
            boxnumber = 63 - (boxnumber - 63)
        return boxnumber

    def test_If_Win(self, boxnumber):
        return boxnumber == self._nbBox


class Box:

    def __init__(self, boxType):
        self._boxType = boxType

    def setType(self, boxType):
        self._boxType = boxType

#***MAIN********************************************************
gooseTray = Tray(2, 6, 63)
gooseTray.set_rules(6, "Bridge")
gooseTray.set_rules(9, "Goose")
gooseTray.set_rules(12, "Bridge")
gooseTray.set_rules(14, "Goose")
gooseTray.set_rules(18, "Goose")
gooseTray.set_rules(19, "Hotel")
gooseTray.set_rules(23, "Goose")
gooseTray.set_rules(26, "Dice63")
gooseTray.set_rules(27, "Goose")
gooseTray.set_rules(31, "Well")
gooseTray.set_rules(32, "Goose")
gooseTray.set_rules(36, "Goose")
gooseTray.set_rules(41, "Goose")
gooseTray.set_rules(42, "Labyrinth")
gooseTray.set_rules(45, "Goose")
gooseTray.set_rules(50, "Goose")
gooseTray.set_rules(52, "Jail")
gooseTray.set_rules(53, "Dice54")
gooseTray.set_rules(54, "Goose")
gooseTray.set_rules(58, "Skull")
gooseTray.set_rules(59, "Goose")

listOfPlayers = []
numberOfPlayer = 4
player = Player("Player1", 21)
listOfPlayers.append(player)
player = Player("Player2", 20)
listOfPlayers.append(player)
player = Player("Player3", 20)
listOfPlayers.append(player)
player = Player("Player4", 20)
listOfPlayers.append(player)

gooseTray.throw()
endOfGame = 0
gameturn = 0
while endOfGame == 0:
    gameturn = gameturn + 1
    print("**********")
    print("* tour", gameturn, "*")
    print("**********")
    for j in range(numberOfPlayer):
        currentplayer = listOfPlayers[j]
        if currentplayer.test_waitingturn() == 1:
            actualBox = currentplayer.get_actualbox()
            gooseTray.throw()
            print("    lancer:", gooseTray._diceresult[0] , "+", gooseTray._diceresult[1], "=", gooseTray.sumofdices())
            #on affecte la nouvelle case
            currentplayer.add_dice(gooseTray.sumofdices())
            currentplayer.set_actualbox(gooseTray.compute_lastbox(currentplayer.get_actualbox()))
            if gooseTray.test_If_Win(currentplayer.get_actualbox()) == 1:
                print("                                    *", currentplayer._name, " a gagné")
                endOfGame = 1
                break
            resultDiceRules= gooseTray.compute_dice()
            if resultDiceRules[1] == 1:
                print("        dé spécial:", resultDiceRules)
                currentplayer.set_actualbox(resultDiceRules[0])
            else:
                ruletest = 1
                while ruletest > 0:
                    resultBoxRules = gooseTray.compute_rule(currentplayer.get_actualbox(), actualBox)
                    ruletest = resultBoxRules[0] == 1 and resultBoxRules[1] != actualBox and resultBoxRules[1] < gooseTray._nbBox
                    if resultBoxRules[0] != 0:
                        print("        case spéciale:", gooseTray.get_type(currentplayer.get_actualbox()))
                    if resultBoxRules[0] == 1:#case speciale concerne seulement le joueur
                        currentplayer.set_actualbox(gooseTray.compute_lastbox(resultBoxRules[1]))
                        currentplayer.set_waitingturn(resultBoxRules[2])
                        ruletest = currentplayer.get_waitingturn() == 1
                    elif resultBoxRules[0] == 2:#case speciale concerne aussi un autre joueur
                        currentplayer.set_actualbox(resultBoxRules[1])
                        currentplayer.freeze_waiting()
                        for k in range(numberOfPlayer):
                            if k != j:#il ne s'agit pas du joueur en cours
                                player = listOfPlayers[k]
                                if player.get_actualbox() == currentplayer.get_actualbox():
                                    #il s'agit du joueur sur la meme case
                                    #on lui applique les regle de la case liberee
                                    player.set_actualbox(resultBoxRules[2])#on affecte l'ancienne case du joueur actif
                                    if resultBoxRules[3] == 0:
                                        player.set_waitingturn(resultBoxRules[4])#le joueur redemarre
                                        player.set_actualbox(resultBoxRules[3])
                                        break
            if gooseTray.test_If_Win(currentplayer.get_actualbox()) == 1:
                print("                                    *", currentplayer._name, " a gagné")
                endOfGame = 1
                break
        else:
            print("    pas de lancer - attente:", currentplayer.get_waitingturn(), "tours")
        print("                                    *", currentplayer._name, ":", currentplayer.get_actualbox())
