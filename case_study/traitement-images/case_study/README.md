# Voir et améliorer votre méthode

Depuis la racine de `traitement-images/`, lancez `python3 case_study/explore.py`. Observez les images et consignez une première proposition de chaîne de traitements dans le journal, avant les essais. Exécutez ensuite la méthode de départ fournie séparément dans `baseline.py` :

```sh
python3 case_study/run.py --method baseline --name baseline
```

Le fichier `pipeline.py` contient une copie modifiable de la méthode simple. Vous pouvez l'améliorer ou réécrire entièrement votre chaîne de traitements. Conservez l'interface documentée de `predict()`. Les exigences de compréhension et de justification restent les mêmes dans les deux démarches. Lancez votre essai :

```sh
python3 case_study/run.py --name trial1
```

Ouvrez ensuite `case_study/results/trial1/report/index.html` dans Firefox ou un autre navigateur. Le terminal affiche aussi l'adresse locale du rapport. Aucune bibliothèque supplémentaire, aucun serveur et aucune connexion Internet ne sont nécessaires pour l'afficher.

L'archive unique contient les notices françaises et anglaises. Les scripts, les commandes et les noms de résultats sont communs aux deux langues. Le menu "Langue / Language" du rapport permet de passer du français à l'anglais sans relancer les traitements.

Le rapport montre, pour chaque photographie, les places prédites libres ou occupées, leurs identifiants, les comptages et le taux d'occupation des huit places suivies. Les contours en tirets indiquent une prédiction "libre" ; les contours continus indiquent une prédiction "occupée". Le tableau associe chaque identifiant de place à son état prédit. Les fichiers `occupancy.csv` et `predictions.csv` du rapport contiennent respectivement les comptages et le taux d'occupation par photographie, et les scores et décisions par place.

Les aperçus PNG de décisions reprennent ces types de contours sur une photographie en niveaux de gris. Chaque identifiant est suivi de `0` pour une place prédite libre ou de `1` pour une place prédite occupée. Dans les aperçus d'exploration, `?` indique qu'aucun verdict n'est affiché. La conversion en gris concerne uniquement les aperçus PNG : les fichiers d'origine et les tableaux RGB utilisés par votre méthode restent inchangés.

Pour un essai de votre chaîne personnelle, le rapport utilise les décisions calculées par votre fonction `predict()`, sans appeler le démonstrateur. Ces prédictions doivent être comparées aux étiquettes de référence. Utilisez les matrices de confusion et les autres diagnostics de l'essai pour analyser vos erreurs sur les ensembles de réglage et de validation. Les étiquettes de l'ensemble d'évaluation restent réservées à l'enseignant.

Le rapport ne montre pas automatiquement les masques ou les autres étapes intermédiaires de votre méthode. Ajoutez les visualisations nécessaires pour expliquer vos choix. Les graphiques de diagnostic utilisent des niveaux de gris, des hachures et des types de traits pour rester lisibles à l'impression en noir et blanc.

L'option `--method baseline` exécute la méthode de départ et produit le rapport correspondant. Par défaut, `run.py` exécute votre fonction `predict()` définie dans `pipeline.py`. Le nom d'essai `baseline` est réservé à la méthode de départ pour protéger ce point de comparaison.

Après une modification de votre chaîne de traitements ou de ses paramètres, utilisez un nouveau nom pour conserver les résultats de l'essai précédent. Le nom d'essai ne sauvegarde ni le code ni ses paramètres : conservez-les séparément pour pouvoir reproduire les résultats. Par exemple :

```sh
python3 case_study/run.py --name trial2
```

Pour comparer deux essais, ouvrez leurs rapports dans deux onglets et sélectionnez la même photographie. Après une modification du code, relancez l'essai pour recalculer les résultats et régénérer le rapport. Si vous réutilisez un nom d'essai, cette exécution remplace les résultats et le rapport correspondants ; actualisez ensuite la page du navigateur.

Pour créer ou régénérer le rapport à partir du fichier `case_study/results/predictions-trial1.csv`, sans réexécuter la chaîne de traitement, utilisez :

```sh
python3 case_study/view_results.py --trial trial1
```

Conservez le dossier `report/` entier pour déplacer ou partager un rapport : il contient la page HTML, les fichiers CSV et les photographies nécessaires à sa consultation.

Les archives de séance contiennent le code Python courant, le modèle `parking_report.html`, le journal, le CSV des prédictions et les figures `confusion-matrices.png` et `metrics-by-day.png`. Ajoutez vos figures personnelles avec l'option `--figure`, répétable. Elles doivent se trouver dans `case_study/results/` et être au format PNG, PDF ou SVG. Les archives n'incluent pas le dossier `report/` ni les photographies du jeu de données.

## Premier dépôt : un traitement personnel exécuté

Rendez le code d'un traitement choisi à partir de vos observations et exécuté sur au moins une place. La chaîne complète peut rester inachevée. Enregistrez vos fichiers Python personnels dans `case_study/` pour les inclure dans l'archive. Enregistrez une figure de l'entrée et du résultat sous `case_study/results/first-step.png`. Expliquez le choix, le résultat et la commande de reproduction dans le journal.

Après avoir exécuté la méthode de départ, créez l'archive :

```sh
python3 case_study/export_checkpoint.py 1 --trial baseline --figure first-step.png
```

Les résultats de `baseline` accompagnent votre code personnel et sa figure. L'exporteur n'importe pas `pipeline.py` : une erreur de syntaxe dans la chaîne en cours ne bloque pas la création de l'archive. Si aucune figure n'a pu être produite, retirez `--figure` et son chemin pour déposer tout de même le code et expliquer le blocage.

## Second dépôt : un prototype en cours et des essais analysés

Présentez les étapes effectivement exécutées, leurs résultats et une situation difficile. Expliquez le masque et la mesure s'ils sont disponibles ; identifiez les étapes manquantes. La chaîne complète n'est pas exigée à ce stade.

Pour joindre une figure `case_study/results/checkpoint-2.png` avec les résultats d'un essai `trial1` terminé :

```sh
python3 case_study/export_checkpoint.py 2 --trial trial1 --figure checkpoint-2.png
```

Si votre méthode ne produit pas encore de décisions, utilisez `baseline` à la place de `trial1`. Vos sources et la figure personnelle sont aussi incluses. Analysez les résultats intermédiaires dans le journal en les distinguant des résultats de la méthode de départ.

## Rendu final : une chaîne complète et un rapport terminé

La version finale doit fonctionner sur toutes les images fournies, produire des scores finis et des décisions 0 ou 1, et pouvoir être relancée avec les paramètres, commandes et bibliothèques indiqués. Mesurez et analysez les erreurs ; une exécution réussie ne garantit pas des décisions toujours correctes. Joignez le rapport terminé et les fichiers demandés par le sujet dans le dossier compressé final.
