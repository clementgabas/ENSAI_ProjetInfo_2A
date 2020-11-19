from jeuxservice.jeux.abstractjeux import AbstractJeu
from jeuxservice.plateau.oiegrid import GridGoose
import DAO.gestionCoups as DAOcoups
import DAO.gestionParticipation as DAOparticipation

class GameGoose(AbstractJeu):

def __init__(self, id_partie):
        AbstractJeu.__init__(self, id_partie)
        self.nbDice = 2
        self.nbFace = 6
        self.nbBox = 63
        self.numberOfPlayer = 4

    def initialisation(self):
        self.gooseTray = Tray(self.nbDice, self.nbFace, self.nbBox)  # 2 dés, 6 face, 63 cases par defaut
        self.gooseTray.Set_GameByDefault()

    def jouer_un_coup(self, coup, gridClass, listOfPlayer): #listOfPlayer = list{'player' : ... , 'id_partie': ... , 'colonne': ..., 'attente':.... }
        #coup = {'player' : ... , 'id_partie': ... , 'colonne': ...}
        from jeuxservice.player.oieplayer import PlayerOie
        playerClass = PlayerGoose(coup[0],
                               color= DAOparticipation.get_couleur(pseudo=coup[0], id_partie=coup[1]),
                               ordre= DAOparticipation.get_position_ordre(pseudo=coup[0], id_partie=coup[1])
                               )
        if playerClass.test_waitingturn() == 1:  # test si le joueur ne doit pas passer son tour
            actualBox = playerClass.get_actualbox()  # récupère sa case actuelle
            gridClass.throw()  # lancer les dés
            playerClass.add_dice(self.gooseTray.sumofdices())  # on ajoute dés à case actuelle
            # on déplace le joueur sur new case & on vérifie qu'il ne dépasse pas la dernière case
            playerClass.set_actualbox(self.gooseTray.compute_lastbox(playerClass.get_actualbox())) 
            self.enregistrer_coup(coup) 
            # Teste victoire joueur ?
            if gridClass.test_If_Win(currentPlayer.get_actualbox()) != 1:
                # Si pas victoire, renvoie résultat du test combinaison spéciale de dés
                resultDiceRules = gridClass.compute_dice()
                # On regarde s'il a fait une combinaison spéciale de dés (par exemple doubles)
                if resultDiceRules[1] == 1:
                    playerClass.set_actualbox(resultDiceRules[0])
                    self.enregistrer_coup(coup)
                else:
                    if playerClass.get_waitingturn() != -1:
                        ruletest = 1
                        while ruletest > 0:
                            resultBoxRules = gridClass.compute_rule(currentPlayer.get_actualbox(), actualBox)
                            ruletest = resultBoxRules[0] == 1 and resultBoxRules[1] != actualBox and resultBoxRules[1] < gridClass._nbBox
                            if resultBoxRules[0] == 1:  # case speciale concerne seulement le joueur
                                playerClass.set_actualbox(gridClass.compute_lastbox(resultBoxRules[1]))
                                playerClass.set_waitingturn(resultBoxRules[2])
                                ruletest = playerClass.get_waitingturn() == 1
                                self.enregistrer_coup(coup)
                            elif resultBoxRules[0] == 2:  # case speciale concerne aussi un autre joueur
                                playerClass.set_actualbox(resultBoxRules[1])
                                playerClass.freeze_waiting()
                                for player in range listOfPlayer:
                                    if player["player"] != playerClass._name:  # il ne s'agit pas du joueur en cours
                                        if player["colonne"] == currentPlayer.get_actualbox():
                                            # il s'agit du joueur sur la meme case
                                            # on lui applique les regle de la case liberee
                                            player["colonne"] = resultBoxRules[3]  # on affecte l'ancienne case du joueur actif
                                            player["attente"] = resultBoxRules[4]  # le joueur redemarre
                                            self.enregistrer_coup(player)
                                            break
        #return gridClass._boxList


    def enregistrer_coup(self, coup):
        #coup = {'player' : ... , 'id_partie': ... , 'colonne': ..., 'attente':....}
        id_partie = coup["id_partie"]
        num_coup = DAOcoups.get_last_coup(id_partie)
        pseudo_joueur = coup["player"]
        position = coup["colonne"]
        prochain_tour = coup["attente"]
        DAOcoups.add_new_coup(id_partie, num_coup , pseudo_joueur, position, prochain_tour)