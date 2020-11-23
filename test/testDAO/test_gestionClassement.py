import AppServeur.DAO.gestionUser as DAOuser
import AppServeur.DAO.gestionScores as DAOscore
import AppServeur.DAO.gestionClassement as DAOcl
import AppServeur.DAO.gestionAmis as DAOamis
import test.testDAO.script_delete_functions as dele
import unittest
import secrets


class Test_gestion_Score(unittest.TestCase):
    def test_afficher_classement_jeu(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        try:
            # on appel la fonction à tester
            DAOuser.add_user(username, pseudo, hpassword)
            DAOuser.add_user_score(pseudo)
        except:
            return "erreur dans la méthode gestionUser.add_user"

        tester1 = DAOcl.afficher_classement_jeu("P4", pseudo)
        try:
            DAOscore.update_nb_parties_gagnees(pseudo, "P4", 2)
        except:
            return "erreur dans gestionScores.update_nb_parties_gagnees"

        tester2 = DAOcl.afficher_classement_jeu("P4", pseudo)

        self.assertNotEqual(tester1, tester2)

    def test_afficher_classement_general(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        try:
            # on appel la fonction à tester
            DAOuser.add_user(username, pseudo, hpassword)
            DAOuser.add_user_score(pseudo)
        except:
            return "erreur dans la méthode gestionUser.add_user"

        tester1 = DAOcl.afficher_classement_general(pseudo)
        try:
            DAOscore.update_nb_parties_gagnees(pseudo, "P4", 55)
        except:
            return "erreur dans gestionScores.update_nb_parties_gagnees"

        tester2 = DAOcl.afficher_classement_general(pseudo)

        self.assertNotEqual(tester1, tester2)

    def test_afficher_classement_jeu_friends(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username1 = secrets.token_hex(10)
        pseudo1 = secrets.token_hex(10)
        hpassword1 = secrets.token_hex(10)

        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username2 = secrets.token_hex(10)
        pseudo2 = secrets.token_hex(10)
        hpassword2 = secrets.token_hex(10)

        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username3 = secrets.token_hex(10)
        pseudo3 = secrets.token_hex(10)
        hpassword3 = secrets.token_hex(10)

        try:
            # on appel la fonction à tester
            DAOuser.add_user(username1, pseudo1, hpassword1)
            DAOuser.add_user(username2, pseudo2, hpassword2)
            DAOuser.add_user(username3, pseudo3, hpassword3)

        except:
            return "erreur dans la méthode gestionUser.add_user"

        try:
            # on appel la fonction à tester
            DAOuser.add_user_score(pseudo1)
            DAOuser.add_user_score(pseudo2)
            DAOuser.add_user_score(pseudo3)
        except:
            return "erreur dans la méthode gestionUser.add_user_score"

        try:
            DAOamis.add_amitie(pseudo1, pseudo2)
            DAOamis.add_amitie(pseudo1, pseudo3)
        except:
            return "Erreur dans l'appel à gestionAmis.add_amitie, test avorté"
        try:
            DAOscore.update_nb_parties_gagnees(pseudo2, "P4", 2)
            DAOscore.update_nb_parties_gagnees(pseudo3, "P4", 1)

        except:
            return "erreur dans gestionScores.update_nb_parties_gagnees"

        tester1 = DAOcl.afficher_classement_jeu_friends("P4", pseudo1)

        try:
            DAOscore.update_nb_parties_gagnees(pseudo2, "P4", 1)
            DAOscore.update_nb_parties_gagnees(pseudo3, "P4", 2)

        except:
            return "erreur dans gestionScores.update_nb_parties_gagnees"

        tester2 = DAOcl.afficher_classement_jeu_friends("P4", pseudo1)

        self.assertNotEqual(tester1, tester2)

        try:
            DAOuser.delete_user_pseudo(pseudo1)
            DAOuser.delete_user_pseudo(pseudo2)
            DAOuser.delete_user_pseudo(pseudo3)
            dele.delete_pseudo_scores(pseudo1)
            dele.delete_pseudo_scores(pseudo2)
            dele.delete_pseudo_scores(pseudo3)
            DAOamis.sup_amitie(pseudo1)

        except:
            print("attention : utilisateur test non supprimé dans la table Utilisateur")

    def test_afficher_classement_jeu_friends(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username1 = secrets.token_hex(10)
        pseudo1 = secrets.token_hex(10)
        hpassword1 = secrets.token_hex(10)

        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username2 = secrets.token_hex(10)
        pseudo2 = secrets.token_hex(10)
        hpassword2 = secrets.token_hex(10)

        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username3 = secrets.token_hex(10)
        pseudo3 = secrets.token_hex(10)
        hpassword3 = secrets.token_hex(10)

        try:
            # on appel la fonction à tester
            DAOuser.add_user(username1, pseudo1, hpassword1)
            DAOuser.add_user(username2, pseudo2, hpassword2)
            DAOuser.add_user(username3, pseudo3, hpassword3)

        except:
            return "erreur dans la méthode gestionUser.add_user"

        try:
            # on appel la fonction à tester
            DAOuser.add_user_score(pseudo1)
            DAOuser.add_user_score(pseudo2)
            DAOuser.add_user_score(pseudo3)
        except:
            return "erreur dans la méthode gestionUser.add_user_score"

        try:
            DAOscore.update_nb_parties_gagnees(pseudo2, "P4", 2)
            DAOscore.update_nb_parties_gagnees(pseudo3, "P4", 1)

        except:
            return "erreur dans gestionScores.update_nb_parties_gagnees"

        tester1 = DAOcl.afficher_classement_jeu_friends("P4", pseudo1)

        try:
            DAOscore.update_nb_parties_gagnees(pseudo2, "P4", 1)
            DAOscore.update_nb_parties_gagnees(pseudo3, "P4", 2)

        except:
            return "erreur dans gestionScores.update_nb_parties_gagnees"

        tester2 = DAOcl.afficher_classement_jeu_friends("P4", pseudo1)

        self.assertNotEqual(tester1, tester2)

        try:
            DAOuser.delete_user_pseudo(pseudo1)
            DAOuser.delete_user_pseudo(pseudo2)
            DAOuser.delete_user_pseudo(pseudo3)

        except:
            print("attention : utilisateur test non supprimé dans la table Utilisateur")

