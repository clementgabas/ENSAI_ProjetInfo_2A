CREATE TABLE "Scores" (
	"jeu"	TEXT,
	"pseudo"	TEXT,
	"nb_points"	INTEGER,
	"nb_parties_jouees" INTEGER,
	"nb_parties_gagnees" INTEGER,
	PRIMARY KEY("jeu","pseudo")
);
