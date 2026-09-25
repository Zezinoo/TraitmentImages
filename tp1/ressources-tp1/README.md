# Ressources du TP n°1

Ce dossier contient uniquement les images utilisées pour le TP n° 1.

Il est distribué dans l'archive `tp1.zip`, avec le sujet, `requirements.txt` et
`README-tp1.md`, qui explique l'installation.

| Fichier | Rôle dans le TP |
|---|---|
| `01-axes-canaux.png` | Vérification des axes, des canaux et du découpage |
| `02-ensicaen-niveaux-gris.jpg` | Calculs sur la dynamique et l'écrêtage |
| `03-billet-50-euros-rgba.png` | Illustration factice avec canal alpha non constant et région d'intérêt |
| `04-balles-reference.jpg` | Réglage des méthodes de sélection par couleur |
| `05-balles-annotation-reference.png` | Annotation de référence : contours tracés à la main puis ajustés par des cercles |
| `06-balles-perturbation-assombrie.png` | Perturbation contrôlée : réduction des intensités |
| `07-balles-perturbation-chaude.png` | Perturbation contrôlée : balance des canaux vers le chaud |
| `08-balles-perturbation-gamma-froide-bruit.png` | Perturbation contrôlée : gamma, dominante froide et bruit |
| `09-fruits-transfert.jpg` | Transfert vers une scène et des objets différents |
| `10-carre-reference.png` | Réglage d'un seuil sur une image scalaire contrôlée |
| `11-carre-verite-terrain.png` | Vérité terrain géométrique du carré |
| `12-carre-faible-gain.png` | Validation après gain et décalage des niveaux |
| `13-carre-decale.png` | Décalage pur de +0,20, sans écrêtage |
| `14-carre-fond-variable-bruit.png` | Limite de la normalisation globale sur un fond variable et bruité |
| `15-balles-validation.jpg` | Validation sur une nouvelle photographie (autres balles, flash, plastique mat) |
| `16-balles-validation-annotation.png` | Annotation de référence de l'image 15, sans règle de couleur |

## Crédits

| Fichier | Origine et transformation | Auteur ou production | Licence ou statut |
|---|---|---|---|
| `01-axes-canaux.png` | Tableau RGB synthétique produit par `scripts/generate_tp1_resources.py` | Production pédagogique locale | Production propre |
| `02-ensicaen-niveaux-gris.jpg` | Copie de `originaux/ensicaen_gray.jpg`, version en niveaux de gris de la photographie `ensicaen.jpg`, créée avec GIMP et déjà utilisée dans le cours | ENSICAEN | (c) ENSICAEN, usage interne |
| `03-billet-50-euros-rgba.png` | Rendu PNG RGBA à 4800 pixels de large de `originaux/50-euros-factice.svg`, avec coins arrondis transparents et fenêtre semi-transparente sur l'hologramme (`scripts/billet_factice_rgba.py`) | frankes, "50 Euro Note" | Illustration CC0 ; reproduction du motif soumise aux règles de la BCE |
| `04-balles-reference.jpg` | Copie de `originaux/play-balls.jpg` | Petr Kratochvil, "Play balls" | CC0 / domaine public |
| `05-balles-annotation-reference.png` | Tracé manuel dans Inkscape, puis ajustement de cercles par RANSAC avec `scripts/construire_annotation.py` | Production pédagogique locale dérivée de 04 | CC0 / domaine public |
| `06-balles-perturbation-assombrie.png` | Réduction calculée des intensités de 04 | Production pédagogique locale dérivée de 04 | CC0 / domaine public |
| `07-balles-perturbation-chaude.png` | Modification calculée de la balance des canaux de 04 | Production pédagogique locale dérivée de 04 | CC0 / domaine public |
| `08-balles-perturbation-gamma-froide-bruit.png` | Gamma, balance froide et bruit calculés à partir de 04 | Production pédagogique locale dérivée de 04 | CC0 / domaine public |
| `09-fruits-transfert.jpg` | Réduction de `originaux/fruits.jpg` | Bhaskar Peddhapati (peddhapati, Chicago), "Fruits!" | CC BY 2.0 |
| `10-carre-reference.png` | Image synthétique bruitée produite à partir de `originaux/square.png`, dessin historique créé avec GIMP | Production pédagogique locale | Production propre |
| `11-carre-verite-terrain.png` | Masque géométrique calculé à partir du carré | Production pédagogique locale | Production propre |
| `12-carre-faible-gain.png` | Transformation affine calculée de 10 | Production pédagogique locale | Production propre |
| `13-carre-decale.png` | Décalage pur de +0,20 calculé à partir de 10, sans écrêtage | Production pédagogique locale | Production propre |
| `14-carre-fond-variable-bruit.png` | Gamma, fond variable et bruit calculés à partir de 10 | Production pédagogique locale | Production propre |
| `15-balles-validation.jpg` | Version réduite de "Toy balls with different Colors" | Ramesh NG | CC BY-SA 2.0 |
| `16-balles-validation-annotation.png` | Annotation produite avec `scripts/construire_annotation_validation.py` | Production pédagogique locale dérivée de 15 | CC BY-SA 2.0 |

Complément sur les provenances :

- `03` : [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:50-Euro.svg),
  illustration publiée à l'origine sur
  [Openclipart](https://openclipart.org/detail/185895/50-euro-note-by-frankes-185895) ;
  Commons rappelle les conditions de reproduction des billets fixées par la BCE
- `09` : [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Fruits!.jpg),
  import de [Bhaskar Peddhapati Photography sur Flickr](https://www.flickr.com/photos/peddhapati/9729907217/)
  ("254/365: 09/11/2013. Fruits!"), même photographie
- `04` à `08` : [Public Domain Pictures](https://www.publicdomainpictures.net/en/view-image.php?image=24696&picture=play-balls)
- `15` et `16` : [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Toy_balls_with_different_Colors.jpg)

Le fichier `02` est la propriété de l'ENSICAEN et reste réservé à un usage
interne. Tous les autres fichiers ont une origine et une licence établies.
