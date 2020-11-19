from jeuxservice.jeux.abstractjeux import AbstractJeu
from jeuxservice.plateau.oiegrid import Tray


class GameOie(AbstractJeu):
    def __init__(self, id_partie):
        AbstractJeu.__init__(self, id_partie)

    def initialisation(self):
        self.tray = Tray(numofdice=2, numoffaces=6, nbBox=63)  # nb lignes, nb colonnes, nb jetons alignés

    def set_Players(self, playerClass):
        self.listOfPlayers.append(playerClass)

    def initialisation(self):
        pass

    def jouer_un_coup(self):
        pass

