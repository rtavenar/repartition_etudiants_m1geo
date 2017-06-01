import csv
import numpy

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'


def get_list_groupes(option, contraintes, horaires, list_options):
    if option not in list_options:
        return ["NO_%s" % option]
    groupes_existants = [k for k in horaires.keys() if k.startswith(option)]
    numpy.random.shuffle(groupes_existants)
    groupes_possibles = []
    for gr in groupes_existants:
        if horaires[gr] not in contraintes.keys():
            groupes_possibles.append(gr)
    return groupes_possibles


def get_contraintes(horaires, list_options):
    contraintes = {}
    for gr_bdd in get_list_groupes("BDD", contraintes, horaires, list_options):
        if gr_bdd != "NO_BDD":
            contraintes[horaires[gr_bdd]] = gr_bdd
        for gr_tel in get_list_groupes("TEL", contraintes, horaires, list_options):
            if gr_tel != "NO_TEL":
                contraintes[horaires[gr_tel]] = gr_tel
            for gr_ent in get_list_groupes("ENT", contraintes, horaires, list_options):
                if gr_ent != "NO_ENT":
                    contraintes[horaires[gr_ent]] = gr_ent
                return contraintes
            del contraintes[horaires[gr_tel]]
        del contraintes[horaires[gr_bdd]]
    return None


horaires = {}
for row in csv.reader(open("data/horaires.csv", "r"), delimiter=";"):
    horaires[row[0]] = row[1]

etudiants = {}
for row in csv.reader(open("data/input_data.csv", "r"), delimiter=";"):
    etudiants[row[0]] = row[1:]

fp = open("data/groupes_bruts.csv", "w")
for numetu, list_options in etudiants.items():
    contraintes = get_contraintes(horaires, list_options)
    fp.write(numetu + ";" + ";".join(contraintes.values()) + "\n")
