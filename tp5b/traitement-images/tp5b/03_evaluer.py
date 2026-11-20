"""Évaluer le recouvrement et le comptage des deux watershed."""
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage as ndi
from skimage import filters, segmentation

from tp5b_outils import scene_cellules, verifier, scores_binaires, enregistrer

image, masque, reference, marqueurs = scene_cellules()
# TODO : calculer distance, gradient et les deux segmentations comme à l'activité 2.
distance = ndi.distance_transform_edt(image)
gradient = filters.sobel(image)
labels_distance =  segmentation.watershed(-distance, markers=marqueurs, mask=masque)
labels_gradient =  segmentation.watershed(gradient, markers=marqueurs, mask=masque)
for valeur in (distance, gradient, labels_distance, labels_gradient):
    verifier(valeur)

reference_binaire = reference > 0
for nom, labels in [('distance', labels_distance), ('gradient', labels_gradient)]:
    prediction = labels > 0
    iou, dice = scores_binaires(prediction, reference_binaire)
    nombre_objets = len(np.unique(labels)) - int(0 in labels)
    erreur_pixels = np.count_nonzero(prediction ^ reference_binaire)
    print(f'{nom}: IoU={iou:.4f}, Dice={dice:.4f}, '
          f'objets={nombre_objets}, pixels mal classés={erreur_pixels}')
    # TODO : calculer l'IoU séparément pour chaque étiquette d'objet.
    iou_par_objet = {}
    for etiquette in np.unique(reference):
        if etiquette == 0:
            continue  # Ignore the background

        prediction_objet = labels == etiquette
        reference_objet = reference == etiquette

        iou_objet, _ = scores_binaires(prediction_objet, reference_objet)
        iou_par_objet[int(etiquette)] = iou_objet
    
    verifier(iou_par_objet)
    print('  IoU par objet :', iou_par_objet)

fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))
for axe, etiquettes, titre in zip(
    axes, (reference, labels_distance, labels_gradient),
    ('Référence', 'Distance', 'Gradient')
):
    axe.imshow(etiquettes, cmap='nipy_spectral', vmin=0, vmax=4,
               interpolation='nearest')
    axe.set_title(titre)
    axe.axis('off')
enregistrer(fig, '03-evaluation.png')
