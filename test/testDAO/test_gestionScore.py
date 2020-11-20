import AppServeur.DAO.gestionUser as DAOuser
import AppServeur.DAO.gestionScores as DAOscore
import unittest
import secrets

class Test_gestion_Score(unittest.TestCase):
    def test_update_nb_parties_jouees(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        try:
            # on appel la fonction à tester
            DAOuser.add_user(username, pseudo, hpassword)
        except:
            return "erreur dans la méthode gestionUser.add_user"

        try:
            tester = DAOscore.DAOscore.get_nb_parties_jouees(pseudo, "p4")
        except:
            return "erreur dans la méthode gestionScores.get_nb_parties_jouees()"

        self.assertIs(tester, 0)

        #on appel la fonction à tester
        DAOscore.update_nb_parties_jouees(pseudo, "p4", 1)

        try:
            tester = DAOscore.DAOscore.get_nb_parties_jouees(pseudo, "p4")
        except:
            return "erreur dans la méthode gestionScores.get_nb_parties_jouees()"

        self.assertIs(tester, 1)

        try:
            DAOuser.delete_user_pseudo(pseudo)
        except:
            print("attention : utilisateur test non supprimé dans la table Utilisateur")

    def test_update_nb_parties_gagnees(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        try:
            # on appel la fonction à tester
            DAOuser.add_user(username, pseudo, hpassword)
        except:
            return "erreur dans la méthode gestionUser.add_user"
        try:
            tester = DAOscore.get_nb_parties_gagnees(pseudo, "p4")
        except:
            return "erreur dans la méthode gestionAmis.get_nb_parties-gagnees"

        self.assertIs(tester, 0)

        # on appel la fonction à tester
        DAOscore.update_nb_parties_gagnees(pseudo, "p4", 1)

        try:
           tester = DAOscore.get_nb_parties_gagnees(pseudo, "p4")
        except:
            return "erreur dans la méthode gestionAmis.get_nb_parties-gagnees"
        self.assertIs(tester, 1)

        try:
            DAOuser.delete_user_pseudo(pseudo)
        except:
            print("attention : utilisateur test non supprimé dans la table Utilisateur")

    def test_get_nb_parties_jouees(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        try:
            # on appel la fonction à tester
            DAOuser.add_user(username, pseudo, hpassword)
        except:
            return "erreur dans la méthode gestionUser.add_user"

        # on appel la fonction à tester
        tester = DAOscore.get_nb_parties_jouees(pseudo, "p4")

        self.assertIs(tester, 0)

        try:
            DAOscore.update_nb_parties_jouees(pseudo, "p4", 1)
        except:
            return "Erreur dans l'appel de la méthode gestionScores.get_nb_parties_gagnees"

        tester = DAOscore.get_nb_parties_jouees(pseudo, "p4")

        self.assertIs(tester, 1)

        try:
            DAOuser.delete_user_pseudo(pseudo)
        except:
            print("attention : utilisateur test non supprimé dans la table Utilisateur")

    def test_get_nb_parties_gagnees(self):
        def test_get_nb_parties_jouees(self):
            # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
            username = secrets.token_hex(10)
            pseudo = secrets.token_hex(10)
            hpassword = secrets.token_hex(10)

            try:
                # on appel la fonction à tester
                DAOuser.add_user(username, pseudo, hpassword)
            except:
                return "erreur dans la méthode gestionUser.add_user"

            # on appel la fonction à tester
            tester = DAOscore.get_nb_parties_gagnees(pseudo, "p4")

            self.assertIs(tester, 0)

            try:
                DAOscore.update_nb_parties_gagnees(pseudo, "p4", 1)
            except:
                return "Erreur dans l'appel de la méthode gestionScores.get_nb_parties_gagnees"

            tester = DAOscore.get_nb_parties_gagnees(pseudo, "p4")

            self.assertIs(tester, 1)

            try:
                DAOuser.delete_user_pseudo(pseudo)
            except:
                print("attention : utilisateur test non supprimé dans la table Utilisateur")