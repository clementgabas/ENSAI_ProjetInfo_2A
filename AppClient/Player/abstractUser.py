from abc import ABC


class AbstractUser(ABC):
    """
       Classe abstraite de laquelle vont hériter plusieurs classes
    """

    def create_resultat(self):
        """
        Procédure qui permet de crée un dictionnaire composé d'un statut et d'un message associée a ce statut.
        """
        return {"Statut": "", "Message": ""}

    def update_resultat(self, statut, message=""):
        """
        Fontion qui permet de mettre a jour un dictionnaire, en modifiant le statut et le message associé

        :param
        -----
        statut: str
            statut de la réponse
        message: str
            message associé, ce paramètre étant optionnel, si rien n'est rentré, on le suppose vide

        :return
        ------
        Resultat : dict
            Dictionnaire mis à jour
        """
        Resultat = self.create_resultat()
        Resultat["Statut"] = statut
        Resultat["Message"] = message
        return Resultat