"""Compare Gaussian blurs and their differences from a smoothed test image."""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from scipy import ndimage
from skimage.color import rgb2gray

from tools import available_images, crop, load_image, slots

boxes = slots()


def draw_crops(ax):
    """Show the exact parking-space crops used for the measurements."""
    for slot_id, (x0, y0, x1, y1) in boxes.items():
        ax.add_patch(Rectangle(
            (x0 - 0.5, y0 - 0.5), x1 - x0, y1 - y0,
            fill=False, edgecolor="yellow", linewidth=0.8,
        ))
        ax.text(
            x0 + 2, y0 + 2, str(slot_id), color="yellow", fontsize=6,
            va="top", bbox=dict(facecolor="black", alpha=0.7, pad=0.5),
        )


def add_crop_statistics(ax, values):
    """Measure the displayed map within each crop; keep labels out of the image."""
    rows = []
    for slot_id, box in boxes.items():
        region = crop(values, box)
        rows.append([
            str(slot_id), f"{np.mean(region):.4f}", f"{np.median(region):.4f}",
        ])
    table = ax.table(
        cellText=rows, colLabels=["Space", "Mean", "Median"],
        cellLoc="center", bbox=[0, -0.72, 1, 0.68],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)


images = available_images()
filenames = {row["image_id"]: row["filename"] for row in images}

reference = load_image(next(row["filename"] for row in images
                                if row["image_id"] == "R00"))
reference = rgb2gray(reference)

TEST_IMAGE_ID = "C054"
TEST_SIGMA = 3
test_image = load_image(next(row["filename"] for row in images
                             if row["image_id"] == TEST_IMAGE_ID))
test_image = rgb2gray(test_image)
smoothed_test = ndimage.gaussian_filter(
    test_image, sigma=TEST_SIGMA, mode="reflect",
)

sigma = [1, 5, 10, 15, 20]

fig, axes = plt.subplots(
    1, len(sigma) + 1, figsize=(4 * (len(sigma) + 1), 4),
    sharex=True, sharey=True, squeeze=False, constrained_layout=True,
)
axes = axes[0]
axes[0].imshow(reference, cmap="gray", vmin=0, vmax=1)
axes[0].set_title("Grayscale (no blur)")

blurred_backgrounds = []
for ax, s in zip(axes[1:], sigma):
    # The grayscale image has only height and width dimensions.
    image = ndimage.gaussian_filter(reference, sigma=s, mode="reflect")
    blurred_backgrounds.append(image)
    ax.imshow(image, cmap="gray", vmin=0, vmax=1)
    ax.set_title(f"Sigma = {s} pixels")

for ax in axes:
    draw_crops(ax)
    ax.axis("off")

fig.suptitle("Gaussian blur comparison - empty reference R00")

# Keep signed floating-point differences: negative values must not be clipped.
differences = [smoothed_test - background for background in blurred_backgrounds]
# Grayscale has one value per pixel, so no reduction across RGB is needed.
signed_maps = differences
absolute_maps = [np.abs(difference) for difference in differences]

# Use the same display limits for every background sigma, for fair comparison.
signed_limit = max(float(np.max(np.abs(values))) for values in signed_maps)
absolute_limit = max(float(np.max(values)) for values in absolute_maps)
signed_limit = max(signed_limit, 1e-6)
absolute_limit = max(absolute_limit, 1e-6)

difference_fig, difference_axes = plt.subplots(
    2, len(sigma) + 1, figsize=(4 * (len(sigma) + 1), 14),
    sharex=True, sharey=True, constrained_layout=True,
)
difference_axes[0, 0].imshow(test_image, cmap="gray", vmin=0, vmax=1)
difference_axes[0, 0].set_title(f"Grayscale test image {TEST_IMAGE_ID}")
difference_axes[1, 0].imshow(smoothed_test, cmap="gray", vmin=0, vmax=1)
difference_axes[1, 0].set_title(f"Test blurred: sigma = {TEST_SIGMA}")

for column, (s, signed, absolute) in enumerate(
    zip(sigma, signed_maps, absolute_maps), start=1,
):
    signed_plot = difference_axes[0, column].imshow(
        signed, cmap="RdBu_r", vmin=-signed_limit, vmax=signed_limit,
    )
    difference_axes[0, column].set_title(
        f"Test sigma {TEST_SIGMA} - reference sigma {s}\nSigned grayscale difference",
    )
    absolute_plot = difference_axes[1, column].imshow(
        absolute, cmap="gray", vmin=0, vmax=absolute_limit,
    )
    difference_axes[1, column].set_title(
        f"Reference sigma = {s}\nAbsolute grayscale difference",
    )
    add_crop_statistics(difference_axes[0, column], signed)
    add_crop_statistics(difference_axes[1, column], absolute)

for ax in difference_axes.flat:
    draw_crops(ax)
    ax.axis("off")

difference_fig.colorbar(
    signed_plot, ax=list(difference_axes[0, 1:]), shrink=0.7,
    label="Blue: test darker | Red: test brighter",
)
difference_fig.colorbar(
    absolute_plot, ax=list(difference_axes[1, 1:]), shrink=0.7,
    label="Black: little change | White: large change",
)
difference_fig.suptitle(
    f"Smoothed {TEST_IMAGE_ID} minus smoothed R00 - shared scales across each row",
)
plt.show()
