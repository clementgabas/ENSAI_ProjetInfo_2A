CREATE TABLE "Coups" (
	"id_partie"	INTEGER,
	"num_coup"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"pseudo_joueur"	INTEGER,
	"position"	INTEGER,
	"prochain_tour"	INTEGER
);
