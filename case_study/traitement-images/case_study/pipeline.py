"""Each team's personal pipeline, to design using the images and lab methods."""

import numpy as np

from tools import crop


DECISION_THRESHOLD = 0.09


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
    current = crop(image, box)
    empty = crop(reference, box)
    score = float(abs(np.mean(current) - np.mean(empty)))
    decision = int(score > DECISION_THRESHOLD)
    return score, decision
