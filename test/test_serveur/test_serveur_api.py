# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 10:43:26 2020

@author: Maël
"""
import os
os.chdir("C:/Users/Maël/Projet-Info/AppServeur")
try :
    from api import app 
    import unittest
except Exception as e:
    print(" Il manque certains modules {} ".format(e))
    
class FlaskTest(unittest.TestCase):
        
    #vérife qu'on a la réponse 200 (ok)
    def test_index(self) :
        tester = app.test_client(self)
        response = tester.get("/home")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
    
    # vérifie si le contenu retourné est une application/json
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get("/home")
        self.assertEqual(response.content_type, "application/json")
    
    #vérifier les données retournées
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get("/home") 
        self.assertTrue(b'Message' in response.data)
        
if __name__ == "__main__":
    unittest.main()
            
    
    


