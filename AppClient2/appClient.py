from menu_Accueil import Menu_Accueil
from printFunctions import timePrint as print


def lancer_appli():
	Acceuil = Menu_Accueil()
	Acceuil.display_info()
	return Acceuil.make_choice()

if __name__ == "__main__":
	print("on peut peut etre afficher un dessin via un .txt pour faire genre on 'ouvre' l'appli")
	lancer_appli()