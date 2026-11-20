"""Mesurer les cellules annotées avec les moments d'ordre deux."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tp5b_outils import enregistrer

DOSSIER_TP = Path(__file__).resolve().parents[1]
DOSSIER_RESSOURCES = DOSSIER_TP / 'ressources'
if not (DOSSIER_RESSOURCES / 'ecoli_brightfield.tif').is_file():  # archive étudiante
    DOSSIER_RESSOURCES = DOSSIER_TP / 'ressources-tp5b'
PAS_UM = 0.106  # micromètre par pixel

image = np.asarray(Image.open(DOSSIER_RESSOURCES / 'ecoli_brightfield.tif'))
etiquettes = np.asarray(Image.open(DOSSIER_RESSOURCES / 'ecoli_instances.tif'))
identifiants = np.unique(etiquettes)
identifiants = identifiants[identifiants != 0]

# TODO : pour chaque étiquette, trouvez les coordonnées (x=colonne, y=ligne)
# et calculez m00, m10, m01, puis x_barre et y_barre.
# Calculez ensuite mu20, mu02 et mu11, puis la matrice de covariance C.
# Les valeurs propres de C donnent les axes de l'ellipse équivalente :
# longueurs = 4*sqrt(lambda), en pixels. Convertissez-les en micromètres.
mesures = []
for identifiant in identifiants:
    y, x = np.nonzero(etiquettes == identifiant)
    m00 = None
    m10 = None
    m01 = None
    x_barre = None
    y_barre = None
    mu20 = None
    mu02 = None
    mu11 = None
    C = None
    valeurs_propres = None
    verifier = (m00, m10, m01, x_barre, y_barre, mu20, mu02, mu11, C, valeurs_propres)
    if any(valeur is None for valeur in verifier):
        raise NotImplementedError('Complétez les calculs de moments avant de lancer le script.')
    axe_long_um, axe_court_um = 4 * np.sqrt(valeurs_propres[::-1]) * PAS_UM
    aire_um2 = m00 * PAS_UM**2
    mesures.append((int(identifiant), m00, aire_um2, axe_long_um, axe_court_um))

print(f'{len(mesures)} objets mesures ; calibration = {PAS_UM:.3f} um/pixel')
print('ID | pixels | aire (um^2) | grand axe (um) | petit axe (um)')
for identifiant, aire_px, aire_um2, grand, petit in mesures:
    print(f'{identifiant:2d} | {aire_px:6d} | {aire_um2:10.3f} | {grand:14.3f} | {petit:14.3f}')
grands_axes = np.array([mesure[3] for mesure in mesures])
print('Grand axe (um) : min =', round(grands_axes.min(), 3),
      '| médiane =', round(np.median(grands_axes), 3),
      '| max =', round(grands_axes.max(), 3))

fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
axes[0].imshow(image, cmap='gray')
axes[0].set_title('Image en champ clair')
axes[1].imshow(etiquettes, cmap='nipy_spectral', interpolation='nearest')
axes[1].set_title('Étiquettes des bactéries annotées')
for ax in axes:
    ax.set_axis_off()
enregistrer(fig, '04-bacteries.png')
