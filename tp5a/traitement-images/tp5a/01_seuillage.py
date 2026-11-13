"""Comparer le seuil d'Otsu sur un fond uniforme et un fond variable."""
import matplotlib.pyplot as plt
from skimage import filters

from tp5a_outils import scene_uniforme, scene_eclairee, verifier, enregistrer, iou

fig, axes = plt.subplots(2, 4, figsize=(14, 6))
image, reference = scene_uniforme()
# TODO : calculer le seuil d'Otsu et le masque d'objets clairs.
seuil = None
masque = None
verifier(seuil)
verifier(masque)
faux_objets = (masque & ~reference).sum()
objets_manques = (~masque & reference).sum()
print(f'Fond uniforme: seuil={seuil:.4f}, IoU={iou(masque, reference):.4f}, '
      f'faux objets={faux_objets}, pixels objets manqués={objets_manques}')
for axe, donnees, titre in zip(axes[0, :3], (image, reference, masque),
                               ('Image', 'Référence', 'Masque d’Otsu')):
    axe.imshow(donnees, cmap='gray', vmin=0, vmax=1)
    axe.set_title(titre)
    axe.axis('off')
axes[0, 3].axis('off')

image, reference = scene_eclairee()
# TODO : calculer le masque d'Otsu pour des objets sombres.
seuil_otsu = None
masque_otsu = None
verifier(seuil_otsu)
verifier(masque_otsu)
# TODO : calculer le seuil local de Sauvola (fenêtre 41, k=0.2, r=0.5) et son masque sombre.
seuil_sauvola = None
masque_sauvola = None
verifier(seuil_sauvola)
verifier(masque_sauvola)
for nom, resultat in [('Otsu', masque_otsu), ('Sauvola', masque_sauvola)]:
    print(f'Fond variable, {nom}: IoU={iou(resultat, reference):.4f}, '
          f'faux objets={(resultat & ~reference).sum()}, '
          f'pixels objets manqués={(~resultat & reference).sum()}')
for axe, donnees, titre in zip(axes[1], (image, reference, masque_otsu, masque_sauvola),
                               ('Image', 'Référence', 'Otsu', 'Sauvola')):
    axe.imshow(donnees, cmap='gray', vmin=0, vmax=1)
    axe.set_title(titre)
    axe.axis('off')
enregistrer(fig, '01-seuillage.png')
