from abc import ABC

class AbstractGame(ABC):

    def __init__(self, id_partie):
        self.listOfPlayers = []


    def set_Players(self, playerClass):
        self.listOfPlayers.append(playerClass)

    def initialisation(self):
        pass
