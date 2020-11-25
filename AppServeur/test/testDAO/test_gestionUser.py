import unittest
import secrets
import AppServeur.DAO.gestionUser as DAOuser



class Test_gestionUser(unittest.TestCase):
    """
    De manière générale, on commence par créer par un utilisateur
    temporaire en s'assurant qu'il n'existe pas déjà. On effectue
    ensuite le test désiré sur l'utilisateur temporaire. Enfin, on supprime
    l'utilisateur. Cette méthode n'est pas optimale, mais il est difficle
    de faire mieux avec les outils à disposition.
    """
    def test_add_user(self):

        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # on appel la fonction à tester
        DAOuser.add_user(username, pseudo, hpassword)

        # on vérifie que les infos de l'utilisateur sont bien dans la base de données
        self.assertTrue(DAOuser.does_pseudo_exist(pseudo))
        self.assertTrue(DAOuser.does_username_exist(username))

        DAOuser.delete_user_pseudo(pseudo)

    def test_does_username_exist(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)

        # recherche l'utilisateur test déjà créé dans la base de données
        tester_found = DAOuser.does_username_exist(username)
        # on vérifie que la fonction renvoie bien True, i.e. qu'elle a trouvé l'utilisateur dans la db
        self.assertTrue(tester_found)

        # on recherche un utilisateur inexistant (probabilité que le username généré par secrets.token_hex(10)existe déjà négligeable)
        tester_not_found = DAOuser.does_username_exist(secrets.token_hex(10))
        # on vérifie que la fonction renvoie bien False
        self.assertFalse(tester_not_found)

        DAOuser.delete_user_pseudo(pseudo)


    def test_delete_user_pseudo(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)

        # vérification
        self.assertTrue(DAOuser.does_pseudo_exist(pseudo))

        # on appel la fonction à tester
        DAOuser.delete_user_pseudo(pseudo)

        self.assertFalse(DAOuser.does_pseudo_exist(pseudo))


    def test_does_pseudo_exist(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)

        # recherche le pseudo de l'utilisateur test déjà créé dans la db
        tester_found = DAOuser.does_pseudo_exist(pseudo)
        # on vérifie que la fonction renvoie bien True, i.e. qu'elle a trouvé l'utilisateur dans la db
        self.assertTrue(tester_found)

        # on recherche un utilisateur inexistant (probabilité que le username généré par secrets.token_hex(10)existe déjà négligeable)
        tester_not_found = DAOuser.does_pseudo_exist(secrets.token_hex(10))
        # on vérifie que la fonction renvoie bien False
        self.assertFalse(tester_not_found)

        DAOuser.delete_user_pseudo(pseudo)

    def test_get_hpass_username(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)

        # on appel la fonction à tester
        tester_hpassword = DAOuser.get_hpass_username(username)

        # on vérifie que la fonction renvoie bien le mot de passe hashé
        self.assertEqual(hpassword, tester_hpassword)

        DAOuser.delete_user_pseudo(pseudo)


    def test_get_hpass_pseudo(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)

        # on appel la fonction à tester
        tester_hpassword = DAOuser.get_hpass_pseudo(pseudo)

        # on vérifie que la fonction renvoie bien le mot de passe hashé
        self.assertEqual(hpassword, tester_hpassword)
        DAOuser.delete_user_pseudo(pseudo)


    def test_get_pseudo(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)

        # on appel la fonction à tester
        tester_pseudo = DAOuser.get_pseudo(username)

        # on vérifie que la fonction renvoie bien le pseudo du joueur
        self.assertEqual(pseudo, tester_pseudo)

        DAOuser.delete_user_pseudo(pseudo)


    def test_get_est_connecte(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)

        # on appel la fonction à tester
        tester1 = DAOuser.get_est_connecte(username)

        # on vérifie qu'elle renvoie false
        self.assertFalse(tester1)

        try:
            DAOuser.update_est_connecte(username)
        except:
            return "Erreur dans l'appel à update_est_connecte, test avorté"

        # on appel la fonction à tester
        tester2 = DAOuser.get_est_connecte(username)

        self.assertTrue(tester2)

        DAOuser.delete_user_pseudo(pseudo)


    def test_update_est_connecte(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)

        # on appel la fonction à tester
        DAOuser.update_est_connecte(username)

        # on vérifie qu'on est connecté
        self.assertTrue(DAOuser.get_est_connecte(username))

        DAOuser.delete_user_pseudo(pseudo)




    def test_update_pseudo_table_utilisateur(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        old_pseudo = secrets.token_hex(10)
        new_pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, old_pseudo, hpassword)

        # on appel la fonction à tester
        DAOuser.update_pseudo(old_pseudo, new_pseudo)

        # on vérifie que le pseudo du joueur a été modifié :
        self.assertNotEqual(old_pseudo, new_pseudo)

        try:
            DAOuser.delete_user_pseudo(new_pseudo)
            DAOuser.delete_user_pseudo(old_pseudo)
        except:
            print("utilisateur non supprimé")


    def test_update_password(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        old_hpassword = secrets.token_hex(10)
        new_hpassword = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, pseudo, old_hpassword)

        # on appel la fonction à tester
        DAOuser.update_password(pseudo, new_hpassword)

        # on vérifie que le mdp a bien été modifié
        self.assertEqual(new_hpassword, DAOuser.get_hpass_pseudo(pseudo))

        # on supprime le joueur
        DAOuser.delete_user_pseudo(pseudo)


    def test_get_stat(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)

        # on appel la fonction à tester
        tester = DAOuser.get_stat(pseudo)

        # vérification
        self.assertIsNotNone(tester)

        # on supprime l'utilisateur test créé
        DAOuser.delete_user_pseudo(pseudo)


    def test_put_all_users_disconnected(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de deux utilisateurs.
        username1 = secrets.token_hex(10)
        pseudo1 = secrets.token_hex(10)
        hpassword1 = secrets.token_hex(10)

        username2 = secrets.token_hex(10)
        pseudo2 = secrets.token_hex(10)
        hpassword2 = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username1, pseudo1, hpassword1)
        DAOuser.add_user(username2, pseudo2, hpassword2)

        #on connecte les utilisateurs:
        DAOuser.update_est_connecte(username1)
        DAOuser.update_est_connecte(username2)

        # on appel la fonction à tester
        DAOuser.put_all_users_disconnected()
        # vérification
        self.assertFalse(DAOuser.get_est_connecte(username1))
        self.assertFalse(DAOuser.get_est_connecte(username2))

        # on supprime l'utilisateur test créé
        DAOuser.delete_user_pseudo(pseudo1)
        DAOuser.delete_user_pseudo(pseudo2)


if __name__ == "__main__":
    unittest.main()