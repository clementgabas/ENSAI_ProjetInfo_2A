from abc import ABC

class AbstractJeu(ABC):

    def __init__(self, id_partie):
        self.listOfPlayers = []
        self.id_partie = id_partie
        self.numberOfPlayer = len(self.listOfPlayers)


    def set_Players(self, playerClass):
        self.listOfPlayers.append(playerClass)

    def initialisation(self):
        pass

    def jouer_un_coup(self):
        pass

    def create_resultat(self):
        return {"Statut": "", "Message": ""}

    def update_resultat(self, statut, message=""):
        Resultat = self.create_resultat()
        Resultat["Statut"] = statut
        Resultat["Message"] = message
        return Resultat
    