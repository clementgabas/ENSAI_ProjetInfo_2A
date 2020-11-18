from abc import ABC   
import DAO.gestionParticipation as DAOparticipation

class AbstractPlay(ABC):

    def __init__(self, id_partie):
        self.id_partie = id_partie  
        self.playerList = DAOparticipation.get_all_players(self.id_partie) 
        self.colorList = DAOparticipation.get_liste_couleur(self.id_partie)

    def Start(self):
        pass

    def simulate(self):
        pass