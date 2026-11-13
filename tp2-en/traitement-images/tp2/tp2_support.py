from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


SCRIPT_DIR = Path(__file__).resolve().parent
STUDENT_ROOT = SCRIPT_DIR.parent
RESOURCE_DIR = STUDENT_ROOT / f"ressources-{SCRIPT_DIR.name}"
if not RESOURCE_DIR.exists():
    RESOURCE_DIR = STUDENT_ROOT / "ressources"
RESULTS_DIR = SCRIPT_DIR / "resultats"


def load_gray(filename):
    """Load a teaching image as grayscale values in [0, 1]."""
    path = RESOURCE_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing image resource: {path}")
    with Image.open(path) as source:
        image = np.asarray(source.convert("L"), dtype=np.float32) / 255.0
    return image


def histogram_data(image, bins=64):
    """Compute bin proportions, centers, and cumulative proportions."""
    counts, edges = np.histogram(image.ravel(), bins=bins, range=(0.0, 1.0))
    probability = counts / counts.sum()
    centers = (edges[:-1] + edges[1:]) / 2
    return probability, centers, np.cumsum(probability)


def add_histogram(axis, image, bins=64, label=None, color=None):
    probability, centers, _ = histogram_data(image, bins=bins)
    axis.step(centers, probability, where="mid", label=label, color=color)
    axis.set(xlim=(0, 1), xlabel="Gray level", ylabel="Fraction of pixels")
    axis.grid(alpha=0.2)


def add_cumulative_distribution(axis, image, bins=64, label=None, color=None):
    _, centers, cumulative = histogram_data(image, bins=bins)
    width = centers[1] - centers[0]
    upper_edges = centers + width / 2
    axis.step(np.r_[0, upper_edges], np.r_[0, cumulative], where="post", label=label, color=color)
    axis.set(xlim=(0, 1), ylim=(0, 1), xlabel="Gray level", ylabel="Cumulative proportion")
    axis.grid(alpha=0.2)


def plot_histogram_data(axis, centers, probability, label=None, color=None):
    axis.step(centers, probability, where="mid", label=label, color=color)
    axis.set(xlim=(0, 1), xlabel="Gray level", ylabel="Fraction of pixels")
    axis.grid(alpha=0.2)


def plot_cumulative_data(axis, centers, cumulative, label=None, color=None):
    width = centers[1] - centers[0]
    upper_edges = centers + width / 2
    axis.step(np.r_[0, upper_edges], np.r_[0, cumulative], where="post", label=label, color=color)
    axis.set(xlim=(0, 1), ylim=(0, 1), xlabel="Gray level", ylabel="Cumulative proportion")
    axis.grid(alpha=0.2)


def compare_images_and_histograms(cases, title, filename, bins=64):
    """Display images and histograms on shared scales."""
    fig, axes = plt.subplots(2, len(cases), figsize=(3.4 * len(cases), 6))
    for column, (label, image) in enumerate(cases):
        axes[0, column].imshow(image, cmap="gray", vmin=0, vmax=1)
        axes[0, column].set_title(label)
        axes[0, column].axis("off")
        add_histogram(axes[1, column], image, bins=bins)
        axes[1, column].set_title("Histogram")
    ymax = max(axis.get_ylim()[1] for axis in axes[1])
    for axis in axes[1]:
        axis.set_ylim(0, ymax)
    fig.suptitle(title, fontsize=15)
    fig.tight_layout()
    save_figure(fig, filename)


def save_figure(fig, filename):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    path = RESULTS_DIR / filename
    fig.savefig(path, dpi=160, bbox_inches="tight")
    print(f"Saved figure: {path}")
    plt.show()


def print_stats(label, image):
    q1, q99 = np.percentile(image, [1, 99])
    print(
        f"{label:24s} mean={image.mean():.3f}  std={image.std():.3f}  "
        f"q99-q1={q99-q1:.3f}  [q1={q1:.3f}, q99={q99:.3f}]"
    )


def load_rgb(filename):
    """Load red, green, and blue channels in [0, 1]."""
    with Image.open(RESOURCE_DIR / filename) as source:
        return np.asarray(source.convert("RGB"), dtype=np.float64) / 255.0


def compare_rgb_cases(cases, distributions, filename):
    """Lay out images and computed histograms."""
    fig, axes = plt.subplots(2, len(cases), figsize=(4.5 * len(cases), 7), squeeze=False)
    for column, ((label, rgb), (centers, frequencies)) in enumerate(zip(cases, distributions)):
        axes[0, column].imshow(rgb)
        axes[0, column].set_title(label)
        axes[0, column].axis("off")
        for k, (color, name) in enumerate(zip(("red", "green", "blue"), ("R", "G", "B"))):
            axes[1, column].step(centers, frequencies[k], where="mid", color=color, label=name)
        axes[1, column].set(xlim=(0, 1), xlabel="Channel value", ylabel="Fraction of channel pixels")
        axes[1, column].legend()
        axes[1, column].grid(alpha=0.2)
    ymax = max(axis.get_ylim()[1] for axis in axes[1])
    for axis in axes[1]:
        axis.set_ylim(0, ymax)
    fig.tight_layout()
    save_figure(fig, filename)
