import AppServeur.DAO.gestionUser as DAOuser
import AppServeur.DAO.gestionAmis as DAOamis
import unittest
import secrets

class Test_gestionAmis(unittest.TestCase):

     def test_add_amitie(self) :
          # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de deux utilisateurs.
          username1 = secrets.token_hex(10)
          pseudo1 = secrets.token_hex(10)
          hpassword1 = secrets.token_hex(10)

          username2 = secrets.token_hex(10)
          pseudo2 = secrets.token_hex(10)
          hpassword2 = secrets.token_hex(10)

          # créé l'utilisateur test
          try:
               DAOuser.add_user(username1, pseudo1, hpassword1)
               DAOuser.add_user(username2, pseudo2, hpassword2)
          except:
               return("erreur dans la fonction DAOuser.add_user")
          # on appel la fonction à tester

          DAOamis.add_amitie(pseudo1, pseudo2)

          # vérification
          self.assertTrue(DAOamis.are_pseudos_friends(pseudo1, pseudo2))

          try:
          # on supprime l'utilisateur test créé
               DAOuser.delete_user_pseudo(pseudo1)
               DAOuser.delete_user_pseudo(pseudo2)
          except:
               return("erreur dans la fonction DAOuser.delete_user_pseudo")

     def test_are_pseudos_friends(self):
          # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de deux utilisateurs.
          username1 = secrets.token_hex(10)
          pseudo1 = secrets.token_hex(10)
          hpassword1 = secrets.token_hex(10)

          username2 = secrets.token_hex(10)
          pseudo2 = secrets.token_hex(10)
          hpassword2 = secrets.token_hex(10)

          # créé l'utilisateur test
          try:
               DAOuser.add_user(username1, pseudo1, hpassword1)
               DAOuser.add_user(username2, pseudo2, hpassword2)
          except:
               return ("erreur dans la fonction DAOuser.add_user")
               # on appel la fonction à tester

          DAOamis.add_amitie(pseudo1, pseudo2)

          # on vérifie que pseudo2 est dans la liste d'amis de pseudo1
          self.assertTrue(DAOamis.are_pseudos_friends(pseudo1, pseudo2))


          #on vérifie que la fonction ne renvoie pas True à chaque fois
          self.assertFalse(pseudo1, secrets.token_hex(10))

          try:
               # on supprime l'utilisateur test créé
               DAOuser.delete_user_pseudo(pseudo1)
               DAOuser.delete_user_pseudo(pseudo2)
          except:
               return ("erreur dans la fonction DAOuser.delete_user_pseudo")

     def test_sup_amitie
          # génération de chaînes de 10 caractères aléatoires (et sécurisés) pour créer les infos de deux utilisateurs.
          username1 = secrets.token_hex(10)
          pseudo1 = secrets.token_hex(10)
          hpassword1 = secrets.token_hex(10)

          username2 = secrets.token_hex(10)
          pseudo2 = secrets.token_hex(10)
          hpassword2 = secrets.token_hex(10)

          # créé l'utilisateur test
          try:
               DAOuser.add_user(username1, pseudo1, hpassword1)
               DAOuser.add_user(username2, pseudo2, hpassword2)
          except:
               return ("erreur dans la fonction DAOuser.add_user")
          # on appel la fonction à tester
          try:
               DAOamis.add_amitie(pseudo1, pseudo2)
          except:
               return ("erreur dans la fonction DAOamis.add_amitie")
          DAOamis.sup_amitie(pseudo1, pseudo2)

          # vérification
          self.assertFalse(DAOamis.are_pseudos_friends(pseudo1, pseudo2))

          try:
               # on supprime l'utilisateur test créé
               DAOuser.delete_user_pseudo(pseudo1)
               DAOuser.delete_user_pseudo(pseudo2)
          except:
               return ("erreur dans la fonction DAOuser.delete_user_pseudo")

