from abc import ABC

class AbstractJeux(ABC):

    def __init__(self):
        self.listOfPlayers = []


    def set_Players(self, playerClass):
        self.listOfPlayers.append(playerClass)

    def init(self):
        pass

    def jouer_un_coup(self):
        pass

    def printGrid(self, gridClass):
        pass
    