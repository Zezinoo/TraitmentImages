"""Scènes synthétiques et affichage communs au TP5a."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from skimage.draw import disk

DOSSIER_SCRIPTS = Path(__file__).resolve().parent
DOSSIER_RESULTATS = DOSSIER_SCRIPTS / 'resultats'


def _scene(fond_variable=False):
    rng = np.random.default_rng(2026)
    hauteur, largeur = 192, 256
    y, x = np.indices((hauteur, largeur))
    if fond_variable:
        image = 0.78 - 0.28 * x / (largeur - 1)
        contraste = -0.35
    else:
        image = np.full((hauteur, largeur), 0.22)
        contraste = 0.53
    reference = np.zeros((hauteur, largeur), dtype=bool)
    objets = [((42, 45), 14), ((42, 108), 19), ((42, 190), 12),
              ((92, 52), 18), ((92, 126), 13), ((92, 205), 20),
              ((148, 42), 12), ((148, 105), 20), ((148, 184), 15),
              ((148, 230), 10)]
    for centre, rayon in objets:
        rr, cc = disk(centre, rayon, shape=reference.shape)
        reference[rr, cc] = True
    image[reference] += contraste
    image += rng.normal(0, 0.025, image.shape)
    return np.clip(image, 0, 1), reference


def scene_uniforme():
    return _scene(False)


def scene_eclairee():
    return _scene(True)


def scene_bruitee():
    masque = np.zeros((128, 192), dtype=bool)
    for centre, rayon in [((34, 35), 15), ((34, 86), 15), ((78, 145), 20)]:
        rr, cc = disk(centre, rayon, shape=masque.shape)
        masque[rr, cc] = True
    # Deux pixels en contact diagonal matérialisent l'ambiguïté 4/8-connexité.
    masque[88, 32] = True
    masque[89, 33] = True
    rng = np.random.default_rng(140)
    bruit = rng.random(masque.shape) < 0.004
    return masque, np.logical_xor(masque, bruit)


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


def iou(prediction, reference):
    union = np.count_nonzero(prediction | reference)
    return 1.0 if union == 0 else np.count_nonzero(prediction & reference) / union
