"""Combiner les modules et les phases de deux images distinctes."""
import numpy as np
from tp4_outils import charger_image, verifier, afficher_hybrides

facade = charger_image('04-facade-reference.png')
circuit = charger_image('07-circuit-reference.png')
if facade.shape != circuit.shape:
    raise ValueError('Les deux images doivent avoir les mêmes dimensions.')
spectre_facade = np.fft.fft2(facade)
spectre_circuit = np.fft.fft2(circuit)

# TODO : conserver le module de la façade et utiliser la phase du circuit.
hybride_1 = np.abs(spectre_facade)*np.exp(1j*np.angle(spectre_circuit))
verifier(hybride_1)
# TODO : conserver le module du circuit et utiliser la phase de la façade.
hybride_2 = np.abs(spectre_circuit)*np.exp(1j*np.angle(spectre_facade))
verifier(hybride_2)

images_hybrides = []
for titre, spectre_hybride, spectre_module in [
    ('Module façade, phase circuit', hybride_1, spectre_facade),
    ('Module circuit, phase façade', hybride_2, spectre_circuit),
]:
    module_attendu = np.abs(spectre_module)
    ecart = np.max(np.abs(np.abs(spectre_hybride) - module_attendu))
    maximum = module_attendu.max()
    ecart_relatif = ecart / maximum if maximum > 0 else ecart
    reconstruction = np.fft.ifft2(spectre_hybride)
    residu = np.max(np.abs(reconstruction.imag))
    print(titre)
    print(f'  Écart relatif entre modules : {ecart_relatif:.3e}')
    print(f'  Résidu imaginaire maximal : {residu:.3e}')
    if residu > 1e-12:
        raise ValueError('Résidu imaginaire trop élevé : vérifier les combinaisons.')
    image = reconstruction.real
    print(f'  Minimum : {image.min():.6f} ; maximum : {image.max():.6f}')
    images_hybrides.append(image)

# Toutes les valeurs reconstruites restent disponibles sans écrêtage.
afficher_hybrides(facade, circuit, *images_hybrides)
