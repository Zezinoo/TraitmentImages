"""Study global histogram equalization."""

import matplotlib.pyplot as plt
from skimage import exposure

from tp2_support import add_cumulative_distribution, add_histogram, load_gray, print_stats, save_figure


reference = load_gray("02-circuit.jpg")
# Reduce the intensity range to create a low-contrast case.
low_contrast = 0.35 + 0.30 * reference
equalized = exposure.equalize_hist(low_contrast, nbins=256)

cases = [
    ("Reference", reference),
    ("Reduced contrast", low_contrast),
    ("Global equalization", equalized),
]

fig, axes = plt.subplots(3, 3, figsize=(12, 10))
for row, (label, image) in enumerate(cases):
    axes[row, 0].imshow(image, cmap="gray", vmin=0, vmax=1)
    axes[row, 0].set_title(label)
    axes[row, 0].axis("off")
    add_histogram(axes[row, 1], image, bins=64)
    axes[row, 1].set_title("Histogram")
    add_cumulative_distribution(axes[row, 2], image, bins=64)
    axes[row, 2].set_title("Cumulative proportion")

fig.suptitle("Global equalization remaps intensities across the whole image", fontsize=15)
fig.tight_layout()
save_figure(fig, "04-egalisation-globale.png")

for label, image in cases:
    print_stats(label, image)
