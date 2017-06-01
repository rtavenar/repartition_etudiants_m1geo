import random

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'


def liste_groupes(td_cible, affectations, horaires, list_td):
    """Liste les groupes possibles pour un TD donné pour un étudiant sachant ses affectations pour les autres groupes.

    Suppose que les codes des groupes de TD aient pour préfixe le nom du TD (ex : BDD1 pour un TD de BDD).

    Note : la liste des groupes possibles est volontairement mélangée pour ne pas que les premiers TD dans l'ordre
    lexicographique soient systématiquement choisis.

    Parameters
    ----------
    td_cible    str
        Nom du TD pour lequel lister les groupes accessibles
    affectations    dict
        Dictionnaire contenant les affectations déjà effectuées (les clés du dictionnaire sont les créneaux horaires et
        les valeurs associées sont les identifiants de groupe).
    horaires    dict
        Un dictionnaire indiquant les horaires de chaque groupe de TD
    list_td list
        Une liste des options à choisir par l'étudiant (si `td_cible` n'est pas dans cette liste, la fonction retournera
        `[None]`.

    Returns
    -------
    list
        Une liste des groupes de TD accessibles ou la liste contenant le seul élément `None` si l'étudiant n'a pas
        choisi le TD en question.

    Examples
    --------
    >>> horaires = {"BDD1": "LU08", "BDD2": "LU10", "TEL1": "LU08"}
    >>> affectations = {"LU08": "TEL1"}
    >>> sorted(liste_groupes("BDD", affectations, horaires, ["TEL", "BDD"]))
    ['BDD2']
    >>> sorted(liste_groupes("ENT", affectations, horaires, ["TEL", "BDD"]))
    [None]
    """
    if td_cible not in list_td:
        return [None]
    groupes_existants = [k for k in horaires.keys() if k.startswith(td_cible)]
    random.shuffle(groupes_existants)
    groupes_possibles = []
    for gr in groupes_existants:
        if horaires[gr] not in affectations.keys():
            groupes_possibles.append(gr)
    return groupes_possibles


def affecte(horaires, list_td):
    """Calcule un ensemble de groupes de TD cohérent (ie sans interférence) pour un étudiant dont les options sont
    fournies.

    Suppose (codé en dur) que les 3 TD que l'on peut considérer sont "BDD", "TEL" et "ENT" et que les noms de groupes
    de TD commencent par ces trois lettres suivies d'un identifiant (typiquement un chiffre, par exemple ENT3 pour le
    groupe 3 du TD ENT)

    Parameters
    ----------
    horaires    dict
        Un dictionnaire indiquant les horaires de chaque groupe de TD
    list_td    list
        Une liste de TD choisis par l'étudiant

    Returns
    -------
    dict
        Un dictionnaire contenant une proposition d'affectation (les clés du dictionnaire sont les créneaux horaires et
        les valeurs associées sont les identifiants de groupe).

    Example
    -------
    >>> horaires = {"BDD1": "LU08", "BDD2": "LU10", "TEL1": "LU08"}
    >>> affecte(horaires, ["BDD", "TEL"]) == {"LU08": "TEL1", "LU10": "BDD2"}
    True
    """
    affectation = {}
    for gr_bdd in liste_groupes("BDD", affectation, horaires, list_td):
        if gr_bdd is not None:
            affectation[horaires[gr_bdd]] = gr_bdd
        for gr_tel in liste_groupes("TEL", affectation, horaires, list_td):
            if gr_tel is not None:
                affectation[horaires[gr_tel]] = gr_tel
            for gr_ent in liste_groupes("ENT", affectation, horaires, list_td):
                if gr_ent is not None:
                    affectation[horaires[gr_ent]] = gr_ent
                return affectation
            del affectation[horaires[gr_tel]]
        del affectation[horaires[gr_bdd]]


def regroupe(etudiants, option):
    """Génère les listes d'étudiants inscrits dans chaque groupe pour une option donnée.

    Parameters
    ----------
    etudiants   dict
        Un dictionnaire ayant pour clés les numéros d'étudiants et pour valeurs les listes de groupes auxquels ils
        sont inscrits
    option  str
        Une chaîne de caractère indiquant le cours pour lequel on veut faire des listes d'étudiants

    Returns
    -------
    dict
        Un dictionaire ayant pour clés les identifiants de groupes et pour valeurs les listes de numéro d'étudiants
        inscrits dans les groupes

    Examples
    --------
    >>> etudiants = {"21600000": ["BDD1", "TEL2"], "21600001": ["BDD3", "TEL2"]}
    >>> regroupe(etudiants, "BDD") == {'BDD3': ['21600001'], 'BDD1': ['21600000']}
    True
    """
    listes = {}
    for numetu, list_groups in etudiants.items():
        for gr in list_groups:
            if gr.startswith(option):
                if gr not in listes.keys():
                    listes[gr] = []
                listes[gr].append(numetu)
    return listes


def dict_argmin(d):
    """Retourne la paire clé-valeur associée à la plus petite valeur du dictionnaire.

    Parameters
    ----------
    d   dict
        Le dictionnaire à considérer

    Returns
    -------
    La clé correpondant au minimum
    La valeur minimale

    Examples
    --------
    >>> dict_argmin({"a": 12, "b": 3, "c": 900})
    ('b', 3)
    """
    minval, argmin = max(d.values()), None
    for k, v in d.items():
        if v <= minval:
            argmin = k
            minval = v
    return argmin, minval


def dict_argmax(d):
    """Retourne la paire clé-valeur associée à la plus grande valeur du dictionnaire.

    Parameters
    ----------
    d   dict
        Le dictionnaire à considérer

    Returns
    -------
    La clé correpondant au maximum
    La valeur maximale

    Examples
    --------
    >>> dict_argmax({"a": 12, "b": 3, "c": 900})
    ('c', 900)
    """
    maxval, argmax = min(d.values()), None
    for k, v in d.items():
        if v >= maxval:
            argmax = k
            maxval = v
    return argmax, maxval


def equilibrage(etudiants, horaires):
    """Tente de ré-équilibrer les tailles des groupes de TD.

    Parameters
    ----------
    etudiants   dict
        Une proposition d'affectation possiblement non équilibrée (dictionnaire dont les clés sont les numéros
        étudiants et les valeurs sont des listes de groupes de TD assignés)
    horaires    dict
        Un dictionnaire indiquant les horaires de chaque groupe de TD

    Returns
    -------
    dict
        Un dictionnaire au même format que `etudiants` mais qui est censé correspondre à une version plus équilibrée en
        termes de nombre d'étudiants par groupe de TD.
    """
    for option in ["BDD", "TEL", "ENT"]:
        has_moved = True
        while has_moved:
            listes = regroupe(etudiants, option)
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
        print("Après équilibrage : %s" % str({k: len(v) for k, v in regroupe(etudiants, option).items()}))
    return etudiants
