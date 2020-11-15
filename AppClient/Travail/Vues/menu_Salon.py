import PyInquirer as inquirer
from Vues.abstractView import AbstractView
import Vues.menu_Jouer as Play

from printFunctions import timePrint as print
import requests
import json
from tabulate import tabulate
import time

from Player.PlayerClass import Player


class Salon(AbstractView):
    def __init__(self, pseudo, id_salle, jeu, est_chef):
        self.pseudo = pseudo.lower()
        self.game = jeu.lower()
        self.id_salle = id_salle
        self.est_chef = est_chef

        self.question = [
            {
                'type' : 'list',
                'name' : 'Salon_accueil',
                'message' : "Que souhaitez-vous faire ?",
                          'choices' : [
                              'Voir les membres de la salle',
                              'Modifier les paramètres de la salle',
                              "Être prêt",
                              inquirer.Separator(),
                              'Quitter la salle',
                          ]
            },
        ]

    def display_info(self):
        print(f"Vous êtes dans le salon de la salle {self.id_salle}.")

    def make_choice(self):
        while True:
            self.reponse = inquirer.prompt(self.question)
            if self.reponse["Salon_accueil"] == 'Voir les membres de la salle':
                return self.menu_voir_membres_salle()
            elif self.reponse["Salon_accueil"] == 'Modifier les paramètres de la salle':
                import Vues.menu_Parametres as MPara
                MParametre1 = MPara.Menu_Parametre(self.pseudo, self.id_salle, self.game,  self.est_chef)
                return MParametre1.make_choice()
            elif self.reponse["Salon_accueil"] == "Être prêt":
                self.choix_couleur(self.get_liste_couleurs_dispo())
                if self.est_chef == True:
                    self.etre_pret_chef()
                else:
                    self.etre_pret()
                return self.jouer()
            else: #'Quitter la salle'
                return self.menu_retour()
            break

    def menu_retour(self):
        self.question_retour = [
            {
                'type' : 'list',
                'name' : 'salon_retour',
                'message' : f"Vous allez retourner au menu précédant. Vous allez donc quitter la salle {self.id_salle}. Etes vous sur? ",
                          'choices' : [
                              "Oui",
                              "Non"
                          ]
            },
        ]
        while True:
            self.reponse_retour = inquirer.prompt(self.question_retour)
            if self.reponse_retour["salon_retour"] == "Oui":
                Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
                Resultat = Player1.quitter_salle()
                self.print_message(Resultat)

                if Resultat["Statut"]:
                    import Vues.menu_Choix_Mode_Jeu as MCMJ
                    Retour = MCMJ.Menu_Choix_Mode_Jeu_Connecte(pseudo=self.pseudo, jeu=self.game)
                    Retour.display_info()
                    return Retour.make_choice()
                elif not Resultat["Statut"]:
                    return self.make_choice()
                else:
                    print("Erreur non prévue")
                    return self.make_choice()
            else: #'non'
                return self.make_choice()


    def menu_voir_membres_salle(self):
        from Player.PlayerClass import Player
        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.voir_membres_salle()
        self.print_message(Resultat)
        if Resultat["Statut"] == True:
            self.print_membres_salle(Resultat["liste_membres"])
            return(self.make_choice())
        elif Resultat["Statut"] == False:
            return (self.make_choice())
        else:
            print("Erreur non prévue")
            return (self.make_choice())

    def print_membres_salle(self, liste_membres):
        print("\n" + tabulate(liste_membres, headers=["Pseudo"], tablefmt="grid"))

    def get_liste_couleurs_dispo(self):
        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.get_liste_couleurs_dispos()
        self.print_message(Resultat)

        if Resultat["Statut"]:
            return Resultat["liste_couleurs_dispos"]
        else:
            return self.make_choice()

    def choix_couleur(self, liste_couleurs_dispos):
        answer = inquirer.prompt([
            {
                'type': 'list',
                'name': 'couleur',
                'message': 'Quelle couleur voulez vous choisir pour jouer?',
                'choices': liste_couleurs_dispos,
            },
        ])
        couleur_choisie = answer['couleur']

        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.choix_couleur(couleur_choisie)
        self.print_message(Resultat)

        if not Resultat["Statut"]:
            liste_couleurs_dispos = self.get_liste_couleurs_dispo()
            return self.choix_couleur(liste_couleurs_dispos)
        else:
            #la couleur est choisie et notée dans la db. On peut passer
            pass

    def etre_pret(self):
        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.etre_pret()
        self.print_message(Resultat)

        if Resultat["Statut"]: #ca c'est bien passé
            pass
        else: #un bug est survenu
            return self.make_choice()

    def is_everyone_ready(self):
        tout_le_monde_pret = False
        count = 1
        while not tout_le_monde_pret:
            count += 1
            Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
            Resultat = Player1.is_everyone_ready()
            if Resultat["Statut"]:
                self.print_message(Resultat)
                tout_le_monde_pret = True
            else:
                if count == 1:
                    self.print_message(Resultat)
                time.sleep(0.5)
        return tout_le_monde_pret

    def etre_pret_chef(self):
        self.etre_pret()
        everyone_ready = False
        while not everyone_ready:
            if self.is_everyone_ready():
                everyone_ready = True

        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.lancer_partie()
        self.print_message(Resultat)

    def jouer(self):
        monTour = False
        while not monTour:
            monTour = self.demander_tour()
            time.sleep(0.5)
        Action = Play.Jouer(self.pseudo, self.id_salle, self.game,  self.est_chef)
        Action.jouer()
        return self.passer_tour()

    def demander_tour(self):
        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.demander_tour()
        self.print_message(Resultat)
        if Resultat["Statut"]:
            #c'est votre tour de jouer
            pass
        elif not Resultat["Statut"]:
            pass
        else:
            print("erreur dans menu_salon.demander_tour")
        return Resultat["Statut"]

    def passer_tour(self):
        Player1 = Player(self.pseudo, self.game, self.id_salle, self.est_chef)
        Resultat = Player1.passer_tour()
        self.print_message(Resultat)
        if Resultat["Statut"]:
            return self.jouer()
        else:
            print(f"erreur dans le passage de tour pour le joueur {self.pseudo}")
