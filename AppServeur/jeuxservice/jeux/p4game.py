from jeuxservice.jeux.abstractjeux import AbstractJeu
from jeuxservice.plateau.p4grid import GridP4

import DAO.gestionCoups as DAOcoups
import DAO.gestionParticipation as DAOparticipation


class GameP4(AbstractJeu):
    """
    Classe qui hérite de la classe AbstractJeu et qui défini la partie d'un Puissance 4
    """
    def __init__(self, id_partie):
        """
        Fonction init qui définie :
            id_partie : int
                l'identifiant de la partie
        et qui initie :
            listOfPlayers : list
                liste des membres de la partie, initialement nulle.
            numberOfPlayer : int
                Nombre de joueur dans la partie, initialement nul.
            nbcolumn : int
                Le nombre de colonnes égale à 7.
            nbline : int
                Le nombre de lignes égale à 7.
            nbToken : int
                Le nombre de jetons à alligner pour gagner la partie égale à 4.
            numberOfPlayer : int
                Le nombre de joueur, égale à 2.


        """
        AbstractJeu.__init__(self, id_partie)
        self.nbcolumn = 7
        self.nbline = 7
        self.nbToken = 4
        self.numberOfPlayer = 2

    def initialisation(self):
        """
        Méthode qui initialise la grille de puissance 4 en prenant, le nombre de lignes, le nombre de colonnes et
        le nombre de jetons à alligner pour gagner la partie.
        """
        self.power4Grid = GridP4(self.nbline, self.nbcolumn, self.nbToken)  # nb lignes, nb colonnes, nb jetons alignés

    def jouer_un_coup(self, coup, gridClass):
        """
        Méthode qui va gérer la séquence où un joueur joue son tour.

        :param
        ------
        Coup : dict
            Dictionnaire contenant le nom du joueur, la partie dans laquelle il se trouve, et la colonne dans laquelle
            il souhaite jouer.
        gridClass : Objet de la classe GridP4
            Grille de jeu en cours, avec tous les coups déja joués.

        :return
        -------
        type = list
            Liste representant la grille contenant les coups joués.
                Si le coup était valide alors il fait partie de cette liste. Sinon la grille est inchangée.
        """
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
        """
        Méthode qui vérifie si le coup joué par un joueur est valide.

        :param
        ------
        Coup : dict
            Dictionnaire contenant le nom du joueur, la partie dans laquelle il se trouve, et la colonne dans laquelle
            il souhaite jouer.
        gridClass : Objet de la classe GridP4
            Grille de jeu en cours, avec tous les coups déja joués.

        :return
        -------
        Resultat: dict
            Dictionnaire contenant la réussite, ou non, cette vérifiaction et le message associé.
                Si le coup est valide,  le statut sera le booléen True.

                A l'inverse, le statut sera le booléen False si les erreurs, que précisera le message associé, arrivent:
                    -Le numero de colonne n'est pas valide.

                    -La colonne est pleine.

                 De plus, le dictionnaire renverra aussi le numéro de la colonne ou a été joué le coup
        """
        #coup = {'player' : ... , 'id_partie': ... , 'colonne': ...}
        try:
            val_column = int(coup["colonne"])
        except:
            val_column = -1
        if val_column >= self.nbcolumn or val_column < 0:
            resultat = self.update_resultat(False, "Le numero de colonne n'est pas valide !")
        try:
            if 0 <= val_column <= (self.nbcolumn - 1):
                if gridClass.TestEndColumn(val_column):
                    resultat = self.update_resultat(False, "La colonne est pleine!")
                else:
                    resultat = self.update_resultat(True, "Le coup est valide")
        except:
            resultat = self.update_resultat(False, "Le numéro de colonne n'est pas valide !")
        finally:
            resultat["Colonne"] = val_column
            return resultat


    def enregistrer_coup(self, coup):
        """
        Méthode qui enregistre le coup joué.

        :param
        ------
        Coup : dict
            Dictionnaire contenant le nom du joueur, la partie dans laquelle il se trouve, et la colonne dans laquelle
            il a joué.
        """
        #coup = {'player' : ... , 'id_partie': ... , 'colonne': ...}

        id_partie = coup["id_partie"]
        num_coup = DAOcoups.get_last_coup(id_partie)
        pseudo_joueur = coup["player"]
        position = coup["colonne"]
        prochain_tour = 1
        DAOcoups.add_new_coup(id_partie, num_coup , pseudo_joueur, position, prochain_tour)


