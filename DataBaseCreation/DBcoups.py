CREATE TABLE "Coups" (
	"ieme_coup"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"id_partie"	INTEGER,
	"numero_joueur"	INTEGER,
	"position"	INTEGER,
	"prochain_tour"	INTEGER
);
