"""Each team's personal pipeline, to design using the images and lab methods."""

import numpy as np
from scipy import ndimage
from skimage import filters, color
from skimage.color import rgb2gray

from tools import crop


DECISION_THRESHOLD = 0.1


def predict_Gaussian(image, reference, box):
    """Return (score, decision) for one parking slot.

    image and reference: floating-point RGB arrays in [0, 1], with shape
    (750, 1000, 3). The reference shows all eight monitored spaces empty.
    box: (x0, y0, x1, y1), with exclusive upper bounds x1 and y1.
    score: a finite number; higher values indicate more likely occupancy.
    decision: integer 0 (empty) or 1 (occupied).

    The initial code uses the baseline's RGB mean comparison. You may modify
    it, rewrite this function entirely, and add your own modules.

    TODO: design, explain, and compare your own method. Keep this signature
    and the convention 1=occupied, 0=empty for the shared evaluation tools.
    """
    current = rgb2gray(crop(image, box))
    empty = rgb2gray(crop(reference, box))

    smoothed_current = ndimage.gaussian_filter(
        current, sigma=3, mode="reflect"
    )
    smoothed_empty = ndimage.gaussian_filter(
        empty, sigma=20, mode="reflect"
    )

    difference = smoothed_current - smoothed_empty
    score = float(np.mean(np.abs(difference)))
    decision = int(score > DECISION_THRESHOLD)

    return score, decision


def predict_Sauvola(image, reference, box):
    """Return (score, decision) for one parking slot.

    The reference shows this slot empty. This baseline compares the mean of
    all three RGB channels. It does not account for shadows, lighting changes,
    or the spatial structure of a vehicle. Keep this method unchanged when
    comparing its results with those of your own pipeline.
    """
    current = crop(image, box)
    empty = crop(reference, box)

    current = color.rgb2gray(current)
    empty = color.rgb2gray(empty)

    # On évalue les valeurs de Sauvola.
    seuil_sauvola = filters.threshold_sauvola(
        current, window_size=41, k=0.2, r=0.5
    )
    masque_sauvola = current < seuil_sauvola

    # On fait un seuillage sur l'image de référence.
    empty_threshold = filters.threshold_sauvola(
        empty, window_size=41, k=0.2, r=0.5
    )

    # Ici, on a les pixels sombres qui existaient avant les voitures.
    empty_mask = empty < empty_threshold

    # On ne garde que les pixels sombres qui n'existaient pas avant les voitures.
    new_pixels = masque_sauvola & ~empty_mask

    # On regarde la proportion de nouveaux pixels parmi tous les pixels présents.
    score = float(np.mean(new_pixels))
    print(score)

    decision = int(score > DECISION_THRESHOLD)

    return score, decision


def predict(image, reference, box):
    gaussian_result = predict_Gaussian(image, reference, box)
    sauvola_result = predict_Sauvola(image, reference, box)

    if gaussian_result[1] == sauvola_result[1]:
        final_decision = gaussian_result[1]
        final_score = sauvola_result[0]
    else:
        final_score = (gaussian_result[0] + sauvola_result[0]) / 2
        final_decision = int(final_score > DECISION_THRESHOLD)

    return final_score, final_decision