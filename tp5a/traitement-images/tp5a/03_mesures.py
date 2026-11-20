"""Relier le seuil à des mesures en pixels et en unités physiques."""
import matplotlib.pyplot as plt
import numpy as np
from skimage import filters, measure , morphology

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

diametres_ref = [14,19,12,18,13,20,12,20,15]
diametres_ref = [2*pas_um*r for r in diametres_ref]
diametres_ref = sorted(diametres_ref)

print('Pas spatial :', pas_um, 'µm/pixel')
for variation in (-0.03, 0.0, 0.03):
    # TODO : former le masque pour seuil + variation, puis l'étiqueter.
    masque = image > seuil + variation 
    verifier(masque)
    labels = morphology.label(masque , connectivity=2)
    verifier(labels)
    # TODO : mesurer les aires et calculer les diamètres équivalents.
    regions = measure.regionprops(labels)
    aires_px = [r.area for r in regions]
    aires_um2 = [p * pas_um**2 for p in aires_px]
    diametres_um = [2 * np.sqrt(a/np.pi) for a in aires_um2]
    sorted_diameters = sorted(diametres_um)
    for valeur in (regions, aires_px, aires_um2, diametres_um):
        verifier(valeur)
    print(f'Variation {variation:+.2f}: IoU={iou(masque, reference):.4f}, '
          f'{len(regions)} objets')
    for numero, (aire_px, aire_um2, diametre_um) in enumerate(
        zip(aires_px, aires_um2, diametres_um), start=1
    ):
        print(f'  objet {numero}: aire={aire_px:.0f} px² = {aire_um2:.1f} µm², '
              f'diamètre équivalent={diametre_um:.2f} µm')
    for ref,measured in zip(diametres_ref , sorted_diameters):
        print(f"Relative Variation : {abs((ref-measured)/measured)}")
