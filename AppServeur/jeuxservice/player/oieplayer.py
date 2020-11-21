from jeuxservice.player.abstractplayer import AbstractPlayer

class PlayerOie(AbstractPlayer):

    def __init__(self, name, color, ordre):
        AbstractPlayer.__init__(self, name, color, ordre)
        self._nbwaitingturn = 1  # nb tours d'attente
        self._actualbox = 0  # case actuelle
        self._previousbox = 0  # case d'où l'on vient


    def __str__(self):
        return f"Joueur : {self._name} ; Couleur : {self._color} ; Ordre de jeu : {self._ordre} ; nbwaitingturn : {self._nbwaitingturn} ; actualbox : {self._actualbox} : previousbox : {self._previousbox}"

    def set_waitingturn(self, nbwaitingturn):
        """
        Modifier le nombre de tours d'attente
        """
        self._nbwaitingturn = nbwaitingturn

    def get_waitingturn(self):
        """
        Obtenir le nombre de tours d'attente
        """
        return self._nbwaitingturn

    def test_waitingturn(self):
        """
        Tester si le joueur doit encore attendre ou peut jouer
        Retourne True ou False
        Si >1, je le retranche de 1 et je teste pour voir si = à 0
        Valeur par défaut c'est 1
         """
        if self._nbwaitingturn > 1:
            self._nbwaitingturn = self._nbwaitingturn - 1
        return self._nbwaitingturn - 1 == 0

    def freeze_waiting(self):
        """
        Geler le joueur afin qu'il ne joue pas (quand ca devrait être son tour, mais qu'il doit passer son tour)
        """
        self._nbwaitingturn = -1

    def get_actualbox(self):
        """
        Obtenir la case où il se situe actuellement
        """
        return self._actualbox

    def set_actualbox(self, box):
        """
        Définir la case où il se situe
        """
        self._actualbox = box

    def set_previousbox(self, box):
        """
        Définir la case où il se situe
        """
        self._previousbox = box

    def add_dice(self, value):
        """
        Par rapport case actuelle, additionne valeur des dés
        """
        self._actualbox = self._actualbox + value