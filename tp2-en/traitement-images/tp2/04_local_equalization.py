"""Compare global and local contrast on a house and a noisy image."""

import matplotlib.pyplot as plt
from skimage import exposure

from tp2_support import add_histogram, load_gray, save_figure

# Both limits are compared in the same figure.
CLIP_LIMITS = (0.01, 0.04)
TILE_SIZE = 64

# Study the house first, then the noisy image.
IMAGE_FILE = "05-image-bruitee.jpg"
# IMAGE_FILE = "05-image-bruitee.jpg"
image = load_gray(IMAGE_FILE)
global_equalized = exposure.equalize_hist(image, nbins=256)
local_results = [
    exposure.equalize_adapthist(image, kernel_size=TILE_SIZE, clip_limit=limit, nbins=256)
    for limit in CLIP_LIMITS
]

cases = [("Original", image), ("Global equalization", global_equalized)]
cases.extend((f"CLAHE - clip={limit:g}", result) for limit, result in zip(CLIP_LIMITS, local_results))

fig, axes = plt.subplots(2, 4, figsize=(15, 7))
for column, (label, result) in enumerate(cases):
    axes[0, column].imshow(result, cmap="gray", vmin=0, vmax=1)
    axes[0, column].set_title(label)
    axes[0, column].axis("off")
    add_histogram(axes[1, column], result, bins=64)
    axes[1, column].set_title("Global histogram")

fig.suptitle(f"Global equalization and CLAHE - tile size: {TILE_SIZE}", fontsize=15)
fig.tight_layout()
save_figure(fig, f"04-contraste-local-{IMAGE_FILE.rsplit('.', 1)[0]}.png")
