"""Study local equalization parameters."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from skimage import exposure

from tp2_support import load_gray, save_figure


TILE_SIZES = (32, 64, 128)
CLIP_LIMITS = (0.01, 0.04)
ANALYSIS_REGION = (420, 220, 480, 280)  # x0, y0, x1, y1


def local_std(image):
    x0, y0, x1, y1 = ANALYSIS_REGION

    # TODO : extract the region using NumPy slicing and compute its standard deviation
    patch = image[y0:y1, x0:x1]
    return np.std(patch)

image = load_gray("05-image-bruitee.jpg")
global_equalized = exposure.equalize_hist(image, nbins=256)
cases = [("Original", image), ("Global equalization", global_equalized)]

for label, result in cases:
    print(f"{label:24s} local standard deviation = {local_std(result):.4f}")

for tile_size in TILE_SIZES:
    for clip_limit in CLIP_LIMITS:
        result = exposure.equalize_adapthist(
            image, kernel_size=tile_size, clip_limit=clip_limit
        )
        cases.append((f"Tile size={tile_size}, limit={clip_limit:g}", result))
        print(
            f"Tile size={tile_size:3d}, limit={clip_limit:.2f} : "
            f"local standard deviation = {local_std(result):.4f}"
        )

fig, axes = plt.subplots(4, 2, figsize=(11, 15))
for axis, (title, result) in zip(axes.flat, cases):
    axis.imshow(result, cmap="gray", vmin=0, vmax=1)
    axis.set_title(title)
    axis.axis("off")
    if title == "Original":
        x0, y0, x1, y1 = ANALYSIS_REGION
        axis.add_patch(
            Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, edgecolor="red", linewidth=2)
        )

fig.suptitle("Effect of tile size and clip limit", fontsize=15)
fig.tight_layout(rect=(0, 0, 1, 0.97))
save_figure(fig, "08-etude-parametres-clahe.png")

# Show enlarged views of the same region to compare fluctuations.
x0, y0, x1, y1 = ANALYSIS_REGION
fig, axes = plt.subplots(2, 4, figsize=(13, 7))
for axis, (title, result) in zip(axes.flat, cases):
    axis.imshow(result[y0:y1, x0:x1], cmap="gray", vmin=0, vmax=1,
                interpolation="nearest")
    axis.set_title(title)
    axis.axis("off")
fig.suptitle("Same region, same grayscale range")
fig.tight_layout()
save_figure(fig, "08-regions-agrandies.png")
