class Player():

    def __init__(self, pseudo, id_salle, chef_salle, jeu):
        self.pseudo = pseudo
        self.id_salle = id_salle
        self.chef_salle = chef_salle
        self.jeu = jeu

    def choix_couleur(self):
        pass

    def ask_api_if_tour(self):
        pass

    def ask_api_if_partie_lancee(self):
        pass
        