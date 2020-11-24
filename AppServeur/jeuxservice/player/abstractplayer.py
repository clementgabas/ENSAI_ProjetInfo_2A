from abc import ABC

class AbstractPlayer(ABC):
    """
    Classe abstraite de laquelle vont hériter plusieurs classes
    """

    def __init__(self, name, color, ordre):
        """
        Fonction init qui définie:
            name : str
                Le pseudo de l'utilisateur
            color : str
                couleur de l'utilisateur
            ordre : float
                ordre de passage
        """
        self._name = name
        self._color = color
        self._ordre = ordre


    def get_ordre(self):
        """
        Fonction qui retourne l'ordre de passage du joueur.

        Returns
        ------
        _order : float
            ordre de passage

        """
        return self._ordre