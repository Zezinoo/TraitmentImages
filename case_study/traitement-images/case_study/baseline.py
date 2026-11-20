"""Simple comparison method, separate from each team's personal pipeline."""

import numpy as np

from tools import crop


DECISION_THRESHOLD = 0.09


def predict(image, reference, box):
    """Return (score, decision) for one parking slot.

    The reference shows this slot empty. This baseline compares the mean of
    all three RGB channels. It does not account for shadows, lighting changes,
    or the spatial structure of a vehicle. Keep this method unchanged when
    comparing its results with those of your own pipeline.
    """
    current = crop(image, box)
    empty = crop(reference, box)
    score = float(abs(np.mean(current) - np.mean(empty)))
    decision = int(score > DECISION_THRESHOLD)
    return score, decision
