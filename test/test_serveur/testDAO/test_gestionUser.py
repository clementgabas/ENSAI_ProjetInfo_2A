# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 10:43:26 2020

@author: Maël
"""
import os
os.chdir("C:/Users/Maël/Projet-Info/AppServeur/DAO")
import gestionUser
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
        tester_created = gestionUser.add_user(username, pseudo, hpassword )
    
        #on vérifie que les infos de l'utilisateur sont bien dans la base de données
        self.assertIsNotNone(tester_created.identifiant)
        self.assertIsNotNone(tester_created.pseudo)
        self.assertIsNotNone(tester_created.mdp)
        

    def test_does_user_exist(self):
        
        #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        tester_created = gestionUser.add_user(username, pseudo, hpassword )

        #recherche l'utilisateur test déjà créé dans la base de données 
        tester_found = gestionUser.does_username_exist(tester_created.identifiant)
        #on vérifie que la fonction renvoie bien True, i.e. qu'elle a trouvé l'utilisateur dans la db
        self.assertTrue(tester_found)
        
        #on recherche un utilisateur inexistant (probabilité que le username généré par secrets.token_hex(10)existe déjà négligeable)
        tester_not_found = gestionUser.does_username_exist(secrets.token_hex(10))
        #on vérifie que la fonction renvoie bien False
        self.assertFalse(tester_not_found)

    
    def test_does_pseudo_exist(self):
        
        #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        tester_created = gestionUser.add_user(username, pseudo, hpassword )

        #recherche le pseudo de l'utilisateur test déjà créé dans la db
        tester_found = gestionUser.does_pseudo_exist(tester_created.identifiant)
        #on vérifie que la fonction renvoie bien True, i.e. qu'elle a trouvé l'utilisateur dans la db
        self.assertTrue(tester_found)
        
        #on recherche un utilisateur inexistant (probabilité que le username généré par secrets.token_hex(10)existe déjà négligeable)
        tester_not_found = gestionUser.does_pseudo_exist(secrets.token_hex(10))
        #on vérifie que la fonction renvoie bien False
        self.assertFalse(tester_not_found)

    def test_add_user_score(self):
        
        #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        tester_created = gestionUser.add_user(username, pseudo, hpassword )
    
        
        #on appel la fonction à tester
        tester_score = gestionUser.add_user_score(tester_created.pseudo)
        
        #on vérifie que la ligne n'est pas vide
        self.assertIsNotNone(tester_score.pseudo)
    
    def test_get_hpass_username(self):
        
         #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        tester_created = gestionUser.add_user(username, pseudo, hpassword )
        
        #on appel la fonction à tester
        tester_hpassword = gestionUser.get_hpass_username(tester_created.identifiant)
        
        #on vérifie que la fonction renvoie bien le mot de passe hashé
        self.assertIs(tester_created.hpassword, tester_hpassword)
        
    def test_get_hpass_pseudo(self):
        
         #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        tester_created = gestionUser.add_user(username, pseudo, hpassword )
        
        #on appel la fonction à tester
        tester_hpassword = gestionUser.get_hpass_pseudo(tester_created.pseudo)
        
        #on vérifie que la fonction renvoie bien le mot de passe hashé
        self.assertIs(tester_created.mdp, tester_hpassword)
    
    def test_get_pseudo(self):
        
         #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        tester_created = gestionUser.add_user(username, pseudo, hpassword )
        
        #on appel la fonction à tester
        tester_pseudo = gestionUser.get_pseudo(tester_created.identifiant)
        
        #on vérifie que la fonction renvoie bien le pseudo du joueur
        self.assertIs(tester_created.pseudo, tester_pseudo)
        
    def test_update_pseudo_table_utilisateur(self):
        
        #génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de l'utilisateur test.
        username = secrets.token_hex(10)
        old_pseudo = secrets.token_hex(10)
        new_pseudo = secrets.token_hex(10)
        hpassword = secrets.token_hex(10)
        
        #créé l'utilisateur test
        tester_created = gestionUser.add_user(username, old_pseudo, hpassword)
        
        #on appel la fonction à tester
        gestionUser.update_pseudo_utilisateur(tester_created.pseudo, new_pseudo)
        
        #on vérifie que le pseudo du joueur a été modifié :
        self.assertIs(tester_created.pseudo, new_pseudo)
        
    
        
    
if __name__ == "__main__":
    unittest.main()
            
        
        
        
        
           
        
        
