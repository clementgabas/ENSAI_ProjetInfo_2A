from jeuxservice.player.abstractplayer import AbstractPlayer

class Player(AbstractPlayer):

    def __init__(self, name, color, ordre):
        AbstractPlayer.__init__(name, color, ordre)
        self._token = 0

    def Set_Param(self, name, color):
        self._name = name
        self._color = color
        if self._color == "Jaune":
            self._token = 1
        elif self._color == "Rouge":
            self._token = 2

    def Get_Token(self):
        return self._token