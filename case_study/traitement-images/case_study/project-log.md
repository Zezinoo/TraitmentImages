# Journal de bord de l'étude de cas / Case study project log

**Binôme / Team members :**

- Bouchet Elisabeth
- Alves Mesquita José Vitor

Ce fichier commun accompagne les deux dépôts en séance et le rendu final. Quelques phrases précises suffisent à chaque étape. Conservez les états précédents lorsque vous le complétez. Vous pouvez rédiger vos réponses en français ou en anglais.

This shared file accompanies both checkpoints and the final submission. A few precise sentences are enough at each stage. Keep earlier entries when adding new ones. You may write your answers in French or English.

## Fin de la première séance / End of the first session

**Date :** 20/11/2026

**Essai exécuté et nom du CSV / Run completed and prediction CSV filename (`baseline` peut fournir les résultats globaux / may supply the overall results) :**

Méthode de départ : `baseline`. Deux pistes personnelles ont également été testées : une comparaison après lissage gaussien et un seuillage de Sauvola.

**À compléter :** noms exacts des essais et des fichiers CSV correspondant aux figures ci-dessous.

**Deux observations sur les images et les erreurs de la méthode de départ / Two observations about images and baseline errors :**

1. Les variations de luminosité et les ombres entraînent des erreurs d'identification.
2. Certaines voitures, notamment blanches, peuvent ne pas modifier suffisamment la moyenne d'intensité de la place pour être détectées.

La méthode de départ soustrait la moyenne d'intensité de la référence vide à celle de la place observée, puis compare la valeur absolue de cette différence à un seuil de décision. Cette mesure ne suffit pas à distinguer toutes les variations observées, comme le montre la matrice de confusion suivante.

