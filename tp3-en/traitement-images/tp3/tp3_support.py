"""Shared plotting helpers. The calculations requested in the lab stay in each script."""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
RESOURCE_DIR = SCRIPT_DIR.parent / 'ressources-tp3'
if not RESOURCE_DIR.exists():
    RESOURCE_DIR = SCRIPT_DIR.parent / 'ressources'
RESULTS_DIR = SCRIPT_DIR / 'resultats'


def load_image(filename):
    with Image.open(RESOURCE_DIR / filename) as source:
        return np.asarray(source.convert('L'), dtype=float) / 255


def require(value):
    if value is None:
        raise NotImplementedError('Complete the TODO calculations before running the script.')
    return value


def save_figure(figure, filename):
    RESULTS_DIR.mkdir(exist_ok=True)
    figure.tight_layout()
    figure.savefig(RESULTS_DIR / filename, dpi=150, bbox_inches='tight')
    print('Saved figure:', RESULTS_DIR / filename)
    plt.show()


def compare_images(cases, filename, region=None):
    rows = 2 if region is not None else 1
    figure, axes = plt.subplots(rows, len(cases), figsize=(4 * len(cases), 3.3 * rows), squeeze=False)
    for column, (title, image) in enumerate(cases):
        require(image)
        axes[0, column].imshow(image, cmap='gray', vmin=0, vmax=1)
        axes[0, column].set_title(title)
        axes[0, column].axis('off')
        if region is not None:
            x0, y0, x1, y1 = region
            axes[0, column].add_patch(plt.Rectangle((x0, y0), x1-x0, y1-y0, fill=False, color='red'))
            axes[1, column].imshow(image[y0:y1, x0:x1], cmap='gray', vmin=0, vmax=1, interpolation='nearest')
            axes[1, column].set_title('Selected region')
            axes[1, column].axis('off')
    save_figure(figure, filename)


def show_profiles(cases, row, filename):
    figure, axis = plt.subplots(figsize=(10, 3.5))
    for title, image in cases:
        axis.plot(image[row, :], label=title)
    lower = min(0.0, min(float(image[row, :].min()) for _, image in cases)) - 0.05
    upper = max(1.0, max(float(image[row, :].max()) for _, image in cases)) + 0.05
    axis.set(xlabel='Column x', ylabel='Intensity', title=f'Intensity profile at row {row}', ylim=(lower, upper))
    axis.grid(alpha=0.25)
    axis.legend()
    save_figure(figure, filename)


def compare_gradients(cases, magnitudes, filename):
    figure, axes = plt.subplots(2, len(cases), figsize=(4*len(cases), 7), squeeze=False)
    maximum = max(float(require(magnitude).max()) for magnitude in magnitudes)
    for column, ((title, image), magnitude) in enumerate(zip(cases, magnitudes)):
        axes[0, column].imshow(image, cmap='gray', vmin=0, vmax=1)
        axes[0, column].set_title(title)
        axes[1, column].imshow(magnitude, cmap='gray', vmin=0, vmax=maximum)
        axes[1, column].set_title('Gradient magnitude, shared scale')
    for axis in axes.flat:
        axis.axis('off')
    save_figure(figure, filename)
