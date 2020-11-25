from jeuxservice.plateau.abstractgrid import AbstractGrid
import DAO.gestionParticipation as DAOparticipation

class GridP4(AbstractGrid):
    """Classe qui hérite de la classe AbstractGrid et qui gére la partie plateau du Puissance 4 """

    def __init__(self, numHeight, numWidth, tokenWinNumber):
        """
        Fonction initiatrice qui définie :
            numHeight : int
                Nombre de lignes dans la grille
            numWidth : int
                Nombre de colonnes
            tokenWinNumber : int
                Nombre de jetons à aligner pour gagner la partie.
        et qui initie :
            gridList : list
                grille sous forme de liste de taille numWidth x numHeight, remplie de 0 représentant une case vide
            win : int
                Attribut signifiant si il y a vitoir ou non, initialement égale à 0.
        """
        self._numHeight = numHeight
        self._numWidth = numWidth
        self._tokenWinNumber = tokenWinNumber
        self._gridList = []
        self._win = 0
        for k in range(self._numWidth):
            self._gridList.append([0] * self._numHeight)

    def simulatation(self, liste_coups):
        """
        Méthode qui simule un coup joué par un joueur.
        Parameters
        ------
        liste_coups : list
            liste des coup qui ont eu lieu dans la partie, ces coups sont eux même des dictionnaires.
        """
        for coup in liste_coups:
            colonne_jouee = coup[3]
            ordre_joueur = DAOparticipation.get_position_ordre(pseudo=coup[2], id_partie=coup[0])
            self.Throw(colonne_jouee, ordre_joueur)

    def Throw(self, x, tokenColor):
        """
        Méthode qui gére l'ajout d'un jeton et qui verifie si le nombre de jeutons de meme couleur qui sont alignés.

        Parameters
        ------
        x: int
            numéro de colonne ou joue le joueur.
        tokenColor : int
            numéro associé à la couleur du joueur.

        Returns
        ------
        resultat : dict
            Dictionnaire contenant la réussite ou non que l'utilisateur ait aligné un nombre de jetons suffisant une partie, et le message associé.
                Si l'utilisateur a réussi a aligné un nombre de jetons suffisant, le statut sera le booléen True.
                Sinon il sera sur False.

        """
        y = 0

        for i in range(self._numHeight):
            if self._gridList[x][i] == 0:
                self._gridList[x][i] = tokenColor #tokenColor vaut 1 ou 2
                y = i
                break
        result = [1, 1, 1, 1]
        continueTest = [1, 1, 1, 1, 1, 1, 1, 1]
        resultat = self.update_resultat(False, f"Vous n'avez pas encore aligné {self._tokenWinNumber} jetons...")

        for i in range(1, self._tokenWinNumber):
            # test horizontal - on scrute la couleur des jetons a gauche puis a droite
            if x - i >= 0:  # pas de debordement hors de la grille a gauche
                if continueTest[0] == 1:  # on continue car pas d'interruption de couleur a gauche
                    if self._gridList[x - i][y] == tokenColor:  # le jeton est de la bonne couleur
                        result[0] = result[0] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[0] = 0  # interruption de couleur - on arrete de chercher a gauche

            if x + i < self._numWidth:  # pas de debordement hors de la grille a droite
                if continueTest[1] == 1:  # on continue car pas d'interruption de couleur a droite
                    if self._gridList[x + i][y] == tokenColor:  # le jeton est de la bonne couleur
                        result[0] = result[0] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[1] = 0  # interruption de couleur - on arrete de chercher a droite

            # test vertical - on scrute la couleur des jetons en bas puis en haut
            if y - i >= 0:  # pas de debordement hors de la grille en bas
                if continueTest[2] == 1:  # on continue car pas d'interruption de couleur par le bas
                    if self._gridList[x][y - i] == tokenColor:  # le jeton est de la bonne couleur
                        result[1] = result[1] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[2] = 0  # interruption de couleur - on arrete de chercher en bas

            if y + i < self._numHeight:  # pas de debordement hors de la grille en haut
                if continueTest[3] == 1:  # on continue car pas d'interruption de couleur par le haut
                    if self._gridList[x][y + i] == tokenColor:  # le jeton est de la bonne couleur
                        result[1] = result[1] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[3] = 0  # interruption de couleur - on arrete de chercher a droite

            # test diagonal montante - on scrute vers le bas a gauche et le haut a droite
            if x - i >= 0 and y - i >= 0:  # pas de debordement hors de la grille a gauche et en bas
                if continueTest[4] == 1:  # on continue car pas d'interruption de couleur par le bas
                    if self._gridList[x - i][y - i] == tokenColor:  # le jeton est de la bonne couleur
                        result[2] = result[2] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[4] = 0  # interruption de couleur - on arrete de chercher a gauche en bas

            if x + i < self._numHeight and y + i < self._numHeight:  # pas de debordement hors de la grille a droite et en haut
                if continueTest[5] == 1:  # on continue car pas d'interruption de couleur par le haut
                    if self._gridList[x + i][y + i] == tokenColor:  # le jeton est de la bonne couleur
                        result[2] = result[2] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[5] = 0  # interruption de couleur - on arrete de chercher a droite en haut

            # test diagonale descendante - on scrute vers le haut a gauche et le bas a droite
            if x - i >= 0 and y + i < self._numHeight:  # pas de debordement hors de la grille a gauche et en haut
                if continueTest[6] == 1:  # on continue car pas d'interruption de couleur par le bas a gauche
                    if self._gridList[x - i][y + i] == tokenColor:  # le jeton est de la bonne couleur
                        result[3] = result[3] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[6] = 0  # interruption de couleur - on arrete de chercher en haut a gauche

            if x + i < self._numHeight and y - i >= 0:  # pas de debordement hors de la grille a droite et en bas
                if continueTest[7] == 1:  # on continue car pas d'interruption de couleur par le haut a droite
                    if self._gridList[x + i][y - i] == tokenColor:  # le jeton est de la bonne couleur
                        result[3] = result[3] + 1  # on increment le nombre de jetons alignes
                    else:
                        continueTest[7] = 0  # interruption de couleur - on arrete de chercher en bas a gauche

            if self._sum(continueTest) == 0:  # il n'y a plus de jeton de couleur alignes
                break

            for j in result:
                if j == self._tokenWinNumber:  # le nombre de jetons alignes est le bon
                    self._win = 1
                    resultat = self.update_resultat(True, f"Vous avez aligné {self._tokenWinNumber} jetons!")
                    break
        return resultat

    def TestIfWin(self):
        """
        Methode qui vérifie si il y a une victoire
        """
        print(str(self._gridList))
        return (self._win == 1)

    def TestEndOfGame(self):
        result = True
        for i in range(self._numWidth):
            result = result and self._gridList[i][self._numHeight - 1] != 0
        return result

    def TestEndColumn(self, column):
        """
        Méthode qui test si une colonne est pleine.

        Parameters
        ------
        column : int
            Numéro de la colonne à tester

        Returns
        ------
        type : Bool
            True : si la colonne est pleine.
            False : Sinon.

        """
        return self._gridList[column][self._numHeight - 1] != 0

    # def ClearGrid(self):#on l'utilise jamais?
    #     self._win = 0
    #     for k in range(self._numWidth):
    #         for l in range(self._numHeight):
    #             self._gridList[k][l] = 0

    def getGrid(self):
        """
        Méthode qui affiche la grille du jeu.

        Returns
        ------
        gridList : Liste
            grille sous forme de liste.
        """
        return self._gridList

    def _sum(self, arr):
        """
        Méthode qui somme les élement d'une liste

        Parameters
        ------
        arr : list
            liste d'entier.

        Returns
        -------
        sum :int
        somme des éléments
        """
        sum = 0
        for i in arr:
            sum = sum + i
        return sum