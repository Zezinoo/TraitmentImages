"""Comparer les modules et les phases lors d'une translation circulaire."""
import numpy as np
from tp4_outils import charger_image, verifier, afficher_translation

dy, dx = 20, 30
for nom, titre in [('05-rectangle.png', 'Rectangle'),
                   ('04-facade-reference.png', 'Façade')]:
    image = charger_image(nom)
    spectre = np.fft.fft2(image)
    # TODO : déplacer circulairement les lignes de dy et les colonnes de dx.
    deplacee = np.roll(image , shift=(dx , dy) , axis=(0,1))
    verifier(deplacee)
    # TODO : calculer le spectre de l'image déplacée.
    spectre_deplace = np.fft.fft2(deplacee)
    verifier(spectre_deplace)
    module = np.abs(spectre)
    ecart = np.max(np.abs(module - np.abs(spectre_deplace)))
    maximum = np.max(module)
    # L'image nulle possède un spectre nul : éviter une division par zéro.
    ecart_relatif = ecart / maximum if maximum > 0 else ecart
    reconstruction = np.fft.ifft2(spectre)
    reconstruction_deplacee = np.fft.ifft2(spectre_deplace)
    print(titre)
    print(f'  Écart relatif entre modules : {ecart_relatif:.3e}')
    for etiquette, entree, sortie in [
        ('Initiale', image, reconstruction),
        ('Déplacée', deplacee, reconstruction_deplacee),
    ]:
        print(f'  {etiquette} : erreur réelle = '
              f'{np.max(np.abs(entree - sortie.real)):.3e}, '
              f'résidu imaginaire = {np.max(np.abs(sortie.imag)):.3e}')
    # Coefficient de ligne 1, colonne 1 dans le spectre non centré.
    indice = (1, 1)
    if maximum > 0 and module[indice] > 1e-6 * maximum:
        print('  Coefficient (ligne 1, colonne 1) :')
        print(f'    Module relatif : {module[indice] / maximum:.3e}')
        print(f'    Phase initiale : {np.angle(spectre[indice]):.6f} rad')
        print(f'    Phase après déplacement : '
              f'{np.angle(spectre_deplace[indice]):.6f} rad')
    else:
        print('  Coefficient négligeable : phase non interprétée.')
    afficher_translation(image, deplacee, spectre, spectre_deplace,
                         reconstruction.real, reconstruction_deplacee.real,
                         titre, '02-translation-' + nom)
