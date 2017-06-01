import csv
import numpy

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'


def compte(etudiants, option):
    listes = {}
    for numetu, list_groups in etudiants.items():
        for gr in list_groups:
            if gr.startswith(option):
                if gr not in listes.keys():
                    listes[gr] = []
                listes[gr].append(numetu)
    return listes


def dict_argmin(d):
    minval, argmin = numpy.inf, None
    for k, v in d.items():
        if v < minval:
            argmin = k
            minval = v
    return argmin, minval


def dict_argmax(d):
    maxval, argmax = -numpy.inf, None
    for k, v in d.items():
        if v > maxval:
            argmax = k
            maxval = v
    return argmax, maxval


horaires = {}
for row in csv.reader(open("data/horaires.csv", "r"), delimiter=";"):
    horaires[row[0]] = row[1]

etudiants = {}
for row in csv.reader(open("data/groupes_bruts.csv", "r"), delimiter=";"):
    etudiants[row[0]] = row[1:]

for option in ["BDD", "TEL", "ENT"]:
    has_moved = True
    while has_moved:
        listes = compte(etudiants, option)
        tailles = {k: len(v) for k, v in listes.items()}
        argmin_taille, min_taille = dict_argmin(tailles)
        argmax_taille, max_taille = dict_argmax(tailles)
        if max_taille - min_taille < 2:
            break
        has_moved = False
        for numetu, list_groupes in etudiants.items():
            if argmax_taille in list_groupes:
                list_horaires = [horaires[gr] for gr in list_groupes if gr != argmax_taille]
                if horaires[argmin_taille] not in list_horaires:
                    etudiants[numetu] = [gr for gr in list_groupes if gr != argmax_taille] + [argmin_taille]
                    has_moved = True
                    break
    print("Après équilibrage : %s" % str({k: len(v) for k, v in compte(etudiants, option).items()}))

fp = open("data/groupes_equilibres.csv", "w")
for numetu, list_groupes in etudiants.items():
    fp.write(numetu + ";" + ";".join(list_groupes) + "\n")