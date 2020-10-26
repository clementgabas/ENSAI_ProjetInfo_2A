CREATE TABLE "Utilisateur" (
	"pseudo"	TEXT UNIQUE,
	"identifiant"	TEXT UNIQUE,
	"mdp"	TEXT,
	"nbr_parties_jouees"	INTEGER,
	"nbr_parties_gagnees"	INTEGER,
	"est_connecte"	TEXT,
	"en_file"	TEXT,
	"en_partie"	TEXT,
	PRIMARY KEY("pseudo")
);

