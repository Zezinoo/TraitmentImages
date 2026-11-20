"""Comparer le watershed fondé sur la distance et sur le gradient."""
import matplotlib.pyplot as plt
from skimage import filters, segmentation
from scipy import ndimage as ndi

from tp5b_outils import scene_cellules, verifier, enregistrer

image, masque, reference, marqueurs = scene_cellules()

# Choisir un essai ; chaque exécution repart des marqueurs d'origine.
essai = 'avec_5'  # 'initial', 'sans_2' ou 'avec_5'
if essai == 'sans_2':
    marqueurs[marqueurs == 2] = 0
elif essai == 'avec_5':
    marqueurs[62, 50] = 5  # Dans le premier objet, hors des marqueurs fournis.
elif essai != 'initial':
    raise ValueError('Choisissez initial, sans_2 ou avec_5.')

# TODO : calculer le gradient de l'image en niveaux de gris.
gradient = filters.sobel(image)
verifier(gradient)
# TODO : appliquer watershed à -distance puis au gradient, avec les mêmes marqueurs et masque.
distance = ndi.distance_transform_edt(image)
labels_distance =  segmentation.watershed(-distance, markers=marqueurs, mask=masque)
labels_gradient =  segmentation.watershed(gradient, markers=marqueurs, mask=masque)
verifier(distance)
verifier(labels_distance)
verifier(labels_gradient)

fig, axes = plt.subplots(1, 4, figsize=(12, 3.5))
for axe, donnees, titre, carte in [
    (axes[0], image, 'Image', 'gray'),
    (axes[1], gradient, 'Gradient', 'magma'),
    (axes[2], labels_distance, 'Relief -distance', 'nipy_spectral'),
    (axes[3], labels_gradient, 'Relief gradient', 'nipy_spectral'),
]:
    axe.imshow(donnees, cmap=carte)
    axe.set_title(titre)
    axe.axis('off')
enregistrer(fig, '02-comparaison-reliefs.png')
