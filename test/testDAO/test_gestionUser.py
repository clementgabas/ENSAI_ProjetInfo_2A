# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 10:43:26 2020

@author: Maël
"""

import AppServeur.DAO.gestionUser as DAOuser
import unittest
import secrets

class Test_gestionUser(unittest.TestCase):


     def test_add_user(self) :
        """
        On teste l'insertion en vérifiant que l'on a bien un pseudo, identifiant et mdp pour notre utilisateur.
        Puis on supprime la ligne. Cette méthode à beaucoup de problèmes,
        mais avec les outils à disposition il est difficile de faire
        mieux.
        """

        #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #on appel la fonction à tester
        DAOuser.add_user(username, pseudo, hpassword)
        
           
        #on vérifie que les infos de l'utilisateur sont bien dans la base de données
        self.assertTrue(DAOuser.does_pseudo_exist(pseudo))
        self.assertTrue(DAOuser.does_username_exist(username))

        DAOuser.delete_user_pseudo(pseudo)

     def test_does_username_exist(self):
        
        #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)

        #recherche l'utilisateur test déjà créé dans la base de données 
        tester_found = DAOuser.does_username_exist(username)
        #on vérifie que la fonction renvoie bien True, i.e. qu'elle a trouvé l'utilisateur dans la db
        self.assertTrue(tester_found)
        
        #on recherche un utilisateur inexistant (probabilité que le username généré par secrets.token_hex(10)existe déjà négligeable)
        tester_not_found = DAOuser.does_username_exist(secrets.token_hex(10))
        #on vérifie que la fonction renvoie bien False
        self.assertFalse(tester_not_found)
        
        DAOuser.delete_user_pseudo(pseudo)

    def test_delete_user_pseudo(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)

        # on appel la fonction à tester
        DAOuser.delete_user_pseudo(pseudo)

        # vérification
        self.assertIsFalse(DAOuser.does_user_exist(pseudo))

        # on supprime l'utilisateur test créé
        DAOuser.delete_user_pseudo(pseudo)

    def test_does_pseudo_exist(self):
        
        #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword )

        #recherche le pseudo de l'utilisateur test déjà créé dans la db
        tester_found = DAOuser.does_pseudo_exist(pseudo)
        #on vérifie que la fonction renvoie bien True, i.e. qu'elle a trouvé l'utilisateur dans la db
        self.assertTrue(tester_found)
        
        #on recherche un utilisateur inexistant (probabilité que le username généré par secrets.token_hex(10)existe déjà négligeable)
        tester_not_found = DAOuser.does_pseudo_exist(secrets.token_hex(10))
        #on vérifie que la fonction renvoie bien False
        self.assertFalse(tester_not_found)

        DAOuser.delete_user_pseudo(pseudo)
    def test_add_user_score(self):

        #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword )
    
        
        #on appel la fonction à tester
        DAOuser.add_user_score(pseudo)
        
        #on vérifie que la ligne n'est pas vide
        self.assertTrue(DAOuser.does_pseudo_exist_score(pseudo))
        # attention : does_user_exist_score n'existe pas encore dans DAOuser
        
        DAOuser.delete_user_pseudo(pseudo)
        pass

    def test_get_hpass_username(self):
        
         #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword )
        
        #on appel la fonction à tester
        tester_hpassword = DAOuser.get_hpass_username(username)
        
        #on vérifie que la fonction renvoie bien le mot de passe hashé
        self.assertIs(hpassword, tester_hpassword)

        DAOuser.delete_user_pseudo(pseudo)
        
    def test_get_hpass_pseudo(self):
        
        #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword )
        
        #on appel la fonction à tester
        tester_hpassword = DAOuser.get_hpass_pseudo(pseudo)
        
        #on vérifie que la fonction renvoie bien le mot de passe hashé
        self.assertIs(hpassword, tester_hpassword)
        DAOuser.delete_user_pseudo(pseudo)
        
    def test_get_pseudo(self):
        
         #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword )
        
        #on appel la fonction à tester
        tester_pseudo = DAOuser.get_pseudo(pseudo)
        
        #on vérifie que la fonction renvoie bien le pseudo du joueur
        self.assertIs(pseudo, tester_pseudo)

        DAOuser.delete_user_pseudo(pseudo)
        
    def test_get_est_connecte_false(self):
        
        #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)
                
        #on appel la fonction à tester
        tester_get_connexion = DAOuser.get_est_connecte(username)
        
        #on vérifie qu'elle renvoie false
        self.assertFalse(tester_get_connexion)

        DAOuser.delete_user_pseudo(pseudo)
        
    def test_update_est_connecte(self):
        
        #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)
        
        #on appel la fonction à tester
        DAOuser.update_est_connecte(username)
        
        #on vérifie qu'on est connecté
        self.assertTrue(DAOuser.get_est_connecte(username))
            
        DAOuser.delete_user_pseudo(pseudo)
        
    def test_update_pseudo_table_utilisateur(self):
        
        #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        old_pseudo = secrets.token_hex(10)
        new_pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        DAOuser.add_user(username, old_pseudo, hpassword)
        
        #on appel la fonction à tester
        DAOuser.update_pseudo_utilisateur(old_pseudo, new_pseudo)
        
        #on vérifie que le pseudo du joueur a été modifié :
        self.assertIs(old_pseudo, new_pseudo)

        try :
            DAOuser.delete_user_pseudo(new_pseudo)
        except :
            DAOuser.delete_user_pseudo(old_pseudo)

    def test_update_password(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        old_hpassword = secrets.token_hex(10)
        new_hpassword = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, pseudo, old_hpassword)

        #on appel la fonction à tester
        DAOuser.update_password(pseudo, new_hpassword)

        #on vérifie que le mdp a bien été modifié
        self.assertIs(new_hpassword, DAOuser.get_hpass_pseudo(pseudo))

        #on supprime le joueur
        DAOuser.delete_user_pseudo(pseudo)

    def test_get_stat(self):
        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # créé l'utilisateur test
        DAOuser.add_user(username, pseudo, hpassword)

        #on appel la fonction à tester
        tester = DAOuser.get_stat(pseudo)

        #vérification
        self.assertIsNotNone(tester)

        #on supprime l'utilisateur test créé
        DAOuser.delete_user_pseudo(pseudo)

    def test_update_stat(self):

        # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)

        # créé l'utilisateur test dans les deux tables
        DAOuser.add_user(username, pseudo, hpassword)
        DAOuser.add_user_score(pseudo)
        #on appel la fonction à tester
        DAOuser.update_stat(pseudo)

        #vérification
        self.assertTrue(DAOuser.does_pseudo_score_exist(pseudo))
        #on supprime l'utilisateur test créé
        DAOuser.delete_user_pseudo(pseudo)

        pass

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

        # on appel la fonction à tester
        DAOuser.put_all_users_disconnected()

        # vérification
        self.assertFalse(DAOuser.get_est_connecte(pseudo1))
        self.assertFalse(DAOuser.get_est_connecte(pseudo2))



        # on supprime l'utilisateur test créé
        DAOuser.delete_user_pseudo(pseudo1)
        DAOuser.delete_user_pseudo(pseudo2)


if __name__ == "__main__":
    unittest.main()
