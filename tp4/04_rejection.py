"""Observer puis atténuer une perturbation périodique de la façade."""
import sys
import numpy as np
from tp4_outils import (charger_image, verifier, afficher_spectre,
                         afficher_rejection)

# TODO : renseigner les coordonnées fréquentielles d'un des deux pics.
frequence_x = 1/16
frequence_y = 0
rayon = 0.015

reference = charger_image('04-facade-reference.png')
image = charger_image('06-facade-periodique.png')
spectre_centre = np.fft.fftshift(np.fft.fft2(image))
for tableau, titre, nom in [
    (reference, 'Façade de référence', '04-observation-reference.png'),
    (image, 'Façade perturbée', '04-observation-perturbee.png'),
]:
    module = np.abs(np.fft.fftshift(np.fft.fft2(tableau)))
    afficher_spectre(tableau, module, titre, nom)

# La première exécution permet de lire les pics avant de compléter le traitement.
if frequence_x is None or frequence_y is None:
    print('Observation terminée. Renseignez frequence_x et frequence_y,')
    print('complétez le masque et la multiplication, puis relancez le script.')
    sys.exit(0)

fx = np.fft.fftshift(np.fft.fftfreq(image.shape[1]))
fy = np.fft.fftshift(np.fft.fftfreq(image.shape[0]))
frequences_x, frequences_y = np.meshgrid(fx, fy)
distance_positive = np.hypot(frequences_x-frequence_x, frequences_y-frequence_y)
distance_negative = np.hypot(frequences_x+frequence_x, frequences_y+frequence_y)
# TODO : conserver les coefficients hors des deux disques de rayon rayon.
masque = (distance_positive > rayon) & (distance_negative > rayon) 
verifier(masque)
# TODO : multiplier le spectre complexe centré par le masque.
spectre_filtre = masque * spectre_centre
verifier(spectre_filtre)
reconstruction = np.fft.ifft2(np.fft.ifftshift(spectre_filtre))
residu = np.max(np.abs(reconstruction.imag))
if residu > 1e-12:
    raise ValueError('Résidu imaginaire trop élevé : vérifier la symétrie du masque.')
corrigee = reconstruction.real

masque_gaussien = np.exp(-(frequences_x**2 + frequences_y**2)/(2*0.04**2))
passe_bas = np.fft.ifft2(np.fft.ifftshift(spectre_centre*masque_gaussien)).real
cas = [('Référence', reference), ('Perturbée', image),
       ('Réjecteur', corrigee), ('Passe-bas gaussien', passe_bas)]
print(f'Rayon : {rayon:.3f} cycle/pixel ; résidu imaginaire : {residu:.3e}')
for titre, resultat in cas[1:]:
    erreur = np.mean((reference-resultat)**2)
    print(f'{titre} : erreur quadratique moyenne (EQM) = {erreur:.8f}')
afficher_rejection(cas, masque, spectre_filtre, fx, fy, rayon)
