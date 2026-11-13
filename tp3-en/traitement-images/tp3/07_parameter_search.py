"""Extension: minimize a numerical error, then inspect the selected result."""
# This would be useful to know during LP2N days
# MSE: mean squared error, the mean of squared differences from the reference.
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
from tp3_support import load_image, require, compare_images, save_figure

reference = load_image('02-facade-reference.png')
noisy = load_image('03-facade-bruit-additif.png')
sigmas = np.array([0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0])
errors = []
results = []
for sigma in sigmas:
    filtered = ndimage.gaussian_filter(noisy, sigma=sigma, mode='reflect')
    # TODO: compute the mean squared error against reference.
    error = np.mean((filtered - reference)**2)
    errors.append(require(error))
    results.append(filtered)
# TODO: obtain the index of the smallest error with np.argmin.
best_index = np.argmin(errors)
require(best_index)
print('Selected sigma:', sigmas[best_index], 'MSE:', errors[best_index])
figure, axis = plt.subplots(figsize=(7, 4))
axis.plot(sigmas, errors, 'o-')
axis.set(xlabel='Sigma (pixels)', ylabel='Mean squared error')
axis.grid(alpha=0.25)
save_figure(figure, '07-erreurs.png')
compare_images([('Reference', reference), ('Noisy input', noisy),
                (f'Selected sigma={sigmas[best_index]}', results[best_index])],
               '07-selection.png', region=(140, 120, 240, 220))
