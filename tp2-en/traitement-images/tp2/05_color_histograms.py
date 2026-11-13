"""Compare channel histograms and RGB processing results."""
import numpy as np
from skimage import exposure
from tp2_support import load_rgb, compare_rgb_cases

FILES = ("08-balles-rgb.jpg", "07-fruits-rgb.jpg")
N_BINS = 64
GAMMA = 0.6


def channel_histograms(rgb):
    frequencies = []
    for k in range(3):
        # TODO : extract channel k from the (height, width, 3) array
        channel = rgb[:,:,k]
        if channel is None:
            raise NotImplementedError("Complete channel extraction in channel_histograms")
        counts, edges = np.histogram(channel, bins=N_BINS, range=(0, 1))
        frequencies.append(counts / counts.sum())
    centers = (edges[:-1] + edges[1:]) / 2
    return centers, frequencies


def equalize_channels(rgb):
    result = np.empty_like(rgb)
    for k in range(3):
        # TODO : equalize channel k; the result is then assigned to result[..., k]
        equalized_channel = exposure.equalize_hist(rgb[... , k])
        if equalized_channel is None:
            raise NotImplementedError("Complete channel equalization in equalize_channels")
        result[..., k] = equalized_channel
    return result


for filename in FILES:
    rgb = load_rgb(filename)
    common_gamma = np.power(rgb, GAMMA)
    independent_equalization = equalize_channels(rgb)
    cases = [("Original", rgb), (f"Same gamma {GAMMA:g} on R, G, B", common_gamma),
             ("Independent R, G, B equalization", independent_equalization)]
    distributions = [channel_histograms(image) for _, image in cases]
    compare_rgb_cases(cases, distributions, f"05-couleur-{filename[:-4]}.png")

# Check the ratios between the components of one pixel.
pixel = np.array([0.2, 0.4, 0.8])
transformed = pixel ** GAMMA
print("Pixel before / after:", pixel, transformed)
print("R/G before / after:", pixel[0] / pixel[1], transformed[0] / transformed[1])
