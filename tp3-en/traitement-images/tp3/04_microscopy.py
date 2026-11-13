"""Choose a filtering compromise without a clean reference image."""
from scipy import ndimage
from tp3_support import load_image, require, compare_images, show_profiles

image = load_image('07-cellule.png')
# TODO: apply a Gaussian filter with sigma=1 and mode='reflect'.
result_a = ndimage.gaussian_filter(image , sigma=1 , mode = "reflect")
# TODO: apply a Gaussian filter with sigma=3 and mode='reflect'.
result_b = ndimage.gaussian_filter(image , sigma = 3 , mode = "reflect")
cases = [('Input', image), ('Gaussian, sigma=1', require(result_a)),
         ('Gaussian, sigma=3', require(result_b))]
compare_images(cases, '04-cellule.png', region=(300, 210, 550, 480))
show_profiles(cases, 350, '04-profil-cellule.png')
