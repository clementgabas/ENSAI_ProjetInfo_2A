CREATE TABLE "Utilisateur" (
	"pseudo"	TEXT UNIQUE,
	"identifiant"	TEXT UNIQUE,
	"mdp"	TEXT,
	"est_connecte"	TEXT,
	"en_file"	TEXT,
	"en_partie"	TEXT,
	PRIMARY KEY("pseudo")
);

