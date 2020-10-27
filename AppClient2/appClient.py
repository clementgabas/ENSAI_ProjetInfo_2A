from menu_Accueil import Menu_Accueil

def lancer_appli():
	Acceuil = Menu_Acceuil()
	Acceuil.display_info()
	return Acceuil.make_choice()

if __name__ == "__main__":
	lancer_appli()