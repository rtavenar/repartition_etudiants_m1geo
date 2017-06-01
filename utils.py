import random

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'


def get_list_groupes(option, contraintes, horaires, list_options):
    if option not in list_options:
        return ["NO_%s" % option]
    groupes_existants = [k for k in horaires.keys() if k.startswith(option)]
    random.shuffle(groupes_existants)
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
    minval, argmin = max(d.values()), None
    for k, v in d.items():
        if v <= minval:
            argmin = k
            minval = v
    return argmin, minval


def dict_argmax(d):
    maxval, argmax = min(d.values()), None
    for k, v in d.items():
        if v >= maxval:
            argmax = k
            maxval = v
    return argmax, maxval


def equilibrage(etudiants, horaires):
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
    return etudiants
