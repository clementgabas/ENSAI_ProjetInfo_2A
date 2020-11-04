CREATE TABLE "Parties" (
	"id_partie"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"jeu"	TEXT,
	"date_debut"	TEXT,
	"date_fin"	TEXT,
	"pseudo_proprietaire"	TEXT,
	"places_total"	INTEGER,
	"places_dispo"	INTEGER,
	"J2pseudo"	TEXT,
	"J3pseudo"	TEXT,
	"J4pseudo"	TEXT,
	"J5pseudo"	TEXT,
	"J1couleur"	TEXT,
	"J2couleur"	TEXT,
	"J3couleur"	TEXT,
	"J4couleur"	TEXT,
	"J5couleur"	TEXT
);