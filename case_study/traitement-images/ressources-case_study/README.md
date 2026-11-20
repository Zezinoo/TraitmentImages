# Ressources de l'étude de cas "parking"

Les 177 photographies et les étiquettes proviennent du jeu de données **CNRPark+EXT**, caméra 6, publié par Amato, Carrara, Falchi, Gennaro et Vairo : <https://cnrpark.it/>. Le site officiel annonce la licence **Open Data Commons Open Database License (ODbL) 1.0** pour ce jeu de données. Les photographies fournies sont des copies de fichiers conservés dans les archives du cours, sélectionnées pour cette étude et renommées `R00`, `C001` à `C080`, `V001` à `V056` et `E001` à `E040`. Elles n'ont été ni redessinées ni générées par IA.

Les noms des fichiers sont identiques dans les deux versions de l'étude de cas. Le dossier `ressources-case_study/` contient les ressources suivantes :

| Fichier ou dossier | Description |
| :------------------------------ | :---------------------------------------------------------------------- |
| `images/` | Photographies en couleur utilisées par les programmes, dont la référence `R00.jpg`. |
| `images.csv` | Pour chaque photographie : code, nom du fichier, date, heure, météo et groupe auquel elle appartient. |
| `parking_spaces.csv` | Numéros des huit places et coordonnées de leurs rectangles (`x0`, `y0`, `x1`, `y1`). |
| `labels_tuning.csv` | États de référence des places (0 = libre, 1 = occupée), appelés "étiquettes", pour l'ensemble de réglage. |
| `labels_validation.csv` | Étiquettes des places pour l'ensemble de validation. |
| `reference_spaces.png` | Aperçu de `R00` en niveaux de gris, avec les rectangles et les numéros des places. |
| `requirements.txt` | Liste des bibliothèques Python nécessaires aux programmes. |

Dans `images.csv`, la colonne `partition` indique l'ensemble auquel appartient chaque photographie. La valeur `calibrage` désigne l'ensemble de réglage. Les scripts communs utilisent le nom de colonne `split` et la valeur `calibration` dans leurs résultats pour désigner ce même ensemble. Ces différences de noms ne changent pas la répartition des photographies.

Les étiquettes libre/occupée ont été extraites du fichier officiel `CNRPark+EXT.csv`. Pour chaque couple (image, place), la correspondance repose sur la caméra, la date, l'heure et l'identifiant de la place. `0` signifie libre ; `1` signifie occupée.

Les coordonnées des rectangles proviennent du fichier officiel `camera6.csv`, conservé dans les archives du cours. Elles se rapportent initialement à des images de 2592 x 1944 pixels. Elles ont été mises à l'échelle pour les images distribuées de 1000 x 750 pixels, puis arrondies. Ces rectangles délimitent les places, pas les contours des véhicules.

Huit instants répartis entre environ 8 h et 16 h ont été retenus pour chacune des 22 journées analysées, sans sélectionner les images selon l'occupation des places.

Les étiquettes de l'ensemble d'évaluation restent réservées à l'enseignant.

`R00` montre les huit places libres ; elle sert de référence et n'est pas elle-même évaluée.

Les journées de réglage, de validation et d'évaluation sont distinctes : toutes les photographies retenues pour une même journée appartiennent au même ensemble.
