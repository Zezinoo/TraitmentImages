# Étude de cas : installation

1. Extrayez cette archive dans votre dossier de travail. Elle contient `traitement-images/case_study/` et `traitement-images/ressources-case_study/`.
2. Copiez ces deux dossiers dans le projet `traitement-images/` utilisé pendant les TP, puis ouvrez ce projet dans *Visual Studio Code*.
3. Sélectionnez l'interpréteur de l'environnement virtuel `.venv` existant. Si une dépendance manque, exécutez `python3 -m pip install -r ressources-case_study/requirements.txt` depuis la racine du projet, dans un terminal où cet environnement est activé.
4. Depuis la racine du projet, lancez `python3 case_study/explore.py`. Suivez les consignes du sujet pour observer les images et consigner votre première proposition de chaîne avant les essais. Lancez ensuite `python3 case_study/run.py --method baseline --name baseline`. Les résultats sont enregistrés dans `case_study/results/`.
5. Complétez `case_study/project-log.md` pendant le travail. À la fin de chaque séance, utilisez `case_study/export_checkpoint.py` comme indiqué dans le sujet et déposez l'archive produite sur Moodle.

Le sujet PDF détaille le travail attendu et les modalités de dépôt. Les scripts de solution et les étiquettes de l'ensemble d'évaluation ne sont pas inclus dans cette archive.
