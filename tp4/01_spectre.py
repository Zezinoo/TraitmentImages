"""Lire un spectre et vérifier la reconstruction des images."""
import numpy as np
from tp4_outils import charger_image, afficher_spectre, verifier

images = [
    ('01-bandes-verticales-32.png', 'Bandes verticales : période 32 pixels'),
    ('02-bandes-verticales-16.png', 'Bandes verticales : période 16 pixels'),
    ('03-bandes-horizontales-16.png', 'Bandes horizontales : période 16 pixels'),
    ('04-facade-reference.png', 'Façade'),
]
for nom, titre in images:
    image = charger_image(nom)
    # TODO : calculer la transformée de Fourier de image.
    spectre = np.fft.fft2(image)
    verifier(spectre)
    # TODO : calculer le module du spectre complexe.
    module = np.abs(spectre)
    verifier(module)
    # TODO : centrer le module pour l'affichage.
    module_centre = np.fft.fftshift(module)
    verifier(module_centre)
    # TODO : reconstruire depuis spectre, sans décalage ni logarithme.
    reconstruction = np.fft.ifft2(spectre)
    verifier(reconstruction)
    erreur = np.max(np.abs(image - reconstruction.real))
    residu = np.max(np.abs(reconstruction.imag))
    print(titre)
    print(f'  Écart absolu maximal : {erreur:.3e}')
    print(f'  Résidu imaginaire maximal : {residu:.3e}')
    afficher_spectre(image, module_centre, titre, nom)
