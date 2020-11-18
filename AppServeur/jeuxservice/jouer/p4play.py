from jeuxservice.jouer.abstractplay import AbstractPlay
from jeuxservice.jeux.p4game import Game     
import DAO.gestionCoups as DAOcoups
import DAO.gestionParticipation as DAOparticipation


class Play(AbstractJeu):

    def __init__(self, id_partie):  
        AbstractJeu.__init__(self, id_partie) 
        self.gameP4 = Game()

    def Start(self):  
        self.gameP4.Init()
        player = Player()
        player.Set_Param(self.playerList[0], self.colorList[0])
        self.gameP4.set_Players(player)
        player = Player()
        player.Set_Param(self.playerList[1], self.colorList[1])
        self.gameP4.set_Players(player)

        endOfGame = False  # Booléen pour continuer la partie en fct de si elle est terminée (s'arrête à 1)
        print("\n Début de partieeeeeeeeee ! \n")
        self.gameP4.printGrid()
        while endOfGame == False:
            num_coup = self.gameP4.NewGameTurn()  # ***bdd***
            for j in range(self.gameP4.Get_NumberPlayers()):
                self.gameP4.Set_CurrentPlayer(j)  # affecte le joueur actuel (celui qui joue)
                pseudo_joueur = self.gameP4.Get_PlayerName()  # ***bdd***
                self.gameP4.Play()
                position = self.gameP4.Get_ColumnNumber()  # ***bdd***
                endOfGame = self.gameP4.TestIfWin()
                endOfGame |= self.gameP4.TestEndOfGame() 
                DAOcoups.add_new_coup(self.id_partie, num_coup , pseudo_joueur, position, 1)
                if endOfGame == True:
                    break

    def simulate(self):
        liste_coups = DAOcoups.get_all_coups(self.id_partie)
        for coup in liste_coups:
            self.gameP4.NewGameTurn()
            nom_joueur = coup[2]
            colonne_jouee = coup[3]
            self.gameP4.PlaySimul(colonne_jouee, nom_joueur)