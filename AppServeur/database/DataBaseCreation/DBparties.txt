CREATE TABLE "Parties" (
	"id_partie"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"jeu"	TEXT,
	"date_debut"	TEXT,
	"date_fin"	TEXT,
	"pseudo_proprietaire"	TEXT,
	"places_total"	INTEGER,
	"places_dispo"	INTEGER
);