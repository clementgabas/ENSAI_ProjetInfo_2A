from jeuxservice.plateau.abstractgrid import AbstractGrid
import DAO.gestionParticipation as DAOparticipation

class Tray(AbstractGrid, Dice):
    """
    Plateau qui h�rit� de la classe d�
    Sert � d�finir le nombre de cases, les particularit�s des cases
    """
    
    def __init__(self, numofdice, numoffaces, nbBox):
        """
        Initialisation nb d�s, nb faces et le nb de cases
        """
        self._nbBox = nbBox # nb de cases
        self._boxList = []  # tableau de classes 'box'
        Dice.__init__(self, numofdice, numoffaces)
        # Dimensione le tableau _boxList en fonction de _nbBox
        for i in range(self._nbBox + 1):
            box = Box("None")  # On instancie une classe box
            self._boxList.append(box)  # Qui est ajout�e au tableau _boxList

    def Set_GameByDefault(self):
        """
        On definit les regles par defaut du jeu de l'oie
        """
        self.set_rules(6, "Bridge")
        self.set_rules(9, "Goose")
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
        Affecte une r�gle � une case
        Prend num case et sa r�gle
        """
        box = self._boxList[boxnumber]  # R�cup�re l'instance de la box dans le tableau
        box.setType(boxtype)  # Et on lui affecte la r�gle

    def get_type(self, boxnumber):
        """
        Obtenir la r�gle d'une case en donnant son num�ro
        """
        box = self._boxList[boxnumber]
        return box._boxType

    def search_box(self, start, end, test):
        """
        Cherche la prochaine case ayant pour r�gle la valeur de test (par rapport au start et au end)
        """
        for i in range(start, end):
            # recherche la premi�re case (suivante) qui a la r�gle 'test'
            if self.get_type(i) == test:
                return i
        return -1

    def compute_dice(self):
        """
        recherche de combinaison de d�s
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
            # on recherche la case Dice54
            foundbox = self.search_box(0, self._nbBox, "Dice54")
            if foundbox != -1:
                return foundbox, 1  # retourne le tuple: index de la case Dice54 , combinaison speciale trouve == 1
        return -1, 0  # retourne le tuple: index fictif , combinaison speciale non trouve == 0

    def compute_rule(self, boxnumber, previousbox):
        """
        Recherche de cases speciales
        """
        # return tuple type/box/nextturn
        box = self._boxList[boxnumber]
        if box._boxType == "Goose":
            return 1, boxnumber + self.sumofdices(), 1
        elif box._boxType == "Bridge":
            foundbox = self.search_box(boxnumber + 1, self._nbBox, "Bridge")
            if foundbox != -1:
                return 1, foundbox, 1
            return boxnumber, 1
        elif box._boxType == "Hotel":
            return 1, boxnumber, 4
        elif box._boxType == "Jail":
            return 2, boxnumber, 0, previousbox, 1
        elif box._boxType == "Well":
            return 2, boxnumber, 0, boxnumber, 1
        elif box._boxType == "Labyrinth":
            return 1, boxnumber - 12, 1
        elif box._boxType == "Skull":
            return 1, 0, 1
        return 0, boxnumber, 1

    def compute_lastbox(self, boxnumber):
        """
        G�rer fin du plateau pour qu'un d� trop grand revienne en arri�re
        """
        if boxnumber > self._nbBox:
            boxnumber = self._nbBox - (boxnumber - self._nbBox)
        return boxnumber

    def test_If_Win(self, boxnumber):
        """
        Tester case finale pour voir si victoire
        """
        return boxnumber == self._nbBox


class Box:
    """
    D�finit une case par sa r�gle
    """
    def __init__(self, boxType):
        """
        Initialise en mettant la r�gle de la case
        """
        self._boxType = boxType

    def setType(self, boxType):
        """
        Affecter une r�gle
        """
        self._boxType = boxType

class Dice:
    """
    Permet de g�rer les d�s : le lancer, le nb de d�s, le nombre de valeurs (faces)
    """
    _numofdice = 0  # nb de d�s
    _diceresult = []  # stocker le r�sultat de chaque d� (sa dimension varie en fct du nb de d�s)
    _numoffaces = 0  # nb de faces par d�

    def __init__(self, numofdice, numoffaces):
        """
        Initialisation de la classe d�
        D�finir nb d�s et nb faces
        En fct nb d�s, on d�finit la dimension du tableau _diceresult
        """
        self._numofdice = numofdice
        self._numoffaces = numoffaces
        for i in range(self._numofdice):
            self._diceresult.append(0)

    def throw(self):
        """
        Jet� de d�s : pour chaque d�, on fait un random (entre 1 et nb faces) et on stocke ce r�sultat dans _diceresult
        """
        for i in range(self._numofdice):
            self._diceresult[i] = random.randint(1, self._numoffaces)

    def Get_numOfDice(self):
        return self._numofdice

    def dicevalue(self, num):
        """
        Demande le r�sultat d'un lancer de d� en donnant l'id du d� (_dicevalue[0] donne le premier d�)
        """
        return self._diceresult[num]

    def sumofdices(self):
        """
        Renvoie somme de tous les d�s
        """
        s = 0
        for i in range(self._numofdice):
            s = s + self._diceresult[i]
        return s