CREATE TABLE "Scores" (
	"jeu"	TEXT,
	"pseudo"	TEXT,
	"nb_points"	INTEGER,
	"nb_partie_jouee" INTEGER,
	"nb_partie_gagnee" INTEGER
	PRIMARY KEY("jeu","pseudo")
);
