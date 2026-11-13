"""Optional extension: implement global equalization."""

import matplotlib.pyplot as plt
import numpy as np
from skimage import exposure

from tp2_support import load_gray, save_figure


image = load_gray("03-maison-reference.png")
image = 0.35 + 0.30 * image
nbins = 256

# TODO 1 : compute the histogram over [0, 1]
counts , edges = np.histogram(image.ravel(), bins=nbins, range=(image.min(), image.max()))

# TODO 2 : normalize the counts so that their sum is 1
probability = counts / counts.sum()

# TODO 3 : compute the cumulative distribution
cumulative = np.cumsum(probability)

# TODO 4 : map intensities by interpolating cumulative proportions at bin centers
centers = (edges[:-1] + edges[1:]) / 2
equalized_manual = np.interp(image, centers, cumulative)

# For each pixel intensity p, find the two bin centers surrounding it.
# Compute how far p lies between those centers, then use the same fraction
# between their cumulative proportions to get the pixel's new intensity.
# Values outside the bin centers use the nearest endpoint value.

if equalized_manual is not None:
    reference = exposure.equalize_hist(image, nbins=nbins)
    difference = np.abs(equalized_manual - reference)
    print(f"Mean absolute difference from scikit-image: {difference.mean():.6f}")

    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for axis, result, title in zip(
        axes,
        [image, equalized_manual, reference],
        ["Reduced contrast", "Your result", "scikit-image"],
    ):
        axis.imshow(result, cmap="gray", vmin=0, vmax=1)
        axis.set_title(title)
        axis.axis("off")
    fig.tight_layout()
    save_figure(fig, "07-egalisation-manuelle.png")
