"""Each team's personal pipeline, to design using the images and lab methods."""

import numpy as np
from scipy import ndimage
from skimage.color import rgb2gray

from tools import crop


DECISION_THRESHOLD = 0.11


def predict(image, reference, box):
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

    smoothed_current = ndimage.gaussian_filter(current, sigma=3, mode='reflect')
    smoothed_empty =  ndimage.gaussian_filter(empty, sigma=20 , mode='reflect')

    difference = smoothed_current - smoothed_empty
    decision = np.mean(np.abs(difference) )

    score = float(decision)   
    decision = int(score > DECISION_THRESHOLD)


    return score, decision
