create database apijeux
use apijeux;

CREATE TABLE "Utilisateur" (
	"pseudo"	TEXT UNIQUE,
	"identifiant"	TEXT UNIQUE,
	"mdp"	TEXT,
	"est_connecte"	TEXT,
	"en_file"	TEXT,
	"en_partie"	TEXT,
	PRIMARY KEY("pseudo")
);

CREATE TABLE "Scores" (
	"jeu"	TEXT,
	"pseudo"	TEXT,
	"nb_points"	INTEGER,
	"nb_parties_jouees" INTEGER,
	"nb_parties_gagnees" INTEGER,
	PRIMARY KEY("jeu","pseudo")
);

CREATE TABLE "Parties" (
	"id_partie"	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	"jeu"	TEXT,
	"date_debut"	TEXT,
	"pseudo_proprietaire"	TEXT,
	"places_total"	INTEGER,
	"places_dispo"	INTEGER,
	"statut"	TEXT,
	"aquiltour"	INTEGER,
	"ami_anonyme"	TEXT
);

CREATE TABLE "Participation" (
	"pseudo"	TEXT,
	"id_partie"	INTEGER,
	"couleur"	INTEGER,
	"est_pret"	TEXT,
	"ordre"	INTEGER,
	PRIMARY KEY("pseudo","id_partie")
);


CREATE TABLE "Liste_Amis" (
	"pseudo"	TEXT,
	"pseudo_ami"	TEXT,
	"date_ajout"	TEXT,
	PRIMARY KEY("pseudo","pseudo_ami")
);

CREATE TABLE "Coups" (
	"id_partie"	INTEGER,
	"num_coup"	REAL,
	"pseudo_joueur"	TEXT,
	"position"	INTEGER,
	"prochain_tour"	INTEGER,
	PRIMARY KEY("num_coup","id_partie")
);