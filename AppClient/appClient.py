from Vues.menu_Accueil import Menu_Accueil

def lancer_appli():
	Acceuil = Menu_Accueil()
	Acceuil.display_info()
	return Acceuil.make_choice()

if __name__ == "__main__":
	with open("Vues/Affichagetxt/parchemin_Accueil.txt", "r") as parchemin:
		aff = parchemin.read()
		print(aff)
	lancer_appli()