# Répartir les étudiants de M1 Géo dans les groupes en fonction de leurs choix d'option

Ici, on suppose que l'on a en entrée les fichiers `data/input_data.csv` et `data/horaires.csv` (y jeter un oeil pour se rendre compte de leur contenu).

On va d'abord commencer par créer des groupes (potentiellement déséquilibrés) :

```bash
python faire_les_groupes.py
```

Cela génère un fichier `data/groupes_bruts.csv` qui contient, pour chaque étudiant, ses groupes d'option.
Les groupes générés sont probablement déséquilibrés. 
On peut essayer d'y pallier avec :

```bash
python equilibrer_les_groupes.py
```

Le terminal nous indique les effectifs des groupes après équilibrage.
Et le fichier `data/groupes_equilibres.csv` donne pour chaque étudiant ses groupes d'option.
