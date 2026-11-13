"""Extension: compare spatial and intensity-dependent averaging."""
from scipy import ndimage
from skimage.restoration import denoise_bilateral
from tp3_support import load_image, require, compare_images

image = load_image('03-facade-bruit-additif.png')
cases = [('Input', image), ('Gaussian, sigma=2', ndimage.gaussian_filter(image, 2, mode='reflect'))]
for sigma_color in (0.05, 0.20):
    # TODO: call denoise_bilateral with sigma_color, sigma_spatial=2,
    # mode='reflect' and channel_axis=None.
    filtered = denoise_bilateral(image , sigma_spatial = 2 , sigma_color = sigma_color , mode = "reflect" , channel_axis = None)
    cases.append((f'Bilateral, sigma_color={sigma_color}', require(filtered)))
compare_images(cases, '06-bilateral.png', region=(140, 120, 240, 220))
