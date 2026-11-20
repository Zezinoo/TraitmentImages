"""Séparer des cellules accolées avec un watershed sur la distance."""
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import measure, segmentation

from tp5b_outils import scene_cellules, verifier, enregistrer

image, masque, reference, marqueurs = scene_cellules()
# TODO : calculer la distance euclidienne au fond dans le masque.
distance = ndi.distance_transform_edt(image)
verifier(distance)
# TODO : appliquer le watershed au relief -distance, avec les marqueurs et le masque.
labels =  segmentation.watershed(-distance, markers=marqueurs, mask=masque)
verifier(labels)
composantes = measure.label(masque, connectivity=1)
print('Régions du masque par simple étiquetage :', composantes.max())
print('Régions séparées par le watershed :', labels.max())
print('Nombre d’objets de référence :', reference.max())

fig, axes = plt.subplots(1, 5, figsize=(14, 3.4))
for axe, donnees, titre, carte in [
    (axes[0], image, 'Image', 'gray'),
    (axes[1], masque, 'Masque', 'gray'),
    (axes[2], distance, 'Distance', 'viridis'),
    (axes[3], marqueurs, 'Marqueurs', 'nipy_spectral'),
    (axes[4], labels, 'Régions', 'nipy_spectral'),
]:
    axe.imshow(donnees, cmap=carte)
    axe.set_title(titre)
    axe.axis('off')
enregistrer(fig, '01-watershed-distance.png')
