from abc import ABC


class AbstractUser(ABC):

    def create_resultat(self):
        return {"Statut": "", "Message": ""}

    def update_resultat(self, statut, message=""):
        Resultat = self.create_resultat()
        Resultat["Statut"] = statut
        Resultat["Message"] = message
        return Resultat