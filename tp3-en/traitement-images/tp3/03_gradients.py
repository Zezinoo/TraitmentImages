"""Observe how smoothing changes gradient maps."""
import numpy as np
from scipy import ndimage
from tp3_support import load_image, require, compare_gradients, show_profiles

image = load_image('06-circuit-bruite.png')
cases = [('No smoothing', image)]
for sigma in (1, 3):
    # TODO: apply a Gaussian filter with this sigma and mode='reflect'.
    smoothed = ndimage.gaussian_filter(image, sigma=1, mode='reflect')
    require(smoothed)
    cases.append((f'Gaussian, sigma={sigma}', smoothed))

magnitudes = []
for title, image in cases:
    # The factor 1/8 normalizes these Sobel kernels for a unit pixel step.
    gx = ndimage.sobel(image, axis=1, mode='reflect') / 8
    gy = ndimage.sobel(image, axis=0, mode='reflect') / 8
    # TODO: compute sqrt(gx**2 + gy**2), without clipping gx or gy.
    magnitude = np.sqrt(gx**2 + gy**2)
    magnitudes.append(require(magnitude))
    print(title, 'Gx range:', gx.min(), gx.max())
compare_gradients(cases, magnitudes, '03-gradients.png')
show_profiles(cases, 250, '03-profils.png')
