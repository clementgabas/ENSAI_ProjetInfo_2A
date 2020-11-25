import AppServeur.DAO.gestionUser as DAOuser
import AppServeur.DAO.gestionScores as DAOscore
import AppServeur.DAO.gestionClassement as DAOcl
import secrets
import unittest


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

