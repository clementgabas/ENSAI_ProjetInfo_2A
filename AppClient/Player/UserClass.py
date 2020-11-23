import requests
import json
from travailMDP.testmdp import anti_SQl_injection
from RequestsTools.AddressTools import get_absolute_address, make_address

from Player.abstractUser import AbstractUser

absolute_address = get_absolute_address()

class User(AbstractUser):
    """
    Classe qui hérite de la classe abstraite AbstactUser et qui gere la partie menu d'un utilisateur connecté.
    """

    def __init__(self, pseudo):
        """
        Fonction init qui définie:
            pseudo : str
                Le pseudo de l'utilisateur
        """
        self.pseudo = pseudo

    def deconnexion(self):
        """
        Foction qui gère la déconnexion d'un utilisateur.

        :return
        -------
        Resultat: dict
            Dictionnaire contenant la réponse, positive ou non, d'execution de cette commande ainsi que le message associé
                Si l'utilisateur c'est déconnecté normalement, le statut sera le booléen True.

                Sinon, le statut sera le booléen False, avec la raison de cette echec dans le message associé.

        """
        relative_address = "/home/deconnexion"
        adresse = make_address(absolute_address, relative_address)


        dataPost = {'pseudo': self.pseudo}
        # -- connexion à l'API
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat


    def ajout_ami(self,pseudo_ami):
        """
         Foction qui gère l'ajout d'un autre utilisateur dans la liste d'amis.

        :param
        -----
         pseudo_ami: str
            Pseudo de l'utilisateur à ajouter en ami.
        :return
        -----
        Resultat: dict
             Dictionnaire contenant la réponse, positive ou non, d'execution de cette commande ainsi que le message associé
                Si l'ajout s'est fait sans accrocs, le statut sera le booléen True.

                A l'inverse, le statut sera le booléen False si les erreurs suivantes, que précisera le message associé, arrivent :
                    -Le pseudo n'existe pas.

                    -Le lien d'amitié existe déja.

                    -Des erreurs quelconques ont lieu.

        """
        relative_address = "/home/main/profil/friends"
        adresse = make_address(absolute_address, relative_address)

        if pseudo_ami == self.pseudo:
            Resultat = self.update_resultat(False, "Vous ne pouvez pas vous ajouter vous même comme ami.")
            return Resultat

        dataPost = {'pseudo': self.pseudo, 'pseudo_ami': pseudo_ami}
        # -- connexion à l'API
        res = requests.post(adresse, data=json.dumps(dataPost))
        if res.status_code == 404:
            Resultat = self.update_resultat(False, f"Le pseudo a ajouter à votre liste d'ami ({pseudo_ami}) n'existe pas.")
        elif res.status_code == 208:
            Resultat = self.update_resultat(False, f"Le lien d'amitié avec {pseudo_ami} existe déjà.")
        elif res.status_code == 200:
            Resultat = self.update_resultat(True, f"Votre nouvel ami ({pseudo_ami}) a bien été ajouté à votre liste d'amis.")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def supp_ami(self,pseudo_ami):
        """
         Foction qui gère la suppression d'un autre utilisateur dans la liste d'amis.

        :param
        -----
         pseudo_ami: str
            Pseudo de l'utilisateur à spprimer de la liste d'amis.
        :return
        -----
        Resultat: dict
             Dictionnaire contenant la réponse, positive ou non, d'execution de cette commande ainsi que le message associé
                Si la suppression s'est faite sans accrocs, le statut sera le booléen True.

                A l'inverse, le statut sera le booléen False si les erreurs suivantes, que précisera le message associé, arrivent :
                    -Le pseudo n'existe pas.

                    -Le lien d'amitié n'existe pas.

                    -Des erreurs quelconques ont lieu.

        """
        relative_address = "/home/main/profil/friends"
        adresse = make_address(absolute_address, relative_address)

        if pseudo_ami == self.pseudo:
            Resultat = self.update_resultat(False, "Vous ne pouvez pas vous supprimer vous même comme ami.")
            return Resultat

        dataPost = {'pseudo': self.pseudo, 'pseudo_ami': pseudo_ami}
        # -- connexion à l'API
        res = requests.delete(adresse, data=json.dumps(dataPost))
        if res.status_code == 404:
            Resultat = self.update_resultat(False, f"Le pseudo à supprimer de votre liste d'ami ({pseudo_ami}) n'existe pas.")
        elif res.status_code == 208:
            Resultat = self.update_resultat(False, f"Le lien d'amitié avec {pseudo_ami} n'existe pas.")
        elif res.status_code == 200:
            Resultat = self.update_resultat(True, f"Votre ancien ami ({pseudo_ami}) a bien été supprimé de votre liste d'amis.")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def afficher_amis(self):
        """
        Fonction qui gère la demande d'affichage de la liste d'amis de l'utilisateur.

        :return
        ------
        Resultat: dict
             Dictionnaire contenant la réponse, positive ou non, d'execution de cette commande ainsi que le message associé
                Si le traitement de la demande d'affichage est faite sans accroc, le statut sera le booléen True
                et le dictionnaire renverra aussi cette liste d'amis.

                Sinon, le statut sera le booléen False, avec la raison de cette echec dans le message associé.
        """
        relative_address = "/home/main/profil/friends"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo}
        # -- connexion à l'API
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["Liste_amis"] = res.json()["liste_amis"]
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def modifier_mdp(self,old_mdp,new_mdp1,new_mdp2):
        """
        Fonction qui gère la modification du mot de passe d'un utilisateur

        :param
        ------
        old_mdp: str
            Ancien mot de passe que l'utilisateur souhaite modifier.
        new_mdp1: str
            Mot de passe qu'il veut avoir
        new_mdp2: str
            confirmation de ce mot de passe
        :return
        ------
        Resultat: dict
             Dictionnaire contenant la réponse, positive ou non, d'execution de cette commande ainsi que le message associé
                Si la modification de mot de passe est faite sans accrocs, le statut sera le booléen True.

                A l'inverse, le statut sera le booléen False si les erreurs suivantes, que précisera le message associé, arrivent :
                    -Les deux nouveaux mots de passes ne correspondent pas.

                    -L'ancien mot de passe fournit ne correspond pas.

                    -Des erreurs quelconques ont lieu.
        """
        relative_address = "/home/main/profil/user/password"
        adresse = make_address(absolute_address, relative_address)

        if new_mdp1 != new_mdp2:
            Resultat = self.update_resultat(False, "Les deux nouveaux mots de passes ne correspondent pas.")
            return Resultat
        if new_mdp1 == "":
            Resultat = self.update_resultat(False, "Veuillez fournir un nouveau mot de passe svp.")
            return Resultat
        if not anti_SQl_injection(new_mdp1):
            Resultat = self.update_resultat(False, "Pour des raisons de sécurité, votre demande ne peut aboutir.")
            return Resultat

        # if not is_mdp_legal(new_mdp1):
        # return self.echec_modif_mdp()

        dataPost = {'pseudo': self.pseudo, 'old_password': old_mdp, 'new_password': new_mdp1}
        res = requests.put(adresse, data=json.dumps(dataPost))

        if res.status_code == 401:
            Resultat = self.update_resultat(False, "Le mot de passe fournit ne correspond pas.")
        elif res.status_code == 200:
            Resultat = self.update_resultat(True, "Le mot de passe a bien été modifié.")
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat


    def modifier_pseudo(self,new_pseudo):
        """
        Fonction qui gère la modification du pseudo d'un utilisateur

        :param
        ------
        new_pseudo: str
            Nouveau pseudo que l'utilisateur veut avoir
        :return
        ------
        Resultat: dict
             Dictionnaire contenant la réponse, positive ou non, d'execution de cette commande ainsi que le message associé
                Si la modification du pseudo est faite sans accrocs, le statut sera le booléen True.

                A l'inverse, le statut sera le booléen False si les erreurs suivantes, que précisera le message associé, arrivent :
                    -Le pseudo demandé est déjà utilisé.

                    -Le nouveau pseudo est identique à l'ancien.

                    -Des erreurs quelconques ont lieu.
        """
        relative_address = "/home/main/profil/user/pseudo"
        adresse = make_address(absolute_address, relative_address)

        if new_pseudo == self.pseudo:
            Resultat = self.update_resultat(False, "Le nouveau pseudo est identique à l'ancien.")
            return Resultat

        dataPost = {'old_pseudo': self.pseudo, 'new_pseudo': new_pseudo}
        res = requests.put(adresse, data=json.dumps(dataPost))

        if res.status_code == 409:
            Resultat = self.update_resultat(False, "Le pseudo demandé est déjà utilisé.")
        elif res.status_code == 200:
            self.pseudo = new_pseudo
            Resultat = self.update_resultat(True, "Le pseudo a été mis à jour.")
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def acceder_stats_perso(self):
        """
            Fonction qui gère la demande d'affichage des statistiques de l'utilisateur.

            :return
            ------
            Resultat: dict
                Dictionnaire contenant la réponse, positive ou non, d'execution de cette commande ainsi que le message associé
                    Si le traitement de la demande d'affichage est faite sans accroc, le statut sera le booléen True
                    et le dictionnaire renverra aussi ces statistiques.

                    Sinon, le statut sera le booléen False, avec la raison de cette echec dans le message associé.
            """
        relative_address = "/home/main/profil/user/stat"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo}
        # -- connexion à l'API
        res = requests.get(adresse, data=json.dumps(dataPost))
        if res.status_code == 200:
            stat_perso = res.json()['Statistiques personnelles']
            parties_g = stat_perso[0][1]
            parties_j = stat_perso[0][0]
            pourc_partie_g = 0
            if parties_j != 0:
                pourc_partie_g = parties_g / parties_j * 100
            stat_perso[0].append("{} %".format(pourc_partie_g))
            Resultat = self.update_resultat(True)
            Resultat["stat_perso"] = stat_perso
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def reinitialiser_stats_perso(self):
        """
        Fonction qui gère la demande de réinitialisation des statistiques de l'utilisateur.

        :return
        ------
        Resultat: dict
            Dictionnaire contenant la réponse, positive ou non, d'execution de cette commande ainsi que le message associé
                Si le traitement de la demande de réinitialisation est faite sans accroc, le statut sera le booléen True.

                Sinon, le statut sera le booléen False, avec la raison de cette echec dans le message associé.
        """
        relative_address = "/home/main/profil/user/stat"
        adresse = make_address(absolute_address, relative_address)

        dataPost = {'pseudo': self.pseudo}
        res = requests.put(adresse, data=json.dumps(dataPost))
        if res.status_code == 200:
            Resultat = self.update_resultat(True, "Vos statistiques ont bien été réinitialisées")
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def aff_classement_general(self):
        """
        Fonction qui gère la demande d'affichage du classement général de l'utilisateur.

        :return
        ------
        Resultat: dict
            Dictionnaire contenant la réponse, positive ou non, d'execution de cette commande ainsi que le message associé
                Si le traitement de la demande d'affichage est faite sans accroc, le statut sera le booléen True
                et le dictionnaire renverra aussi le classement général mondial et celui entre amis.

                Sinon, le statut sera le booléen False, avec la raison de cette echec dans le message associé.
        """
        relative_address = "/home/main/profil/classment/general"
        adresse = make_address(absolute_address, relative_address)

        # -- connexion à l'API
        dataPost = {"pseudo": self.pseudo}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["classement_general"] = res.json()["classement_general"]
            Resultat["classement_general_amis"] = res.json()["classement_general_amis"]
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def aff_classement_jeu_oie(self):
        """
        Fonction qui gère la demande d'affichage du classement du jeu de l'oie de l'utilisateur.

        :return
        ------
        Resultat: dict
            Dictionnaire contenant la réponse, positive ou non, d'execution de cette commande ainsi que le message associé
                Si le traitement de la demande d'affichage est faite sans accroc, le statut sera le booléen True
                et le dictionnaire renverra aussi le classement du jeu de l'oie mondial et celui entre amis.

                Sinon, le statut sera le booléen False, avec la raison de cette echec dans le message associé.
        """
        relative_address = "/home/main/profil/classment/jeu"
        adresse = make_address(absolute_address, relative_address)

        # -- connexion à l'API
        dataPost = {"nom_jeu": "Oie", "pseudo": self.pseudo}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["classement_jeu"] = res.json()["classement_jeu"]
            Resultat["classement_jeu_amis"] = res.json()["classement_jeu_amis"]
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def aff_classement_P4(self):
        """
        Fonction qui gère la demande d'affichage du classement du puissance 4 de l'utilisateur.

        :return
        ------
        Resultat: dict
            Dictionnaire contenant la réponse, positive ou non, d'execution de cette commande ainsi que le message associé
                Si le traitement de la demande d'affichage est faite sans accroc, le statut sera le booléen True
                et le dictionnaire renverra aussi le classement du puissance 4 mondial et celui entre amis.

                Sinon, le statut sera le booléen False, avec la raison de cette echec dans le message associé.
        """
        relative_address = "/home/main/profil/classment/jeu"
        adresse = make_address(absolute_address, relative_address)

        # -- connexion à l'API
        dataPost = {"nom_jeu": "P4", "pseudo": self.pseudo}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True)
            Resultat["classement_jeu"] = res.json()["classement_jeu"]
            Resultat["classement_jeu_amis"] = res.json()["classement_jeu_amis"]
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat