"""Connect a local average to smoothing and loss of fine details."""
import numpy as np
from scipy import ndimage
from tp3_support import load_image, require, compare_images, show_profiles

window = np.array([[0.2, 0.2, 0.8], [0.2, 0.2, 0.8], [0.2, 0.2, 0.8]])
print('Central pixel before filtering:', window[1, 1])
print('Local mean:', window.mean())

image = load_image('01-mire.png')
cases = [('Reference', image)]
for size in (3, 15):
    # TODO: create a size by size array of ones, then divide by size squared.
    kernel = np.ones(shape=((size,size)))/(size**2)
    require(kernel)
    print('Kernel sum:', kernel.sum())
    # TODO: convolve image with kernel, using mode='reflect'.
    
    filtered = ndimage.convolve(image , kernel , mode='reflect')
    require(filtered)
    cases.append((f'Mean filter {size} x {size}', filtered))
compare_images(cases, '01-mire.png')
show_profiles(cases, 96, '01-profils.png')
