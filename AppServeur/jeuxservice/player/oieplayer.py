from jeuxservice.player.abstractplayer import AbstractPlayer

class PlayerOie(AbstractPlayer):
    """
    Classe qui définie la partie joueur d'un jeu de l'oie, cette classe hérite de la classe AbstractPlayer
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
        et qui initialise :
            nbwaitingturn : int
                le nombre de tours d'attente a 1
            actualbox : int
                la position actuelle a 0
            previousbox
                la position précédente a 0
        """
        AbstractPlayer.__init__(self, name, color, ordre)
        self._nbwaitingturn = 1  # nb tours d'attente
        self._actualbox = 0  # case actuelle
        self._previousbox = 0  # case d'où l'on vient


    def __str__(self):
        return f"Le joueur {self._name}, de couleur {self._color}, jouant en {self._ordre +1} position, se situais précédemment sur la case {self._previousbox} et est maitenant sur la case {self._actualbox}. Il a {self._nbwaitingturn} tours d'attente"

    def get_dico(self):
        """
        Fontion qui gère la demande d'affichage des informations sur l'utilisateur.

        Returns
        -----
        type : dict
            Dictionnaire contenant nom, couleur, ordre de jeu, nombre de tour d'attente, position actuelle et position précédente deu joueur.
        """
        return {'Joueur' : self._name, 'Couleur' : self._color, 'Ordre_de_jeu' : self._ordre, 'nbwaitingturn' : self._nbwaitingturn, 'actualbox' : self._actualbox, 'previousbox' : self._previousbox}

    def set_waitingturn(self, nbwaitingturn):
        """
        Procédure qui gere la modification du nombre de tours d'attentes.

        Parameters
        -----
        nbwaitingturn : int
            nouvelle valeur du nombre de tours d'attente.
        """
        self._nbwaitingturn = nbwaitingturn

    def get_waitingturn(self):
        """
        Fonction qui permet d'afficher le nombre de tours d'attentes d'un utilisateur

        Returns
        ------
        nbwaitingturn :int
            Nombre de tours d'attentes.
        """
        return self._nbwaitingturn

    def test_waitingturn(self):
        """
        Fonction teste le nombre de tours d'attentes d'un utilisateur.

        Returns
        -------
        type : bool
            Si le joueur peut jouer au prochain tour, le booleen sera True.

            Sinon il sara False
        """
        if self._nbwaitingturn > 1:
            self._nbwaitingturn = self._nbwaitingturn - 1
        return self._nbwaitingturn - 1 == 0

    def freeze_waiting(self):
        """
        Fonction qui gere l'impossibilité de joueur du joueur. Cela permet de geler le joueur afin qu'il ne joue pas
        quand ça devrait être son tour, mais qu'il doit passer son tour.
        """
        self._nbwaitingturn = -1

    def get_actualbox(self):
        """
        Fonction qui permet d'afficher la postition actuelle d'un utilisateur

        Returns
        ------
        actualbox :int
             Postition actuelle de l'utilisateur.
        """
        return self._actualbox

    def set_actualbox(self, box):
        """
        Procédure qui gere la modification de la nouvelle position du joueur.

        Parameters
        -----
        box : int
            nouvelle valeur de la position du joueur.
        """
        self._actualbox = box

    def set_previousbox(self, box):
        """
        Procédure qui gere la modification de l'oncienne position du joueur.

        Parameters
        -----
        box : int
            nouvelle valeur de la position du joueur.
        """
        self._previousbox = box

    def add_dice(self, value):
        """
        Procédure qui gere la modification de la nouvelle position du joueur en ajoutant la some des dés.

        Parameters
        -----
        value : int
            valeur du dé
        """
        self._actualbox = self._actualbox + value