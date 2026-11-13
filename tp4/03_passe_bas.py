"""Comparer les filtres passe-bas idéal et gaussien."""
import numpy as np
from tp4_outils import charger_image, verifier, afficher_passe_bas

for nom, titre in [('05-rectangle.png', 'Rectangle'),
                   ('04-facade-reference.png', 'Façade')]:
    image = charger_image(nom)
    fx = np.fft.fftshift(np.fft.fftfreq(image.shape[1]))
    fy = np.fft.fftshift(np.fft.fftfreq(image.shape[0]))
    frequences_x, frequences_y = np.meshgrid(fx, fy)
    distance = np.hypot(frequences_x, frequences_y)
    spectre_centre = np.fft.fftshift(np.fft.fft2(image))
    resultats = []
    for frequence_limite in (0.04, 0.10):
        # TODO : conserver les fréquences dont distance <= frequence_limite.
        masque_ideal = distance < frequence_limite
        verifier(masque_ideal)
        # TODO : appliquer la formule du masque gaussien avec np.exp.
        masque_gaussien = np.exp(-distance**2/(2*frequence_limite*2))
        verifier(masque_gaussien)
        for methode, masque in [('Idéal', masque_ideal),
                                ('Gaussien', masque_gaussien)]:
            # TODO : multiplier le spectre complexe centré par le masque.
            spectre_filtre = spectre_centre * masque
            verifier(spectre_filtre)
            reconstruction = np.fft.ifft2(np.fft.ifftshift(spectre_filtre))
            residu = np.max(np.abs(reconstruction.imag))
            if residu > 1e-12:
                raise ValueError('Résidu imaginaire trop élevé : vérifier le masque.')
            filtree = reconstruction.real
            print(f'{titre}, {methode}, f0={frequence_limite:.2f} : '
                  f'min={filtree.min():.6f}, max={filtree.max():.6f}, '
                  f'résidu imaginaire={residu:.3e}')
            # Les valeurs calculées sont conservées sans écrêtage.
            resultats.append((methode, frequence_limite, masque, filtree))
    afficher_passe_bas(image, resultats, titre, nom, fx, fy,
                       ligne_profil=100 if nom == '05-rectangle.png' else None)
