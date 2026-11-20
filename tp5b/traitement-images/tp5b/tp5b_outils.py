"""Scène synthétique et affichage communs au TP5b."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from skimage.draw import disk

DOSSIER_SCRIPTS = Path(__file__).resolve().parent
DOSSIER_RESULTATS = DOSSIER_SCRIPTS / 'resultats'


def scene_cellules():
    hauteur, largeur = 192, 256
    y, x = np.indices((hauteur, largeur))
    centres = [(62, 60), (62, 94), (132, 160), (132, 194)]
    rayon = 23
    reference = np.zeros((hauteur, largeur), dtype=int)
    masque = np.zeros((hauteur, largeur), dtype=bool)
    image = np.full((hauteur, largeur), 0.12, dtype=float)
    marqueurs = np.zeros((hauteur, largeur), dtype=int)
    for etiquette, (cy, cx) in enumerate(centres, start=1):
        distance2 = (y - cy)**2 + (x - cx)**2
        objet = distance2 <= rayon**2
        masque |= objet
        reference[objet & (reference == 0)] = etiquette
        image += 0.72 * np.exp(-distance2 / (2 * (rayon * 0.68)**2))
        rr, cc = disk((cy, cx), 4, shape=marqueurs.shape)
        marqueurs[rr, cc] = etiquette
    rng = np.random.default_rng(51)
    image += rng.normal(0, 0.025, image.shape)
    image = np.clip(image, 0, 1)
    return image, masque, reference, marqueurs


def verifier(valeur):
    if valeur is None:
        raise NotImplementedError('Complétez les passages TODO avant de lancer le script.')
    return valeur


def enregistrer(figure, nom):
    DOSSIER_RESULTATS.mkdir(exist_ok=True)
    figure.tight_layout()
    chemin = DOSSIER_RESULTATS / nom
    figure.savefig(chemin, dpi=150, bbox_inches='tight')
    print('Figure enregistrée :', chemin)
    plt.show()


def scores_binaires(prediction, reference):
    intersection = np.count_nonzero(prediction & reference)
    union = np.count_nonzero(prediction | reference)
    total = np.count_nonzero(prediction) + np.count_nonzero(reference)
    iou = 1.0 if union == 0 else intersection / union
    dice = 1.0 if total == 0 else 2 * intersection / total
    return iou, dice
