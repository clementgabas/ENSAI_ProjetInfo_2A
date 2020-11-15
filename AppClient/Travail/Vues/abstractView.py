# Importation des modules
from abc import ABC
from printFunctions import timePrint as print

#Création de la classe AbstractView

class AbstractView(ABC):
    #@abstractmethod
    def display_info(self):
        pass
    def make_choice(self):
        pass

    def print_message(self, Resultat):
        if Resultat["Message"]:
            print(Resultat["Message"])

