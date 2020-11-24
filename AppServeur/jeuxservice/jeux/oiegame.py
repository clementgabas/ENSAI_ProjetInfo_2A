from jeuxservice.jeux.abstractjeux import AbstractJeu
from jeuxservice.plateau.oiegrid import Tray


class GameOie(AbstractJeu):
    """
    Classe qui hérite de la classe AbstractJeu et qui définit la partie de jeu de l'oie.

    """
    def __init__(self, id_partie):
        AbstractJeu.__init__(self, id_partie)

    def initialisation(self):
        """
        Méthode qui initialise la grille de Jeu de l'oie en prenant, le nombre de dés, le nombre de faces sur ces dés et
        le nobre de case sur le jeu de l'oie
        """
        self.tray = Tray(numofdice=2, numoffaces=6, nbBox=63)  # nb dé, nb face, nb case

    def set_Players(self, playerClass):
        """
        Procédure qui ajoute un joueur à la liste des membre de la partie.
        
        Parameters
        ------
        playerClass : objet de la classe playerClass
            information sur le joueur a ajouter.
        """
        self.listOfPlayers.append(playerClass)

#    def initialisation(self):
#       pass

    def jouer_un_coup(self): # a supp
        pass

