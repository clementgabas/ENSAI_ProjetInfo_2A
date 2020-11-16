from jeuxservice.jeux.abstractjeux import AbstractJeu
from jeuxservice.plateau.p4grid import GridP4
import DAO.gestionCoups as DAOcoups
import DAO.gestionParticipation as DAOparticipation


class GameP4(AbstractJeu):

    def __init__(self, id_partie):
        AbstractJeu.__init__(self, id_partie)
        self.nbcolumn = 7
        self.nbline = 6
        self.nbToken = 4
        self.numberOfPlayer = 2

    def initialisation(self):
        self.power4Grid = GridP4(self.nbline, self.nbcolumn, self.nbToken)  # nb lignes, nb colonnes, nb jetons alignés

    def jouer_un_coup(self, coup, gridClass):
        #coup = {'player' : ... , 'id_partie': ... , 'colonne': ...}
        from jeuxservice.jeux.p4game import PlayerP4
        playerClass = PlayerP4(coup[0],
                               color= DAOparticipation.get_couleur(pseudo=coup[0], id_partie=coup[1]),
                               ordre= DAOparticipation.get_position_ordre(pseudo=coup[0], id_partie=coup[1])
                               )

        if self.is_coup_valide(coup, gridClass)["Statut"]:
            gridClass.Throw(self.is_coup_valide(coup, gridClass)["Colonne"], playerClass.Get_Token())
            self.enregistrer_coup(coup, playerClass)
        return gridClass.getGrid()

    def is_coup_valide(self, coup, gridClass):
        #coup = {'player' : ... , 'id_partie': ... , 'colonne': ...}
        val_column = int(coup["colonne"])
        try:
            if 0 <= val_column <= (self.nbcolumn - 1):
                if gridClass.TestEndColumn(val_column):
                    resultat = self.update_resultat(False, "La colonne est pleine!")
                else:
                    resultat = self.update_resultat(True, "Le coup est valide")
        except ValueError:
            resultat = self.update_resultat(False, "Le numero de colonne n'est pas valide !")
        finally:
            resultat["Colonne"] = val_column
            return resultat


    def enregistrer_coup(self, coup):
        #coup = {'player' : ... , 'id_partie': ... , 'colonne': ...}

        id_partie = coup["id_partie"]
        num_coup = DAOcoups.get_last_coup(id_partie)
        pseudo_joueur = coup["player"]
        position = coup["colonne"]
        prochain_tour = 1
        DAOcoups.add_new_coup(id_partie, num_coup , pseudo_joueur, position, prochain_tour)


