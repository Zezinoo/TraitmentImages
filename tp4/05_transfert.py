"""Adapter la réjection à deux perturbations d'une image de circuit."""
import sys
import numpy as np
from tp4_outils import charger_image, verifier, afficher_spectre, afficher_rejection

# TODO : remplacer chaque None par un couple (fréquence x, fréquence y).
centres = [(0,1/16), (1/32 , 1/32)]
# Commencer avec une paire, puis passer à deux pour la question 3.
nombre_paires = 2
rayon = 0.015

reference = charger_image('07-circuit-reference.png')
image = charger_image('08-circuit-periodique.png')
spectre_centre = np.fft.fftshift(np.fft.fft2(image))
for tableau, titre, nom in [
    (reference, 'Circuit de référence', '05-observation-reference.png'),
    (image, 'Circuit perturbé', '05-observation-perturbe.png'),
]:
    afficher_spectre(tableau, np.abs(np.fft.fftshift(np.fft.fft2(tableau))), titre, nom)
if nombre_paires not in (1, 2):
    raise ValueError('Choisissez une ou deux paires.')
if any(centre is None for centre in centres[:nombre_paires]):
    print('Observation terminée. Renseignez les centres des paires à rejeter,')
    print('complétez les masques et les multiplications, puis relancez.')
    sys.exit(0)

fx = np.fft.fftshift(np.fft.fftfreq(image.shape[1]))
fy = np.fft.fftshift(np.fft.fftfreq(image.shape[0]))
frequences_x, frequences_y = np.meshgrid(fx, fy)


def construire_masque(frequence_x, frequence_y):
    distance_positive = np.hypot(frequences_x-frequence_x, frequences_y-frequence_y)
    distance_negative = np.hypot(frequences_x+frequence_x, frequences_y+frequence_y)
    # TODO : reprendre la construction d'un masque symétrique de l'activité 4.
    masque = (distance_positive > rayon) & (distance_negative > rayon) 
    return verifier(masque)


masque_total = np.ones(image.shape)
for frequence_x, frequence_y in centres[:nombre_paires]:
    masque_paire = construire_masque(frequence_x, frequence_y)
    # TODO : multiplier le masque total courant par celui de cette paire.
    masque_total = masque_total * masque_paire
    verifier(masque_total)
# TODO : filtrer le spectre complexe de l'image perturbée initiale.
spectre_filtre = spectre_centre * masque_total
verifier(spectre_filtre)
reconstruction = np.fft.ifft2(np.fft.ifftshift(spectre_filtre))
residu = np.max(np.abs(reconstruction.imag))
if residu > 1e-12:
    raise ValueError('Résidu imaginaire trop élevé : vérifier la symétrie des masques.')
corrigee = reconstruction.real
print(f'{nombre_paires} paire(s), rayon {rayon:.3f} ; résidu imaginaire : {residu:.3e}')
for titre, resultat in [('Perturbée', image), ('Corrigée', corrigee)]:
    print(f'{titre} : erreur quadratique moyenne (EQM) = '
          f'{np.mean((reference-resultat)**2):.8f}')
cas = [('Référence', reference), ('Perturbée', image),
       (f'Rejet de {nombre_paires} paire(s)', corrigee)]
afficher_rejection(cas, masque_total, spectre_filtre, fx, fy, rayon,
                   prefixe=f'05-{nombre_paires}paires', region=(120, 180, 160, 160))
