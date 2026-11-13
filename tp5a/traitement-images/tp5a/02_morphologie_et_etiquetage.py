"""Observer l'effet du nettoyage morphologique et de la connexité."""
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import measure, morphology

from tp5a_outils import scene_bruitee, verifier, enregistrer

reference, bruit = scene_bruitee()
# TODO : appliquer une ouverture avec un disque de rayon 2.
ouverture = None
verifier(ouverture)
# TODO : appliquer une fermeture avec un disque de rayon 2 au masque d'origine.
fermeture = None
verifier(fermeture)
# TODO : étiqueter la référence en 4-connexité, puis en 8-connexité.
labels_4 = None
labels_8 = None
verifier(labels_4)
verifier(labels_8)
print('Composantes -- référence 4/8 :', labels_4.max(), labels_8.max())
print('Composantes -- bruit 4/8 :', measure.label(bruit, connectivity=1).max(),
      measure.label(bruit, connectivity=2).max())
print('Composantes -- ouverture 4/8 :',
      measure.label(ouverture, connectivity=1).max(),
      measure.label(ouverture, connectivity=2).max())
print('Composantes -- fermeture 4/8 :',
      measure.label(fermeture, connectivity=1).max(),
      measure.label(fermeture, connectivity=2).max())

fig, axes = plt.subplots(1, 4, figsize=(12, 3.4))
for axe, image, titre in zip(axes, (reference, bruit, ouverture, fermeture),
                             ('Référence', 'Masque bruité', 'Ouverture', 'Fermeture')):
    axe.imshow(image, cmap='gray', vmin=0, vmax=1)
    axe.set_title(titre)
    axe.axis('off')
enregistrer(fig, '02-morphologie.png')
