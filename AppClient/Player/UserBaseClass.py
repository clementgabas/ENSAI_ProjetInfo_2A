import requests
import json
from travailMDP.testmdp import anti_SQl_injection, hacherMotDePasse
from RequestsTools.AddressTools import get_absolute_address, make_address

from Player.abstractUser import AbstractUser


absolute_address = get_absolute_address()


class UserBase(AbstractUser):
    """
    Classe UserBase, classe qui hérite de la classe AbstractUser et qui représente la partie menu intiale,
    au lancement de l'application.
    """

    def creer_compte(self,identifiant,mdp,mdp2,pseudo):
        """
        Fonction qui a pour but de créer un compte pour un nouvel utilisateur.

        :param
        ------
        identifiant : str
            identifiant entré par le nouvel utilisateur.
        mdp : str
            Mot de passe entré par le nouvel utilisateur.
        mdp2 : str
            Confirmation du mot de passe entré par le nouvel utilisateur.
        pseudo : str
            Pseudo entré par le nouvel utilisateur.

        :return
        ------
        Resultat: dict
            Dictionnaire contenant la réussite ou non de création d'un utilisateur et le message associé
                Si la création de compte c'est faite sans accroc, le statut sera le booléen True.

                A l'inverse, le statut sera le booléen False si les erreurs suivantes, que précisera le message associé, arrivent :
                    -Les mot de passes ne correspondent pas.

                    -L'identifiant ou le mot de passe n'a pas été précisé.

                    -L'identifiant ou le pseudo est déjà utilisé.

                    -Des erreurs quelconques ont lieu.

        """
        relative_address = "/home/users"
        adresse = make_address(absolute_address, relative_address)

        if mdp != mdp2:
            Resultat = self.update_resultat(False, "Les mot de passes ne correspondent pas.")
            return Resultat
        if identifiant == "" or mdp == "":
            Resultat = self.update_resultat(False, "L'identifiant ou le mot de passe n'a pas été précisé.")
            return (Resultat)
        if not anti_SQl_injection(identifiant) or not anti_SQl_injection(mdp) or not anti_SQl_injection(pseudo):
            Resultat = self.update_resultat(False, "Pour des raisons de sécurité, votre demande ne peut aboutir.")
            return (Resultat)
            # if not is_mdp_legal(mdp):
            # return self.make_choice_retour()
        hmdp = hacherMotDePasse(mdp)

            # création du data pour le corps du post de l'api
        dataPost = {'username': identifiant, "hpassword": hmdp, "pseudo": pseudo}
            # -- connexion à l'API
        res = requests.post(adresse, data=json.dumps(dataPost))

        if res.status_code == 409:
            if "User" in res.json()['message']:
                Resultat = self.update_resultat(False, "L'identifiant est déjà utilisé par un autre membre.")
            elif "Pseudo" in res.json()['message']:
                Resultat = self.update_resultat(False, "Le pseudo est déjà utilisé par un autre membre")
            else:
                Resultat = self.update_resultat(False, "error in UserBase.creer_compte")
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        elif res.status_code == 200:
            Resultat = self.update_resultat(True, "Compte créé avec succès. Veuillez vous authentifiez svp")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat

    def connexion(self,identifiant,mdp,):
        """
        Fonction qui gère la connexion d'un utilisateur.

        :param
        ------
        identifiant : str
            identifiant entré par l'utilisateur
        mdp : str
            mot de passe entré par l'utilisateur

        :return
        -------
        Resultat: dict
            Dictionnaire contenant la réussite ou non de connexion d'un utilisateur et le message associé.
                Si la connexion se fait sans accrocs,  le statut sera le booléen True.

                A l'inverse, le statut sera le booléen False si les erreurs, que précisera le message associé, arrivent:
                    -L'identifiant ou le mot de passe n'a pas été précisé.

                    -Identifiant ou mot de passe incorrect.

                    -L'utilisateur est déjà connecté.

                    -Des erreurs quelconques ont lieu.

        """
        relative_address = "/home/connexion"
        adresse = make_address(absolute_address, relative_address)

        if identifiant == "" or mdp == "":
            Resultat = self.update_resultat(False, "L'identifiant ou le mot de passe n'a pas été précisé.")
            return Resultat
        if not anti_SQl_injection(identifiant) or not anti_SQl_injection(mdp):
            Resultat = self.update_resultat(False, "Pour des raisons de sécurité, votre demande ne peut aboutir.")
            return Resultat

        # -- connexion à l'API
        dataPost = {'username': identifiant, "password": mdp}
        res = requests.get(adresse, data=json.dumps(dataPost))

        if res.status_code == 200:
            Resultat = self.update_resultat(True, "Connection réussie")
            Resultat["pseudo"] = res.json()["pseudo"]
        elif res.status_code == 404:
            Resultat = self.update_resultat(False, "erreur, l'api n'a pas été trouvée")
        elif res.status_code == 500:
            Resultat = self.update_resultat(False, "erreur dans le code de l'api")
        elif res.status_code == 401:
            Resultat = self.update_resultat(False, "Identifiant ou mot de passe incorrect.")
        elif res.status_code == 403:
            Resultat = self.update_resultat(False, "L'utilisateur est déjà connecté")
        else:
            Resultat = self.update_resultat(False, "erreur non prévue : " + str(res.status_code))
        return Resultat
