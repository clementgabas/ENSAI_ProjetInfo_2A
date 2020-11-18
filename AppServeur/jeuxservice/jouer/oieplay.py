from jeuxservice.jouer.abstractplay import AbstractPlay
from jeuxservice.jeux.oiegame import Game     
import DAO.gestionCoups as DAOcoups
import DAO.gestionParticipation as DAOparticipation


class Play(AbstractJeu):

    def __init__(self, id_partie):  
        AbstractJeu.__init__(self, id_partie)
        self.gameGoose = Game()

    def Start(self):
        player = Player()
        player.Set_Param(self.playerList[0], self.colorList[0])
        self.gameGoose.set_Players(player)
        player = Player()
        player.Set_Param(self.playerList[1], self.colorList[1])
        self.gameGoose.set_Players(player)
        player = Player()
        player.Set_Param(self.playerList[2], self.colorList[2])
        self.gameGoose.set_Players(player)
        player = Player()
        player.Set_Param(self.playerList[3], self.colorList[3])
        self.gameGoose.set_Players(player)
        
        self.gameGoose.Set_NbBoxOnLineOfGrid(8)
        self.gameGoose.Init()
        self.gameGoose.ShowTray()

        endOfGame = False  # Booléen pour continuer la partie en fct de si elle est terminée (s'arrête à 1) 
        print("\n Début de partieeeeeeeeee ! \n") 
        self.gameGoose.ShowTray()
        while endOfGame == False:
            num_coup = self.gameGoose.NewGameTurn()  # ***bdd***
            for j in range(gameGoose.Get_NumberPlayers()):
                self.gameGoose.Set_CurrentPlayer(j)  # affecte le joueur actuel (celui qui joue)
                pseudo_joueur = gameGoose.Get_PlayerName()  # ***bdd***
                self.gameGoose.Play()
                position = self.gameGoose.Get_Box()  # ***bdd***
                waitTime = self.gameGoose.Get_WaitTime()  # ***bdd***
                endOfGame = self.gameGoose.TestIfWin()
                DAOcoups.add_new_coup(self.id_partie, num_coup , pseudo_joueur, position, waitTime)
                if endOfGame == True:
                    break
            self.gameGoose.ShowTray()


    def simulate(self):
        liste_coups = DAOcoups.get_all_coups(self.id_partie)  
        maxTurn = 0
        for coup in liste_coups: 
            if maxTurn < coup[1]:
                maxTurn = coup[1]
            nom_joueur = coup[2]
            colonne_jouee = coup[3]
            temps_attente = coup[4]
            self.gameGoose.PlaySimul(nom_joueur, colonne_jouee, v)
        for j in range(maxTurn):
            self.gameP4.NewGameTurn()