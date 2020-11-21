from abc import ABC

class AbstractGrid(ABC):

    def __init__(self):
        pass

    def TestIfWin(self):
        pass

    def create_resultat(self):
        return {"Statut": "", "Message": ""}

    def update_resultat(self, statut, message=""):
        Resultat = self.create_resultat()
        Resultat["Statut"] = statut
        Resultat["Message"] = message
        return Resultat
