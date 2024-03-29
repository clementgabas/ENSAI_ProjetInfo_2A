from jeuxservice.plateau.abstractgrid import AbstractGrid
from jeuxservice.player.oieplayer import PlayerOie
import math
import DAO.gestionParticipation as DAOparticipation


class Dice:
    """
    Classe qui permet de gérer les dés : le lancer, le nb de dés, le nombre de valeurs (faces)
    """


    def __init__(self, numofdice, numoffaces):
        """
        Méthode qui initialise la classe dé

        Parameters
        -------
        numofdice : int
            nombre de dé
        numoffaces : int
            nombre de faces

        En fonction du nombre de dés, on définit la dimension du tableau _diceresult
        """
        self._numofdice = numofdice
        self._numoffaces = numoffaces
        self._diceresult = []
        for i in range(self._numofdice):
            self._diceresult.append(0)



    #def throw(self):
    #    """
    #   Jeté de dés : pour chaque dé, on fait un random (entre 1 et nb faces) et on stocke ce résultat dans _diceresult
    #    """
    #    for i in range(self._numofdice):
    #        self._diceresult[i] = random.randint(1, self._numoffaces)

    def throw(self, dice1, dice2):
        """
        Méthode qui ajoute le résultat du lancé de des a la table _diceresult.

        Parameters
        -------
        dice1 : int
            valeur du premier dé
        dice2 : int
            valeur du deuxieme dé
        """
        self._diceresult[0], self._diceresult[1] = dice1, dice2

    def get_dices(self, coup):
        """
        Méthode qui atribue une valeur à chaque dé

        Parameters
        -------
        coup : float
            valeure a donnée au dé.

        Returns
        -------
        type = tuple
            valeur des dés
        """

        #coup = 1.2 ou coup = 6.3 ou coup = 4.4
        dice1 = math.floor(coup)
        dice2 = round(coup%1*10)
        return (dice1, dice2)

    def dicevalue(self, num):
        """
        Méthode qui demande le résultat d'un lancé de dé
        
        Parameters
        ------
        num: int
            id du dé

        Returns
        ------
        type = int
            resultat du lancé
        """
        return self._diceresult[num]

    def sumofdices(self):
        """
        Renvoie somme de tous les dés
        """
        s = 0
        for i in range(self._numofdice):
            s = s + self._diceresult[i]
        return s

class Box:
    """
    Classe qui définit une case par sa règle
    """

    def __init__(self, boxType):
        """
        Méthode qui initialise en mettant la règle de la case

        Parameters
        ------
        boxType : str
            regle de la case
        """
        self._boxType = boxType


    def setType(self, boxType):
        """
        Méthode qui affecte une règle

        Parameters
        ------
        boxType : str
            regle à affecter
        """
        self._boxType = boxType

