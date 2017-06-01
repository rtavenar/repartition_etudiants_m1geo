import csv
import random

from utils import get_contraintes, equilibrage

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'

# Etape 1 : Récupérer les horaires des différents groupes dans le fichier data/horaires.csv
horaires = {}
for row in csv.reader(open("data/horaires.csv", "r"), delimiter=";"):
    horaires[row[0]] = row[1]

# Etape 2 : Récupérer les choix d'option des étudiants dans le fichier data/input_data.csv
etudiants = {}
for row in csv.reader(open("data/input_data.csv", "r"), delimiter=";"):
    etudiants[row[0]] = row[1:]

random.seed(0)  # Uniquement pour pouvoir faire tourner plusieurs fois et obtenir les mêmes groupes

# Etape 3 : créer des groupes (potentiellement déséquilibrés)
etudiants_dans_les_groupes = {}
for numetu, list_options in etudiants.items():
    contraintes = get_contraintes(horaires, list_options)
    etudiants_dans_les_groupes[numetu] = list(contraintes.values())

# Etape 4 : équilibrer les groupes
etudiants_dans_les_groupes = equilibrage(etudiants_dans_les_groupes, horaires)

# Etape 5 : Ecrire les groupes dans un fichier
fp = open("data/groupes_equilibres.csv", "w")
for numetu, list_groupes in etudiants_dans_les_groupes.items():
    fp.write(numetu + ";" + ";".join(list_groupes) + "\n")