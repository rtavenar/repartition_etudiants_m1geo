import random

__author__ = 'Romain Tavenard romain.tavenard[at]univ-rennes2.fr'


def liste_groupes(td_cible, affectations, horaires, list_td):
    """Liste les groupes possibles pour un TD donne pour un etudiant sachant ses affectations pour les autres groupes.

    Suppose que les codes des groupes de TD aient pour prefixe le nom du TD (ex : BDD1 pour un TD de BDD).

    Note : la liste des groupes possibles est volontairement melangee pour ne pas que les premiers TD dans l'ordre
    lexicographique soient systematiquement choisis.

    Parameters
    ----------
    td_cible    str
        Nom du TD pour lequel lister les groupes accessibles
    affectations    dict
        Dictionnaire contenant les affectations deja effectuees (les cles du dictionnaire sont les creneaux horaires et
        les valeurs associees sont les identifiants de groupe).
    horaires    dict
        Un dictionnaire indiquant les horaires de chaque groupe de TD
    list_td list
        Une liste des options a choisir par l'etudiant (si `td_cible` n'est pas dans cette liste, la fonction retournera
        `[None]`.

    Returns
    -------
    list
        Une liste des groupes de TD accessibles ou la liste contenant le seul element `None` si l'etudiant n'a pas
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
    """Calcule un ensemble de groupes de TD coherent (ie sans interference) pour un etudiant dont les options sont
    fournies.

    Suppose (code en dur) que les 3 TD que l'on peut considerer sont "BDD", "TEL" et "ENT" et que les noms de groupes
    de TD commencent par ces trois lettres suivies d'un identifiant (typiquement un chiffre, par exemple ENT3 pour le
    groupe 3 du TD ENT)

    Parameters
    ----------
    horaires    dict
        Un dictionnaire indiquant les horaires de chaque groupe de TD
    list_td    list
        Une liste de TD choisis par l'etudiant

    Returns
    -------
    dict
        Un dictionnaire contenant une proposition d'affectation (les cles du dictionnaire sont les creneaux horaires et
        les valeurs associees sont les identifiants de groupe).

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
    """Genere les listes d'etudiants inscrits dans chaque groupe pour une option donnee.

    Parameters
    ----------
    etudiants   dict
        Un dictionnaire ayant pour cles les numeros d'etudiants et pour valeurs les listes de groupes auxquels ils
        sont inscrits
    option  str
        Une chaine de caractere indiquant le cours pour lequel on veut faire des listes d'etudiants

    Returns
    -------
    dict
        Un dictionaire ayant pour cles les identifiants de groupes et pour valeurs les listes de numero d'etudiants
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
    """Retourne la paire cle-valeur associee a la plus petite valeur du dictionnaire.

    Parameters
    ----------
    d   dict
        Le dictionnaire a considerer

    Returns
    -------
    La cle correpondant au minimum
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
    """Retourne la paire cle-valeur associee a la plus grande valeur du dictionnaire.

    Parameters
    ----------
    d   dict
        Le dictionnaire a considerer

    Returns
    -------
    La cle correpondant au maximum
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
    """Tente de re-equilibrer les tailles des groupes de TD.

    Parameters
    ----------
    etudiants   dict
        Une proposition d'affectation possiblement non equilibree (dictionnaire dont les cles sont les numeros
        etudiants et les valeurs sont des listes de groupes de TD assignes)
    horaires    dict
        Un dictionnaire indiquant les horaires de chaque groupe de TD

    Returns
    -------
    dict
        Un dictionnaire au meme format que `etudiants` mais qui est cense correspondre a une version plus equilibree en
        termes de nombre d'etudiants par groupe de TD.
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
        print("Apres equilibrage : %s" % str({k: len(v) for k, v in regroupe(etudiants, option).items()}))
    return etudiants
