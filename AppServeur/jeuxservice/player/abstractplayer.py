from abc import ABC

class AbstractPlayer(ABC):

    def __init__(self, name, color, ordre):
        self._name = name
        self._color = color
        self._ordre = ordre


    def get_ordre(self):
        return self._ordre