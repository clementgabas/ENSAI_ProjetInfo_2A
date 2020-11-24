from jeuxservice.player.abstractplayer import AbstractPlayer

class PlayerP4(AbstractPlayer):
    """
    Classe qui définit la partie joueur de puissance 4, cette classe hérite de la classe AbstractPlayer
    """
    def __init__(self, name, color, ordre):
        """
        Fonction init qui définit:
            name : str
                Le pseudo de l'utilisateur
            color : str
                couleur de l'utilisateur
            ordre : float
                ordre de passage
        et qui initialise :
            token : int
            le numéro du joueur à 0, ce numéro definira le joueur dans la gille du puissance 4
        """
        AbstractPlayer.__init__(name, color, ordre)
        self._token = 0

    def Set_Param(self, name, color):
        """
        Procédure qui attribue a un joueur un numéro qui est soit 1 soit 2 en fonction de la couleur du joueur

        Parameters
        ------
        name: str
            nom du joueur
        color: str
            couleur choisie par le joueur

        """
        self._name = name
        self._color = color
        if self._color == "Jaune":  # Croix A MODIFIER
            self._token = 1
        elif self._color == "Rouge":  # Rond A MODIFIER
            self._token = 2

    def Get_Token(self):
        """
        Fonction qui renvoie le numéro du joueur comme défini dans la fonction initiatrice

        Returns
        -------
        token : str
            numéro du joueur, ce numéro defini le joueur dans la gille du puissance 4
        """
        return self._token