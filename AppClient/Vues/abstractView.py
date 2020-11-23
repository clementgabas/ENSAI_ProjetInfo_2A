# Importation des modules
from abc import ABC
from Vues.usefulfonctions.printFunctions import timePrint as print

#Création de la classe AbstractView

class AbstractView(ABC):

    def display_info(self):
        pass
    def make_choice(self):
        pass

    def print_message(self, Resultat):
        if Resultat["Message"]:
            print(Resultat["Message"])

