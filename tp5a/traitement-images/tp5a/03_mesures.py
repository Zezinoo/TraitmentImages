"""Relier le seuil à des mesures en pixels et en unités physiques."""
import matplotlib.pyplot as plt
import numpy as np
from skimage import filters, measure

from tp5a_outils import scene_uniforme, verifier, enregistrer, iou

image, reference = scene_uniforme()
image = filters.gaussian(image, sigma=1.2)
seuil = filters.threshold_otsu(image)
pas_um = 0.40
fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))
for axe, donnees, titre in zip(axes, (image, reference, image > seuil),
                               ('Image', 'Référence', f'Seuil {seuil:.3f}')):
    axe.imshow(donnees, cmap='gray', vmin=0, vmax=1)
    axe.set_title(titre)
    axe.axis('off')
enregistrer(fig, '03-masque.png')

print('Pas spatial :', pas_um, 'µm/pixel')
for variation in (-0.03, 0.0, 0.03):
    # TODO : former le masque pour seuil + variation, puis l'étiqueter.
    masque = None
    verifier(masque)
    labels = None
    verifier(labels)
    # TODO : mesurer les aires et calculer les diamètres équivalents.
    regions = None
    aires_px = None
    aires_um2 = None
    diametres_um = None
    for valeur in (regions, aires_px, aires_um2, diametres_um):
        verifier(valeur)
    print(f'Variation {variation:+.2f}: IoU={iou(masque, reference):.4f}, '
          f'{len(regions)} objets')
    for numero, (aire_px, aire_um2, diametre_um) in enumerate(
        zip(aires_px, aires_um2, diametres_um), start=1
    ):
        print(f'  objet {numero}: aire={aire_px:.0f} px² = {aire_um2:.1f} µm², '
              f'diamètre équivalent={diametre_um:.2f} µm')
