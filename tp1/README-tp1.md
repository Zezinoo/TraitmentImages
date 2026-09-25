# TP n° 1 : Images numériques, couleur et robustesse

Ce dossier contient tout ce qu'il faut pour le TP n° 1 de traitement d'images.

## 1. Extraire l'archive

Extrayez `tp1.zip` dans votre dossier `~/Documents`. Vous obtenez :

```text
traitement-images/
├── README-tp1.md          # ce fichier
├── requirements.txt       # bibliothèques Python à installer
├── tp1/
│   └── tp1-images-couleur-robustesse.ipynb   # le bloc-notes
└── ressources-tp1/        # les images du TP
```

Ne déplacez ni ne renommez ces fichiers : le sujet retrouve seul le dossier
`ressources-tp1`.

## 2. Créer l'environnement virtuel

Ouvrez un terminal dans le dossier `traitement-images`, puis exécutez :

```text
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

L'installation prend quelques minutes. Comme en 2e année, l'environnement virtuel
`.venv` isole les bibliothèques de ce projet.

## 3. Ouvrir le sujet

Dans le même terminal, avec `.venv` activé, lancez :

```text
python -m jupyter notebook
```

Le navigateur s'ouvre : ouvrez `tp1/tp1-images-couleur-robustesse.ipynb`.

**N'ouvrez pas le bloc-notes par double-clic** : Jupyter démarrerait sans votre
environnement et les bibliothèques seraient introuvables. La première cellule de
code du sujet vous le signalera.

## 4. Aux séances suivantes

```text
cd traitement-images
source .venv/bin/activate
```

## Sur un portable personnel

- Sous Windows, remplacez `source .venv/bin/activate` par `.venv\Scripts\activate`
  et remplacez `python3` ou `python` par `py` si la commande est introuvable. Si
  PowerShell refuse l'activation, utilisez l'invite de commandes `cmd`.
- Vous pouvez aussi travailler dans *Visual Studio Code* : ouvrez le dossier
  `traitement-images`, puis sélectionnez l'interpréteur Python de `.venv`.
