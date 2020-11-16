import PyInquirer as inquirer
from Vues.abstractView import AbstractView
from Player.PlayerClass import Player

#from printFunctions import timePrint as print



class Jouer(AbstractView):
    def __init__(self, pseudo, id_salle, jeu, est_chef):
        self.pseudo = pseudo.lower()
        self.game = jeu.lower()
        self.id_salle = id_salle
        self.est_chef = est_chef

        if self.game == 'oie':
            self.action_jouer = [
                {
                    'type': 'input',
                    'name': 'action',
                    'message' : "Pour jeter les dés, veuillez appuyer sur la touche entrée."
                }
            ]
        elif self.game == 'p4':
            self.action_jouer = [
                {
                    'type': 'input',
                    'name': 'action',
                    'message': "Veuillez saisir le numéro de la colonne dans laquelle vous souhaitez jouer votre pion."
                }
            ]
        else:
            self.action_jouer = [{'type':'list', 'message':'bug dans classe jouer.'}]


    def jouer(self):
        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.demander_grille()
        self.print_message(Resultat)
        self.print_grille(Resultat["Grille"])

        Player1.jouer_son_tour(self.jouer_son_tour())


        Resultat = Player1.demander_grille()
        self.print_message(Resultat)
        self.print_grille(Resultat["Grille"])



    def print_grille(self, _grid):
        self.nbcolumn, self.nbline = 7, 6

        line = "|"
        separator = "-"
        abscisse = " "
        for k in range(self.nbline):
            separator = separator + "----"

            if k == 0:
                abscisse = 2 * abscisse + str(k) + "   "

            elif k >= 10:
                abscisse = abscisse + str(k) + "  "

            else:
                abscisse = abscisse + str(k) + "   "

        print(separator)
        for i in range(self.nbcolumn - 1, -1, -1):
            for j in range(self.nbline):

                if _grid[j][i] == 0:
                    line = line + "   |"

                elif _grid[j][i] == 1:
                    line = line + " X |"

                elif _grid[j][i] == 2:
                    line = line + " O |"

            print(line)
            print(separator)
            line = "|"
        print(abscisse)


    def jouer_son_tour(self):
        action = inquirer.prompt(self.action_jouer)
        #actoion --> {'action': '2'}
        return action
