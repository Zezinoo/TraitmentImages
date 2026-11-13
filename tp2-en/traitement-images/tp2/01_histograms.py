"""Compare grayscale images and their histograms."""

import matplotlib.pyplot as plt
import numpy as np

from tp2_support import load_gray, plot_cumulative_data, plot_histogram_data, save_figure


# Change this value to compare coarse and detailed histograms.
N_BINS = 256

images = [
    ("Disk", load_gray("01-disque.png")),
    ("Circuit", load_gray("02-circuit.jpg")),
    ("House", load_gray("03-maison-reference.png")),
    ("MRI slice", load_gray("06-coupe-irm-affichage.png")),
]


def compute_distribution(image, bins):
    counts, edges = np.histogram(image.ravel(), bins=bins, range=(0.0, 1.0))

    # TODO 1 : normalize counts so that proportions sum to 1
    probability = counts / counts.sum()

    # TODO 2 : compute cumulative proportions
    cumulative = np.cumsum(probability)
    centers = (edges[:-1] + edges[1:]) / 2
    return centers, probability, cumulative

def plot_images():
    fig, axes = plt.subplots(len(images), 3, figsize=(12, 12))
    for row, (name, image) in enumerate(images):
        axes[row, 0].imshow(image, cmap="gray", vmin=0, vmax=1)
        axes[row, 0].set_title(name)
        axes[row, 0].axis("off")

        centers, probability, cumulative = compute_distribution(image, N_BINS)
        plot_histogram_data(axes[row, 1], centers, probability)
        axes[row, 1].set_title(f"Histogram - {N_BINS} bins")

        plot_cumulative_data(axes[row, 2], centers, cumulative)
        axes[row, 2].set_title("Cumulative proportion")

    fig.suptitle("Intensity distributions do not describe pixel positions", fontsize=15)
    fig.tight_layout()
    save_figure(fig, "01-analyse-histogrammes.png")

    # Shuffle disk pixels without changing their values.
    

def plot_shuffled_disk():
    disk = images[0][1]
    shuffled = np.random.default_rng(2025).permutation(disk.ravel()).reshape(disk.shape)
    fig, axes = plt.subplots(2, 2, figsize=(9, 7))
    axes[0, 0].imshow(disk, cmap="gray", vmin=0, vmax=1)
    axes[0, 0].set_title("Original disk")
    axes[0, 0].axis("off")
    axes[0, 1].imshow(shuffled, cmap="gray", vmin=0, vmax=1)
    axes[0, 1].set_title("Same pixels, shuffled")
    axes[0, 1].axis("off")
    centers, probability, cumulative = compute_distribution(disk, N_BINS)
    plot_histogram_data(axes[1, 0], centers, probability, label="Original")
    centers, probability, cumulative = compute_distribution(shuffled, N_BINS)
    plot_histogram_data(axes[1, 0], centers, probability, label="Shuffled", color="tab:orange")
    axes[1, 0].set_title("Histograms")
    axes[1, 0].legend()
    centers, probability, cumulative = compute_distribution(disk, N_BINS)
    plot_cumulative_data(axes[1, 1], centers, cumulative, label="Original")
    centers, probability, cumulative = compute_distribution(shuffled, N_BINS)
    plot_cumulative_data(axes[1, 1], centers, cumulative, label="Shuffled", color="tab:orange")
    axes[1, 1].set_title("Cumulative proportion")
    axes[1, 1].legend()
    fig.tight_layout()
    save_figure(fig, "02-meme-histogramme.png")

def exercises():

    _ , _ , house_cumulative = compute_distribution(images[2][1] , bins = 64)
    idx_median = np.where(house_cumulative >= 0.5)[0][0]
    print(idx_median)

    name,mri = images[3]



    mri = np.where(mri < 0.1 ,  0 , 1)
    print(mri)
    centers, probability, cumulative = compute_distribution(mri , 64)


    fig, axes = plt.subplots(2, 3, figsize=(12, 12))
    axes[0, 0].imshow(mri, cmap="gray", vmin=0, vmax=1)
    axes[0, 0].set_title(name)
    axes[0, 0].axis("off")

    centers, probability, cumulative = compute_distribution(mri, N_BINS)
    plot_histogram_data(axes[0, 1], centers, probability)
    axes[0, 1].set_title(f"Histogram - {N_BINS} bins")

    plot_cumulative_data(axes[0, 2], centers, cumulative)
    fig.tight_layout()
    plt.show()

plot_images()