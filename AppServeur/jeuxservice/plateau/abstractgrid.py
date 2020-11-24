from abc import ABC

class AbstractGrid(ABC):
    """
    Classe abstraite qui définit le plateau d'un jeu
    """
    def __init__(self):
        """Méthode init"""
        pass

    def TestIfWin(self):
        """Méthode abstraite qui vérifie si il y a victoire."""
        pass

    def create_resultat(self):
        """
        Méthode qui permet de créer un dictionnaire composé d'un statut et d'un message associée a ce statut.
        """
        return {"Statut": "", "Message": ""}

    def update_resultat(self, statut, message=""):
        """
        Fontion qui permet de mettre a jour un dictionnaire, en modifiant le statut et le message associé

        Parameters
        -----
        statut: bool
            statut de la réponse
        message: str
            message associé, ce paramètre étant optionnel, si rien n'est rentré, on le suppose vide

        Returns
        ------
        Resultat : dict
            Dictionnaire mis à jour
        """
        Resultat = self.create_resultat()
        Resultat["Statut"] = statut
        Resultat["Message"] = message
        return Resultat