![Matrice de confusion de la méthode de départ sur l'ensemble de validation.](results/project-log-figures/baseline-validation.png)

Convention des étiquettes : `1` signifie « place occupée » et `0` signifie « place libre ».

**Première proposition de chaîne et justification, consignée avant les essais / Initial pipeline proposal and justification, recorded before running trials :**

1. Sélectionner uniquement les places considérées à l'aide de leurs zones d'intérêt.
2. Lisser l'image pour essayer de diminuer l'impact des ombres.
3. Comparer la moyenne de chaque place à une valeur de référence ; envisager une comparaison sur les trois couleurs ou une moyenne locale dans la place.

### Observations ayant motivé les pistes de traitement

![Exemple d'image avec du soleil et des reflets.](results/project-log-figures/observation-soleil.png)

*Soleil.*

![Exemple d'image avec une ombre portée sur les places.](results/project-log-figures/observation-ombre.png)

*Ombre.*

En observant notamment la place **204**, nous distinguons quatre principales sources de variation :

- l'environnement extérieur : passant, roue d'une voiture voisine, etc. ;
- le déplacement des ombres ;
- les réflexions du soleil ;
- les changements de luminosité liés à l'heure de la journée.

Les hypothèses envisagées sont les suivantes :

- utiliser un seuil en niveaux de gris pour supprimer les reflets et d'autres variations ; cette première piste a conduit à des erreurs ;
- utiliser le seuillage de Sauvola pour observer les variations locales et essayer d'en déduire la présence d'une voiture ;
- utiliser un filtrage gaussien pour atténuer certaines variations et le bruit ;
- utiliser un seuil de couleur pour observer l'apparition d'éléments colorés.

Nous souhaitons d'abord étudier les variations dues aux ombres et au soleil. Deux pistes ont été retenues pour les essais : une comparaison après lissages gaussiens et un seuillage de Sauvola. Nous envisageons de les combiner lors de la prochaine séance.

Repérage des images dans le jeu de données : `C` pour calibrage, `V` pour validation et `E` pour évaluation.
**Ce que nous avons effectivement codé et testé pendant la séance / Code actually written and tested during the session :**

### Comparaison après lissages gaussiens

Nous avons testé une approche fondée sur la différence entre l'image courante et la référence après lissage gaussien. Nous avons comparé plusieurs valeurs de sigma pour l'image courante et pour la référence afin d'observer leur effet sur les variations spatiales et le bruit.

Les analyses ont été effectuées sur des images converties en niveaux de gris. Après soustraction des images lissées, nous avons étudié la médiane des différences absolues dans chaque crop comme score possible. Les visualisations permettent également de comparer la moyenne et la médiane et d'examiner un seuil de décision.

Les essais de lissage se trouvent dans `test_blurring.py`. La méthode personnelle est conservée dans `pipeline_dog.py`, dans la fonction `predict()`.

![Comparaison des lissages et des différences, avec moyenne et médiane par place.](results/project-log-figures/comparaison-lissage.png)

*Exemple de sortie de `test_blurring.py` : comparaison des valeurs de sigma, des différences signées et absolues, puis de la moyenne et de la médiane dans les places. Cette figure a servi à examiner l'effet du lissage et le choix d'un seuil.*

![Matrices de confusion de l'essai utilisant les lissages gaussiens.](results/project-log-figures/confusion-gaussiennes.png)

*Résultats de l'essai présenté dans le document source sur les ensembles de réglage et de validation. Le nom exact de l'essai et sa configuration restent à préciser.*

### Seuillage de Sauvola

Nous avons également testé le seuillage de Sauvola. Le code ci-dessous est repris du document source ; seule son indentation a été remise en forme.

```python
import numpy as np
from skimage import filters, color
from tools import crop

DECISION_THRESHOLD = 0.1


def predict(image, reference, box):
    """Return (score, decision) for one parking slot.

    The reference shows this slot empty. This baseline compares the mean of
    all three RGB channels. It does not account for shadows, lighting changes,
    or the spatial structure of a vehicle. Keep this method unchanged when
    comparing its results with those of your own pipeline.
    """
    current = crop(image, box)
    empty = crop(reference, box)
    current = color.rgb2gray(current)
    empty = color.rgb2gray(empty)

    # On évalue les valeurs de Sauvola.
    seuil_sauvola = filters.threshold_sauvola(
        current, window_size=41, k=0.2, r=0.5
    )
    masque_sauvola = current < seuil_sauvola

    # On fait un seuillage sur l'image de référence.
    empty_threshold = filters.threshold_sauvola(
        empty, window_size=41, k=0.2, r=0.5
    )
    # Ici, on a les pixels sombres qui existaient avant les voitures.
    empty_mask = masque_sauvola < empty_threshold

    # On ne garde que les pixels sombres qui n'existaient pas avant les voitures.
    new_pixels = masque_sauvola & ~empty_mask

    # On regarde la proportion de nouveaux pixels parmi tous les pixels présents.
    score = float(np.mean(new_pixels))
    print(score)

    decision = int(score > DECISION_THRESHOLD)
    return score, decision
```

Les étapes sont détaillées dans les commentaires. Les paramètres de Sauvola ont été repris du TP5a, car ils nous semblaient encore adaptés à la situation.

![Matrices de confusion de l'essai utilisant le seuillage de Sauvola.](results/project-log-figures/confusion-sauvola.png)

*Résultats de l'essai Sauvola sur les ensembles de réglage et de validation. Nous envisageons ensuite de modifier `DECISION_THRESHOLD` pour étudier son effet sur les résultats.*
**Fichier et fonction du premier traitement personnel, puis commande pour l'exécuter / File and function implementing the first personal processing step, followed by its execution command :**

- Comparaison des lissages et affichage des différences : `case_study/test_blurring.py`.
- Méthode gaussienne : fonction `predict()` dans `case_study/pipeline_dog.py`.
- Méthode de Sauvola : fonction `predict()` reproduite ci-dessus ; **fichier utilisé à préciser**.

Depuis le dossier `traitement-images/`, la visualisation des lissages se lance avec :

```sh
python case_study/test_blurring.py
```

**À compléter :** commande exacte utilisée pour reproduire chacun des essais et ses matrices de confusion.

Le code est également disponible dans le [dépôt du projet](https://github.com/Zezinoo/TraitmentImages).
**Figure montrant l'entrée et le résultat, et commentaire (`case_study/results/first-step.png`) / Figure showing the input and result, with an explanation (`case_study/results/first-step.png`) :**

![Image C012 avec les rectangles des places et les décisions affichées.](results/project-log-figures/c012-decisions.png)

*Image **C012**, reprise du document source, avec les huit places repérées. La comparaison des lissages et des différences intermédiaires est présentée plus haut.*

**À compléter :** identifier précisément la méthode et l'essai ayant produit cette figure, puis fournir la figure d'entrée et de résultat demandée sous le nom `case_study/results/first-step.png`.
**Difficulté encore ouverte / Unresolved difficulty :**

Les variations de luminosité et les ombres restent difficiles à distinguer des changements liés à la présence d'une voiture. Certaines voitures noires se confondent également avec les variations sombres ou le bruit. Nous souhaitons poursuivre l'étude des seuils et envisager une combinaison des deux pistes à la prochaine séance.
La chaîne complète peut rester inachevée. Le premier dépôt demande un traitement personnel exécuté et commenté. Si vous n'avez pas pu l'exécuter ou produire sa figure, indiquez le blocage et déposez tout de même votre code.

The full pipeline may remain unfinished. Checkpoint 1 requires one personal processing step that has been run and discussed. If you could not run it or produce its figure, explain the difficulty and still submit your code.

## Fin de la seconde séance / End of the second session

**Date :**

**Essai exécuté et nom du CSV / Run completed and prediction CSV filename :**

**Étapes du prototype réellement exécutées, résultats intermédiaires et étapes manquantes / Prototype steps actually run, intermediate results, and missing steps :**

**Masque et mesure, s'ils sont disponibles / Mask and measurement, if available :**

**Commande reproduisant une étape exécutée et figure jointe (par exemple `case_study/results/checkpoint-2.png`) / Command reproducing a completed step and attached figure (for example `case_study/results/checkpoint-2.png`) :**

**Résultats sur les ensembles de réglage et de validation si la méthode produit déjà des décisions ; sinon, analyse des résultats intermédiaires / Tuning-set and validation-set results if the method already produces decisions; otherwise, intermediate-result analysis :**

**Résultat observé et situation difficile analysée (identifiants image/place), même si la chaîne reste incomplète / Observed result and analysis of a difficult situation (image and space IDs), even if the pipeline is unfinished :**

**Les résultats joints correspondent-ils au code déposé ? Sinon, précisez les différences / Do the attached results correspond to the submitted code? If not, explain the differences :**

**Travail restant avant le rendu final / Work remaining before the final submission :**

## Contributions et assistance / Contributions and assistance

Précisez les contributions de chaque membre. Pour chaque usage d'un assistant IA, indiquez l'outil, la tâche, les fichiers ou passages concernés, ce qui a été repris ou modifié, et comment vous avez vérifié le résultat. Ajoutez une ligne à chaque nouvelle utilisation, y compris pendant le travail personnel. Si vous n'avez pas utilisé d'assistant IA, écrivez explicitement "aucune assistance IA".

State each team member's contribution. For every use of an AI assistant, give the tool, task, affected files or report sections, what you retained or changed, and how you checked the result. Add a row for each new use, including work done after class. If you used no AI assistant, write "no AI assistance" explicitly.

| Moment / Stage | Membre / Team member | Travail réalisé / Work completed | Assistant IA et aide obtenue, ou "aucune" / AI assistant and help received, or "none" | Vérifications et modifications / Checks and changes |
|---|---|---|---|---|
| Séance 1 / Session 1 | | | | |
| Séance 2 / Session 2 | | | | |
| Après les séances / After class | | | | |
| Aide pendant les essais | À préciser | Visualisation des lissages et des différences ; compréhension des scores et des métriques. | Codex : aide à la modification de `test_blurring.py`, explications sur les splits, les statistiques par crop et les commandes de rapport. | Contrôles par l'assistant : exécution des visualisations sans interface, inspection des figures et calcul des métriques sur un CSV sauvegardé. Vérifications et modifications du binôme à compléter. |
| Mise en forme du journal | À préciser | Conversion du document PDF en `project-log.md` et intégration des sept figures. | Codex : organisation selon le modèle fourni, mise en forme Markdown, indentation du code et corrections de langue. | Contrôle de la structure, des liens vers les figures et de la syntaxe du bloc Python par l'assistant ; relecture du binôme à compléter. |

## Rendu final / Final submission

Le rendu final comprend une chaîne complète et reproductible et un rapport terminé. La souplesse des dépôts en séance concerne le travail en cours.

The final submission includes a complete, reproducible pipeline and a finished report. Flexibility at the classroom checkpoints concerns work in progress.

**Vérification de l'exécution sur toutes les images fournies, des scores finis et des décisions 0 ou 1 / Checks that the pipeline runs on all supplied images, returns finite scores, and outputs decisions of 0 or 1 :**

**Paramètres et bibliothèques nécessaires / Required parameters and libraries :**

**Nom de la méthode retenue et commande qui régénère les résultats / Selected method and command that reproduces the results :**

**Écart entre le prototype de la seconde séance et le rendu final / Changes between the second-session prototype and final submission :**

**Limite principale que nous savons expliquer / Main limitation we can explain :**
