from abc import ABC

class AbstractJeu(ABC):
    """
    Classe abstraite qui défini la partie action du jeu
    """

    def __init__(self, id_partie):
        """
        Fonction initiatrice qui définie :
            id_partie : int
                l'identifiant de la partie
        et qui initie :
            listOfPlayers : list
                liste des membres de la partie, initialement nulle.
            numberOfPlayer : int
                Nombre de joueur dans la partie, initialement nul.
        """
        self.listOfPlayers = []
        self.id_partie = id_partie
        self.numberOfPlayer = len(self.listOfPlayers)


    def set_Players(self, playerClass):
        """
        Procédure qui ajoute un joueur à la liste des membre de la partie.
        :param
        ------
        playerClass : objet
            information sur le joueur a ajouter.
        """
        self.listOfPlayers.append(playerClass)

    def initialisation(self):
        """
        Méthode abstraite
        """
        pass

    def jouer_un_coup(self): #a supp ?
        """
        Méthode abstraite
        """
        pass

    def create_resultat(self):
        """
        Procédure qui permet de crée un dictionnaire composé d'un statut et d'un message associée a ce statut.
        """
        return {"Statut": "", "Message": ""}

    def update_resultat(self, statut, message=""):
        """
        Fontion qui permet de mettre a jour un dictionnaire, en modifiant le statut et le message associé

        :param
        -----
        statut: str
            statut de la réponse
        message: str
            message associé, ce paramètre étant optionnel, si rien n'est rentré, on le suppose vide

        :return
        ------
        Resultat : dict
            Dictionnaire mis à jour
        """
        Resultat = self.create_resultat()
        Resultat["Statut"] = statut
        Resultat["Message"] = message
        return Resultat