class Tray(AbstractGrid, Dice):
    """
    Classe qui représent le plateau qui hérité de la classe dé
    Sert à définir le nombre de cases, les particularités des cases
    """
    _nbBox = 1  # nb de cases
    _boxList = []  # tableau de classes 'box'

    def __init__(self, numofdice, numoffaces, nbBox, id_partie):
        """
        Méthode qui initialise la classe Tray

        Parameters
        -------
        numofdice : int
            nombre de dé
        numoffaces : int
            nombre de faces
        nbBox : int
            nombre de cases
        id_partie : int
            identifiant de la partie

        et definie :
        listOfPlayers : list
            la liste des joueurs initialement vide
        nbOfPlayer : int
            nombre de joueurs dans la partie
        """
        self._nbBox = nbBox
        Dice.__init__(self, numofdice, numoffaces)

        # Dimensione le tableau _boxList en fonction de _nbBox
        for i in range(self._nbBox + 1):
            box = Box("None")  # On instancie une classe box
            self._boxList.append(box)  # Qui est ajoutée au tableau _boxList

        self.listOfPlayers = []
        self.nbOfPlayer = len(self.listOfPlayers)
        self.id_partie = id_partie

    def make_liste_of_players(self): ######
        """
        Méthode qui rajoute tous les participants à la liste des joueurs.
        """
        liste_players_ordonnee = DAOparticipation.get_all_players2(self.id_partie)
        liste_couleur_ordonnee = DAOparticipation.get_liste_couleur(self.id_partie)
        L = []
        for i in range(len(liste_couleur_ordonnee)):
            L.append([liste_players_ordonnee[i], liste_couleur_ordonnee[i]])
        L2 = []
        for k in range(len(L)):
            name, color, ordre = L[k][0][0], L[k][1][0], k
            joueur = PlayerOie(name, color, ordre)
            L2.append(joueur)
        self.listOfPlayers = L2
        print(f"Liste des joueurs : {self.listOfPlayers}")

    def simulation(self, liste_coups):
        """
        Méthode qui simule un coup joué par un joueur.

        Parameters
        ------
        liste_coups : list
            liste des coup qui ont eu lieu dans la partie, ces coups sont eux même des dictionnaires.

        Returns
        -------
        dico : dict
            Dictionnaire contenant tous les participants. Et aqqui a chaque joueur associe un dictionnaire contenant
             nom, couleur, ordre de jeu, nombre de tour d'attente, position actuelle et position précédente deu joueur.
        """
        self.make_liste_of_players()
        self.Set_GameByDefault()
        for coup in liste_coups:
            colonne_jouee = coup[3]
            dice1, dice2 = self.get_dices(colonne_jouee)
            ordre_joueur = DAOparticipation.get_position_ordre(pseudo=coup[2], id_partie=coup[0])
            self.Throw(dice1, dice2, ordre_joueur)
        dico = {}
        for player in self.listOfPlayers:
            dico[f"{player._name}"] = player.get_dico()
        return dico

    def Throw(self, dice1, dice2, ordre):
        """
        Méthode qui gére le fait qu'un joueur joue son coup et qui véfie si il y a victoire.

        Parameters
        ----------
        dice1 : int
            premier dé.
        dice2 : int
            Deuxième dé.
        ordre : int
            Ordre de passage.

        Returns
        -------
        endOfGame : 1
            est retourné si et seulement si le joueur gagne la partie.

        """
        currentplayer = self.listOfPlayers[ordre-1]  # récupère le joueur actuel (celui qui joue)

        if currentplayer.test_waitingturn() == 1:  # test si le joueur ne doit pas passer son tour
            currentplayer.set_previousbox(currentplayer.get_actualbox())
            actualBox = currentplayer.get_actualbox()  # récupère sa case actuelle
            self.throw(dice1, dice2) #on récupère ces dés
            currentplayer.add_dice(self.sumofdices())  # on ajoute dés à case actuelle
            currentplayer.set_actualbox(self.compute_lastbox(currentplayer.get_actualbox()))  # on déplace le joeur sur new case & on vérifie qu'il ne dépasse pas la dernière case

            print(f"{currentplayer._name} est en sur la case {currentplayer._actualbox} et était juste avant sur la case {currentplayer._previousbox}")

            # Teste victoire joueur ?
            if self.test_If_Win(currentplayer.get_actualbox()) == 1: #victoire du joueur
                print("partie finie")
                endOfGame = 1
                return endOfGame

            # Si pas victoire, renvoie résultat du test combinaison spéciale de dés
            resultDiceRules = self.compute_dice()
            print(f"resultDiceRules : {resultDiceRules}")

            # On regarde s'il a fait une combinaison spéciale de dés (par exemple doubles)
            if resultDiceRules[1] == 1:
                currentplayer.set_actualbox(resultDiceRules[0])


            else:
                ruletest = 1
                while ruletest > 0:
                    resultBoxRules = self.compute_rule(currentplayer.get_actualbox(), actualBox)
                    ruletest = resultBoxRules[0] == 1 and resultBoxRules[1] != actualBox and resultBoxRules[
                        1] < self._nbBox

                    if resultBoxRules[0] != 0:
                        print("        case spéciale:", self.get_type(currentplayer.get_actualbox()))

                    if resultBoxRules[0] == 1:  # case speciale concerne seulement le joueur
                        currentplayer.set_actualbox(self.compute_lastbox(resultBoxRules[1]))
                        currentplayer.set_waitingturn(resultBoxRules[2])
                        ruletest = currentplayer.get_waitingturn() == 1

                    elif resultBoxRules[0] == 2:  # case speciale concerne aussi un autre joueur
                        currentplayer.set_actualbox(resultBoxRules[1])
                        currentplayer.freeze_waiting()

                        for k in range(self.numberOfPlayer):
                            player = self.listOfPlayers[k]

                            if player.get_actualbox() == currentplayer.get_actualbox():
                                # il s'agit du joueur sur la meme case
                                # on lui applique les regle de la case liberee
                                player.set_actualbox(resultBoxRules[3])  # on affecte l'ancienne case du joueur actif
                                player.set_waitingturn(resultBoxRules[4])  # le joueur redemarre
                                break


    def Set_GameByDefault(self):
        """
        Méthode qui définit les regles par defaut du jeu de l'oie
        """
        self.set_rules(6, "Bridge")
        self.set_rules(9, "Goose")# on sort cette règle si
        self.set_rules(12, "Bridge")
        self.set_rules(14, "Goose")
        self.set_rules(18, "Goose")
        self.set_rules(19, "Hotel")
        self.set_rules(23, "Goose")
        self.set_rules(26, "Dice63")
        self.set_rules(27, "Goose")
        self.set_rules(31, "Well")
        self.set_rules(32, "Goose")
        self.set_rules(36, "Goose")
        self.set_rules(41, "Goose")
        self.set_rules(42, "Labyrinth")
        self.set_rules(45, "Goose")
        self.set_rules(50, "Goose")
        self.set_rules(52, "Jail")
        self.set_rules(53, "Dice54")
        self.set_rules(54, "Goose")
        self.set_rules(58, "Skull")
        self.set_rules(59, "Goose")

    def set_rules(self, boxnumber, boxtype):
        """
        Méthode qui affecte une règle à une case

        Parameters
        ------
        boxnumber : int
            Numéro de la case
        boxtype : str
            règle à affecter

        """
        box = self._boxList[boxnumber]  # Récupère l'instance de la box dans le tableau
        box.setType(boxtype)  # Et on lui affecte la règle

    def get_type(self, boxnumber):
        """
        Methode qui permet d'obtenir la règle d'une case.

        Parameters
        ---------
        boxnumber : int
            Numéro de la case.

        Returns
        -------
        type : str
            Regle de la case.
        """
        box = self._boxList[boxnumber]
        return box._boxType

    def search_box(self, start, end, test):
        """
        Méthode qui cherche la prochaine case ayant pour règle la valeur de test.

        Parameters
        ----------
        start : int
            Départ
        end : int
            Fin
        test : str
            regle à rechercher.

        Returns
        -------
        type : int
            Egale au numéro de la case si elle existe, à -1 sinon.

        """
        for i in range(start, end):
            # recherche la première case (suivante) qui a la règle 'test'
            if self.get_type(i) == test:
                print(f"case trouvée : {i} pour la règle {test}")
                return i
        return -1

    def compute_dice(self):
        """
        Méthode qui recherche si il y a une combinaison de dés qui envoie sur une case spéciale.

        Returns
        -------
        foundbox : int
            Case ou doit être envoyé le joueur du à cette combinaison de dés. Est égale a -1 si il n'y a aucune conbinaison

        type : int
            Egale à 1 si une combinaison a été trouvée. 0 sinon
        """
        dice1 = 0
        dice2 = 0
        # recherche de la combinaison 6 + 3

        for i in range(self._numofdice):
            if self._diceresult[i] == 6:
                dice1 = 1
            elif self._diceresult[i] == 3:
                dice2 = 1

        if dice1 == 1 and dice2 == 1:
            print("Vous avez fait un 6 et un 3. Vous allez donc sur la case la plus proche pour la règle Dice63")
            # on recherche la case Dice63
            foundbox = self.search_box(0, self._nbBox, "Dice63")
            if foundbox != -1:
                return foundbox, 1  # retourne le tuple: index de la case Dice63 , combinaison speciale trouve == 1
        dice1 = 0
        dice2 = 0

        # recherche de la combinaison 5 + 4
        for i in range(self._numofdice):
            if self._diceresult[i] == 5:
                dice1 = 1
            elif self._diceresult[i] == 4:
                dice2 = 1

        if dice1 == 1 and dice2 == 1:
            print("Vous avez fait un 4 et un 5. Vous allez donc sur la case la plus proche pour la règle Dice54")

            # on recherche la case Dice54
            foundbox = self.search_box(0, self._nbBox, "Dice54")
            if foundbox != -1:
                return foundbox, 1  # retourne le tuple: index de la case Dice54 , combinaison speciale trouve == 1

        return -1, 0  # retourne le tuple: index fictif , combinaison speciale non trouve == 0

    def compute_rule(self, boxnumber, previousbox):
        """
        Méthode qui recherche si il y a des cases speciales

        Parameters
        ----------
        boxnumber : int
            Numéro de la case
        previousbox : int
            Numéro de la case précédente.

        Returns
        -------
        type : int
            différent entier deffinissant entre autre si le joueur peut jouer ou non et la case sur laquelle
            il sera au prochain tour.

        """
        # return tuple type/box/nextturn
        box = self._boxList[boxnumber]

        if box._boxType == "Goose":
            print("Vous êtes sur une oie, avancez à nouveau du nombre de points réalisés.")
            return 1, boxnumber + self.sumofdices(), 1
        elif box._boxType == "Bridge":
            print("case pont. Si vous êtes en case 6, allez en case 12. Si vous êtes en case 12, allez en case 6.")
            foundbox = self.search_box(boxnumber + 1, self._nbBox, "Bridge")
            if foundbox != -1:
                return 1, foundbox, 1;
            return boxnumber, 1

        elif box._boxType == "Hotel":
            print("Vous êtes tombés sur la case Hotel et devrez donc passer 2 fois votre tour.")
            return 1, boxnumber, 4

        elif box._boxType == "Jail":
            print(
                "Case prison. Vous ne pourrez sortir et rejouer que lorsqu'un autre joueur tombera sur cette case. En attendant, passez votre tour.")

            return 2, boxnumber, 0, previousbox, 1

        elif box._boxType == "Well":
            if self.nbOfPlayer >2:
                print("Case puit. Vous ne pourrez sortir et rejouer que lorsqu'un autre joueur tombera sur cette case. En attendant, passez votre tour.")
                return 2, boxnumber, 0, boxnumber, 1
            else: #a 2 joueurs, on ne peut pas joue ravec le puit ET la prison sinon on peut bloquer la partie.
                pass

        elif box._boxType == "Labyrinth":
            print("Vous êtes sur la case labyrinth. Reculez de 12 cases.")
            return 1, boxnumber - 12, 1

        elif box._boxType == "Skull":
            print("Vous êtes sur la case tête de mort. Recommencez depuis le début!!!")
            return 1, 0, 1

        return 0, boxnumber, 1

    def compute_lastbox(self, boxnumber):
        """
        Méthode qui permet de gérer fin du plateau pour qu'un dé trop grand revienne en arrière.

        Parameters
        ----------
        boxnumber : int
            Numero de la case

        Returns
        -------
        boxnumber : int
            Nouvelle case
        """
        if boxnumber > self._nbBox:
            boxnumber = self._nbBox - (boxnumber - self._nbBox)
        return boxnumber

    def test_If_Win(self, boxnumber):
        """
        Méthode qui va tester la case finale pour voir si victoire

        Parameters
        ----------
        boxnumber : Numero de la case

        Returns
        -------
        type : bool
            True si le joueur est bien sur la derniere case, False sinon.

        """
        return boxnumber == self._nbBox

