CREATE TABLE "Parties" (
	"id_partie"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"id_jeu"	INTEGER,
	"pseudo_proprietaire"	TEXT,
	"places_disponibles"	INTEGER
);
