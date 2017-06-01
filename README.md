# Répartir les étudiants de M1 Géo dans les groupes en fonction de leurs choix d'option

Ici, on suppose que l'on a en entrée les fichiers `data/input_data.csv` et `data/horaires.csv` (y jeter un oeil pour se rendre compte de leur contenu).

On va d'abord commencer par créer des groupes (potentiellement déséquilibrés) puis les rééquilibrer.
L'algorithme d'équilibrage n'est pas optimal, mais il semble fonctionner.

Pour lancer la moulinette, il faut entrer dans un terminal :

```bash
export PYTHONPATH="${PYTHONPATH}:."
python groupes.py
```

Le terminal nous indique les effectifs des groupes après équilibrage (pour chaque option).
Et le fichier `data/groupes_equilibres.csv` donne pour chaque étudiant ses groupes d'option.
