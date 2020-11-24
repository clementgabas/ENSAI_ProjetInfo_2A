import requests
import json
from Player.UserClass import User
from Player.RequestsTools.AddressTools import get_absolute_address, make_address
absolute_address = get_absolute_address()


class Player(User):
    """
    Classe qui gère la partie "joueur" de l'utilisateur, qui débute à la création d'une salle est fini avec la fin de partie.
    Cette classe hérite de la classe Userbase.
    """

    def __init__(self, pseudo, jeu, id_salle, chef_salle, ami_anonyme="ami"):
        """
        Fonction init qui définit:
            pseudo : str
                Le pseudo de l'utilisateur
            id_salle : int
                identifiant de la salle qui est aussi celui de la partie.
            est_chef : bool
                Booléen qui définit si oui ou non l'utilisateur est chef de partie
            ami_anonyme :str
                attribut qui définit si la partie créée est pour jouer uniquement entre amis ou non.

        """
        self.pseudo = pseudo
        self.id_salle = id_salle
        self.est_chef = chef_salle
        self.jeu = jeu
        self.ami_anonyme = ami_anonyme


    def is_salle_anonyme_available(self):
        """
        Procédure qui vérifie si il existe une salle ouverte aux anonymes est encore disponible.

        Returns
        -------
        Resultat : dict
            Dictionnaire contenant la réussite ou non de cette vérification et le message associé.
                Si il existe une salle est qu'il y a encore de la place : le statut sera le booléen True.

                Si il existe de telles salle mais quelles sont pleinnes : le statut sera le booléen False

                Si une erreur a lieu pendant la procédure, le statut sera false et le message associé determinera
                la raison de l'erreur


        """
        relative_address = "/home/game/room/anonyme"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo, 'game': self.jeu}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200: #une salle anonyme est dispo
            Resultat = self.update_resultat(True)
            Resultat["id_salle"] = res.json()['id_salle']
        elif res.status_code == 404:
            Resultat = self.update_resultat(False)
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def creer_salle(self):
        """
        Fonction qui assure la création d'une salle pour jouer un un jeu.

        Returns
        ------
        Resultat : dict
            Dictionnaire contenant la réussite ou non de la création d'une salle et le message associé

                Si la partie a bien été créée, le statut sera le booléen True, deux possiblités permettent cette option :
                    1- création d'une partie entre amis

                    2- création d'une parite entre anonyme.

                    le dictionnaire renverra aussi l'identifiant de la salle.

                Si la partie n'a pas été crée due à differentes erreurs, le statut sera le booléen False

        """
        relative_address = "/home/game/room"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo_chef_salle': self.pseudo, 'game': self.jeu, "ami_anonyme": self.ami_anonyme}
        res = requests.post(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            if self.ami_anonyme == "ami":
                Resultat = self.update_resultat(True, f"Une salle (numéro {res.json()['id_salle']}) vient d'être créée. Vos amis peuvent la rejoindre via son numéro.")
            else:
                Resultat = self.update_resultat(True)
            Resultat["id_salle"] = res.json()['id_salle']
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def rejoindre_salle(self,id_salle):
        """
        Fonction qui gère le fait qu'un utilisateur rejoint une salle d'un amis.

        Parameters
        -------
        id_salle: int
             identifiant de la salle que veut rejoindre l'utilisateur.

        Returns
        -------
        Resultat : dict
            Dictionnaire contenant la réussite ou non que l'utilisateur ait rejoint la partie , et le message associé.
                Si l'utilisateur a réussi a rejoindre la salle, le statut sera le booléen True et
                le dictionnaire renverra aussi l'identifiant de la salle.

                Si l'utilisateur ne peut rejoindre la salle le statut sera le booléen False et le message associé
                justifiera la cause pouvant être : Une erreur quelconque, le fait que la partie soit déja pleine
                ou bien que cette partie n'existe pas.
        """
        relative_address = "/home/game/room"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo, 'id_salle': id_salle, 'jeu':self.jeu}
        res = requests.put(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True, f"Vous avez bien été ajouté à la salle {id_salle}.")
            Resultat["id_salle"] = id_salle
        elif res.status_code == 401:
            Resultat = self.update_resultat(False, f"Vous ne pouvez pas rejoindre la salle {id_salle} car elle est déjà pleine.")
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "La salle demandée n'existe pas.")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def rejoindre_salle_anonyme(self):
        """
        Fonction qui gère le fait qu'un utilisateur rejoint une salle d'anonyme.

        Returns
        -------
        Resultat : dict
            Dictionnaire contenant la réussite ou non que l'utilisateur ait rejoint une partie , et le message associé.
                Si l'utilisateur a réussi a rejoindre une salle, le statut sera le booléen True.

                Si l'utilisateur ne peut rejoindre la salle le statut sera le booléen False et le message associé
                justifiera la cause pouvant être : Une erreur quelconque, le fait que la partie soit déja pleine
                ou qu'aucune salle ne soit disponible.
        """
        relative_address = "/home/game/room/anonyme"
        adresse = make_address(absolute_address, relative_address)

        
        res = requests.put(adresse, data=json.dumps(dataPost)) #on recupere le id_salle
        dataPost = {'pseudo': self.pseudo, 'id_salle': res["id_salle"], 'jeu':self.jeu}

        if res.status_code == 200:
            Resultat = self.update_resultat(True, f"Vous avez bien été ajouté à la salle anonyme {id_salle}.")
            Resultat["id_salle"] = id_salle
        elif res.status_code == 401:
            Resultat = self.update_resultat(False, f"La salle anonyme {id_salle} est pleine") #surbooking
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "Aucune salle anonyme de disponible")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def voir_membres_salle(self):
        """
        Fonction qui permet de renvoyer les memebres présents dans une même salle.

        Returns
        -------
        Resultats : dict
            Dictionnaire contenant la réussite ou non d'affichage des membres et le message associé.
                Si l'affichage a bien lieu, le statut sera le booléen True et le dictionnaire renverra aussi
                la liste des membres de la salle.

                Sinon, le statut sera le booléen False et le message associé justifiera l'erreur.

        """
        relative_address = "/home/game/room"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'id_salle': self.id_salle}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["liste_membres"] = res.json()["liste_membres"]
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.voir_membres_salle")
        return Resultat

    def quitter_salle(self):
        """
        Fonction qui permet à un utilisateur de quitter une salle.

        Returns
        -------
        Resultat : dict
            Dictionnaire contenant la réussite ou non d'abandon de la salle et le message associé
                Si l'abandon a bien eu lieu, le statut sera le booléen True.

                Si l'abandon ne peut avoir lieu, car l'utilisateur est chef de salle par exemple,
                le statut sera le booléen False et la cause sera justifée dans le message associé
        """
        relative_address = "/home/game/room"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {"pseudo": self.pseudo, "id_salle": self.id_salle, "est_chef_salle": self.est_chef}
        res = requests.delete(adresse, data=json.dumps(dataPost))
        if res.status_code == 401:
            Resultat = self.update_resultat(False,"Vous êtes le chef de la salle! Vous ne pouvez pas la quitter tant qu'un autre utilisateur s'y trouve encore. Un capitaine quitte toujours son navire en dernier n'est-ce pas?")
        elif res.status_code == 200:
            Resultat = self.update_resultat(True, f"Vous avez quitté la salle {self.id_salle}")
        return Resultat

    def get_liste_couleurs_dispos(self):
        """
        Fonction qui gère l'affichage de la liste des couleurs disponibles.

        Returns
        -------
        Resultat: dict
            Dictionnaire contenant la réussite ou non d'affichage de cette liste et le message associé
                Si l'affichage a bien lieu, le statut sera le booléen True et le dictionnaire renverra aussi
                la liste des couleurs disponibles.

                Sinon, le statut sera le booléen False, la cause justifiée dans le message associé peut être:
                une erreur quelconque ou le fait que l'utilisateur soit seul dans la salle.

        """
        relative_address = "/home/game/room/colors"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'id_salle':self.id_salle}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["liste_couleurs_dispos"] = res.json()["liste_couleurs_dispos"]
        elif res.status_code == 403:
            Resultat = self.update_resultat(False, "Vous ne pouvez pas être pret car vous êtes seuls dans la salle. Il faut être au moins 2.")
        else:
            Resultat = self.update_resultat(False, "erreur ndas PlayerClass.get_liste_couleurs_dispos")
        return Resultat

    def choix_couleur(self, couleur_choisie):
        """
        Fonction qui gère le choix de la couleur séléctionnée par un utilisateur.

        Parameters
        ------
        couleur_choisie: str
            Couleur choisie par l'utilisateur

        Returns
        ------
        Resultat: dict
            Dictionnaire contenant la réussite ou non de cette sélection, et le message associé
                Si la sélection a bien eu lieu, le statut sera le booléen True.

                Sinon, le statut sera le booléen False, le message associé justifiera la cause, pouvant être :
                    une erreur quelconque ou le fait que la couleur ait été choisie par quelqu'un d'autre.
        """
        relative_address = "/home/game/room/colors"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'id_salle':self.id_salle, 'pseudo':self.pseudo, 'couleur':couleur_choisie}
        res = requests.post(adresse, data=json.dumps(dataPost))

        if res.status_code == 409: #la couleur a été choisie entre temps
            Resultat = self.update_resultat(False, "La couleur demandée a été choisie entre temps par un autre utilisateur. Veuillez réessayer svp.")
        elif res.status_code == 200:
            Resultat = self.update_resultat(True)
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.choix_couleur")
        return Resultat

    def etre_pret(self):
        """
         Fonction qui permet à un utilisateur se mettre prêt à débuter une partie.

         Returns
         ------
         Resultat: dict
             Dictionnaire contenant la réussite ou non de l'actualisation du statut de l'utilisateur et le message associé
                 Si l'actualisation a bien eu lieu, le statut sera le booléen True.

                 Sinon, une erreur est relevée, le statut sera le booléen False. Le message associé justifiera
                 la cause de l'erreur.
         """
        relative_address = "/home/game/room/turns"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo':self.pseudo,'id_salle':self.id_salle, 'est_chef':self.est_chef, 'jeu': self.jeu}
        res = requests.post(adresse, data=json.dumps(dataPost))
        if res.status_code == 200:
            Resultat = self.update_resultat(True, "Vous êtes prêts!")
        else:
            Resultat = self.update_resultat(False, "erreur ndas PlayerClass.choix_couleur")
        return Resultat

    def is_everyone_ready(self):
        """
        Fonction qui gère la verification du status de tous les utilisateurs. Ansi elle s'assure que tous les utilisateurs
        sont prêts à jouer

        Returns
        -------
        Resultat: dict
            Dictionnaire contenant la réussite ou non de la véfication i.e si tout le monde est prêt et le message associé
             Si tout le monde est prêt, le statut sera le booléen True.
             Sinon, le statut sera le booléen False.
        """
        relative_address = "/home/game/room/launch"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo, 'id_salle': self.id_salle, 'est_chef': self.est_chef}
        # -- on requete pour savoir si tout le monde est pret dans la salle
        res = requests.get(adresse, data=json.dumps(dataPost))
        # -- si on récupère un "tout le monde est pret", on lance la partie
        if res.status_code == 200:
            Resultat = self.update_resultat(True, "Tout le monde est prêt dans la salle. La partie va se lancer.")
        else:
            Resultat = self.update_resultat(False, "En attente que tous les participants soient prêts pour lancer la partie.")
        return Resultat

    def lancer_partie(self):
        """
        Fonction qui gère le lancement d'une partie.

        Returns
        -------
        Resultat: dict
            Dictionnaire contenant la réussite ou non de ce lancement et le message associé.
                Si la partie s'est bien lancée, le statut sera le booléen True.

                Sinon, le statut sera le booléen False. La cause sera justifiée dans le message associé
        """
        relative_address = "/home/game/room/launch"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'id_salle': self.id_salle}
        res = requests.post(adresse, data=json.dumps(dataPost))  # dao pour modifier dans la table Partie le statut à en cours
        if res.status_code == 200:
            # la partie est lancée, on peut requeter pour savoir si c'est son tour
            Resultat = self.update_resultat(True)
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.lancer_partie")
        return Resultat

    def passer_tour(self):
        """
        Fonction qui gère le passage de tour d'un utilisateur.

        Returns
        ------
        Resultat: dict
            Dictionnaire contenant la réussite ou non de ce passage de tour et le message associé
                Si l'action est bien éffectuée, le statut sera le booléen True.

                Sinon, le statut sera le booléen False.
        """
        relative_address = "/home/game/room/turns"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo, 'id_salle': self.id_salle}
        res = requests.put(adresse, data=json.dumps(dataPost))
        if res.status_code == 200:
            Resultat = self.update_resultat(True, "Vous passez votre tour.")
        else:
            Resultat = self.update_resultat(False)
        return Resultat

    def demander_tour(self):
        """
         Fonction qui gère la demande de tour, ainsi l'interrogateur va savoir si c'est à lui de jouer ou non.

         Returns
         -------
         Resultat: dict
             Dictionnaire contenant la réponse, positive ou non, de cette demande, et le message associé.
                 Si c'est au tour de l'utilisateur et qu'il peut jouer,  le statut sera le booléen True.

                 Deplus, le statut sera le booléen False si :
                     -C'est au tour du joueur, mais il ne peut jouer son tour.

                     -Ce n'est pas son tour.

                     -Il y a une erreur quelconque.
                 la cause sera justifiée dans le message associée
         """
        relative_address = "/home/game/room/turns"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo, 'id_salle': self.id_salle}
        res = requests.get(adresse, data=json.dumps(dataPost))
        if res.status_code == 200:
            Resultat = self.update_resultat(True, "C'est votre tour de jouer")
        elif res.status_code == 403:
            Resultat = self.update_resultat(False, "C'était votre tour de jouer mais vous deviez le passer.")
        elif res.status_code == 449:
            Resultat = self.update_resultat(False, "Ce n'est pas votre tour de jouer")
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.demander_tour")
        return Resultat

    def demander_grille(self):
        """
        Fonction qui gère une demande d'affichage de la grille de jeu.

        Returns
        -------
        Resultat: dict
            Dictionnaire contenant la réponse, positive ou non, d'affichage de cette grille ainsi que le message associé
                Si la demande est bien traitée, le statut sera le booléen True et le dictionnaire renverra aussi
                la grille et la liste des couleurs sélectionné ardonnée.

                Sinon  le statut sera le booléen False.
        """
        relative_address = "/home/game/room/grid"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'id_partie': self.id_salle, 'jeu': self.jeu.lower()}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["Grille"] = res.json()["grid"]
            Resultat["liste_couleur_ordonnee"] = res.json()["liste_couleur_ordonnee"]
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.demander_grille")
        return Resultat

    def jouer_son_tour(self, action):
        """
        Fonction qui gère la demande de jouer son tour, avec une action particuliere, pour un utilisateur

        Parameters
        ------
        action :
         action en entrée, lancé de dé pour le jeu de l'oie et choix de colonne pour le P4.

        Returns
        -------
        Resultat: dict
            Dictionnaire contenant la réponse, positive ou non, d'execution de cette commande ainsi que le message associé
                Si la demande est bien traitée, le statut sera le booléen True.

                Sinon, le statut sera le booléen False, le message associé en précisera la raison.
        """
        relative_address = "/home/game/room/grid"
        adresse = make_address(absolute_address, relative_address)

        coup = {'pseudo': self.pseudo, 'id_partie': self.id_salle, 'position': action['action'], 'jeu': self.jeu}
        res = requests.post(adresse, data=json.dumps(coup))

        if res.status_code == 200:
            Resultat = self.update_resultat(True, "Le coup a bien été joué.")
        elif res.status_code == 403:
            Resultat = self.update_resultat(False, res.json()["message"])
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.jouer_son_tour")
        return Resultat

    def demander_si_vainqueur(self):
        """
        Fonction qui vérifie si l'utilisateur remporte la partie.

        Returns
        -------
        Resultat: dict
            Dictionnaire contenant la réponse, positive ou non, d'execution de cette vérification ainsi que le message associé.
                Si l'utilisateur a remporté la partie, le statut sera le booléen True.

            Sinon, le statut sera le booléen False dans les cas suivant:
                -Le joueur n'a pas remporté la partie

                -Une erreur quelconque a eu lieu, dans ce cas, le message associé le précisera.
        """
        relative_address = "/home/game/room/grid"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'id_partie': self.id_salle, 'jeu': self.jeu.lower()}
        res = requests.put(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            winner_bool = res.json()["is_winner"]
            if winner_bool:
                Resultat = self.update_resultat(True, "Vous avez gagné la partie")
            else:
                Resultat = self.update_resultat(False)
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.jouer_son_tour")
        return Resultat

    def gestion_fin_partie(self, self_win):
        """
        Fonction qui gère la fin de la partie ou ce trouve l'utilisateur, i.e qui mais à jour ses statistiques personnelles

        Parameters
        ------
        self_win: bool
            Parametre qui définit si l'utilisateur est le vainqueur de la partie.

        Returns
        -------
        Resultat: dict
            Dictionnaire contenant la réponse, positive ou non, d'execution de cette commande ainsi que le message associé
                Si les statistiques ont été mises à jour, le statut sera le booléen True.

                Sinon, le statut sera le booléen False et le message associcé précisera la cause.
        """
        #-- fonction qui nous retire de la table participation pour cette partie,
        # qui update si on a gagné notre nb de parties gagnees dans la table score
        # et qui update notre score (si la partie est anonyme)
        relative_address = "/home/game/room/end"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo, 'id_partie': self.id_salle, 'jeu': self.jeu.lower(), 'win_bool': self_win, "ami_anonyme": self.ami_anonyme}
        res = requests.put(adresse, data=json.dumps(dataPost))

        if res.status_code==200:
            Resultat = self.update_resultat(True, "Vos statistiques ont été mises à jour")
        else:
            Resultat = self.update_resultat(False, "erreur dans PlayerClass.gestion_fin_partie")
        return Resultat