"""Extension: examine sharpening, clipping, and halos."""
import numpy as np
from scipy import ndimage
from tp3_support import load_image, require, compare_images, show_profiles

IMAGE_FILE = '01-mire.png'
# IMAGE_FILE = '03-facade-bruit-additif.png'
# IMAGE_FILE = '01-mire.png'
image = load_image(IMAGE_FILE)
blurred = ndimage.gaussian_filter(image, sigma=2, mode='reflect')
cases = [('Input', image)]
for amount in (0.5, 2):
    # TODO: compute image + amount * (image - blurred), without clipping.
    sharpened = image + amount * (image - blurred)
    require(sharpened)
    print('Amount:', amount, 'Fraction outside [0, 1]:', np.mean((sharpened < 0) | (sharpened > 1)))
    cases.append((f'Sharpening, amount={amount}', sharpened))
compare_images(cases, f'05-{IMAGE_FILE}')
# This profile shows the computed values, including overshoots.
show_profiles(cases, 96, f'05-profil-{IMAGE_FILE}')
