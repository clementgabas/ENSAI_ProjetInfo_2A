CREATE TABLE "Coups" (
	"id_partie"	INTEGER,
	"num_coup"	INTEGER,
	"pseudo_joueur"	INTEGER,
	"position"	INTEGER,
	"prochain_tour"	INTEGER,
	PRIMARY KEY("num_coup","id_partie")
);