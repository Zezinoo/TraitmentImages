"""Compare filters at fixed settings on two controlled perturbations."""
# MSE: mean squared error, the mean of squared differences from the reference.
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from tp3_support import load_image, require, compare_images, save_figure, RESULTS_DIR


# Use exactly the same window/frame detail for both noise types and all filters.
HOUSE_REGION = (140, 120, 240, 220)


def mean_squared_error(reference, image):
    return np.mean(np.square(reference - image))


def filter_cases(noisy):
    return [
        ('Noisy input', noisy),
        ('Mean 3 x 3', ndimage.uniform_filter(noisy, size=3, mode='reflect')),
        ('Gaussian, sigma=1', ndimage.gaussian_filter(noisy, sigma=1, mode='reflect')),
        ('Median 3 x 3', ndimage.median_filter(noisy, size=3, mode='reflect')),
    ]


def find_isolated_impulse(reference, noisy, radius=4):
    """Find an added black/white pixel with no other changes in its 9 x 9 patch."""
    changed = noisy != reference
    extreme = (noisy == 0) | (noisy == 1)
    size = 2 * radius + 1
    count = ndimage.convolve(changed.astype(int), np.ones((size, size), dtype=int),
                             mode='constant')
    candidates = changed & extreme & (count == 1)
    candidates[:radius, :] = candidates[-radius:, :] = False
    candidates[:, :radius] = candidates[:, -radius:] = False
    if not candidates.any():
        raise ValueError('No isolated impulse found with a complete comparison patch.')
    # Prefer a high-contrast impulse in a smooth patch, away from real edges.
    variation = (ndimage.maximum_filter(reference, size=size)
                 - ndimage.minimum_filter(reference, size=size))
    score = variation / np.maximum(np.abs(noisy - reference), 1 / 255)
    return np.unravel_index(np.argmin(np.where(candidates, score, np.inf)),
                            reference.shape)


def compare_impulse(reference, cases):
    y, x = find_isolated_impulse(reference, cases[0][1])
    radius = 4
    patch = np.s_[y-radius:y+radius+1, x-radius:x+radius+1]
    all_cases = [('Reference', reference)] + cases
    figure, axes = plt.subplots(1, len(all_cases), figsize=(16, 3.5))
    for axis, (title, image) in zip(axes, all_cases):
        axis.imshow(image[patch], cmap='gray', vmin=0, vmax=1,
                    interpolation='nearest')
        axis.add_patch(plt.Rectangle((radius-0.5, radius-0.5), 1, 1,
                                     fill=False, edgecolor='red'))
        axis.set_title(f'{title}\nCenter = {image[y, x]:.4f}')
        axis.axis('off')
    figure.suptitle(f'Isolated impulse at (x={x}, y={y}); same 9 x 9 patch')

    # Remove only this impulse and repeat the filters to measure its influence
    # independently of smoothing of the facade or any other noisy pixels.
    repaired = cases[0][1].copy()
    repaired[y, x] = reference[y, x]
    repaired_cases = filter_cases(repaired)
    lines = [f'Isolated impulse at (x={x}, y={y}), zero-based coordinates.',
             f'Reference intensity: {reference[y, x]:.6f}',
             'Case                 Center error   Max influence on neighbors']
    for (title, image), (_, repaired_image) in zip(cases, repaired_cases):
        influence = np.abs(image[patch] - repaired_image[patch])
        influence[radius, radius] = 0
        lines.append(f'{title:<21} {abs(image[y, x]-reference[y, x]):.6f}'
                     f'       {influence.max():.6f}')
    lines.extend([
        'Neighbor influence compares each result with the same filter applied',
        'after replacing only the selected impulse with its reference value.',
        'The median attenuates the isolated impulse without spreading it like',
        'the mean and Gaussian filters, which distribute its intensity to neighbors.',
    ])
    return figure, lines


def main():
    reference = load_image('02-facade-reference.png')
    experiments = []
    for noise_type, filename in (
        ('Additive', '03-facade-bruit-additif.png'),
        ('Impulse', '04-facade-bruit-impulsionnel.png'),
    ):
        cases = filter_cases(load_image(filename))
        errors = []
        for title, image in cases:
            require(image)
            error = require(mean_squared_error(reference, image))
            errors.append(error)
            print(filename, title, f'MSE={error:.6f}')
        experiments.append((noise_type, filename, cases, errors))

    # Question 3: two result rows and four MSE value columns, in [0, 1] units.
    report = ['MSE relative to reference (intensities normalized to [0, 1])',
              f'{"Noise type":<12} {"Noisy input":>12} {"Mean":>12}'
              f' {"Gaussian":>12} {"Median":>12}']
    for noise_type, _, _, errors in experiments:
        report.append(f'{noise_type:<12}' + ''.join(f' {error:12.6f}' for error in errors))

    # Question 4: locate and compare one actual added impulse at identical coordinates.
    impulse_figure, impulse_report = compare_impulse(reference, experiments[1][2])
    report.extend([''] + impulse_report)

    # Question 5: combine the measured error with the common enlarged house detail.
    report.extend([
        '', f'Common house detail (x0, y0, x1, y1): {HOUSE_REGION}',
        'Additive noise: choose Gaussian (sigma=1). It has the lowest MSE here',
        'and smooths the grain in the window/facade detail. Unwanted effect:',
        'window-frame edges and fine brick texture become blurred despite the lower MSE.',
        'Impulse noise: choose median (3 x 3). It has the lowest MSE here and',
        'removes isolated black/white specks while retaining the main window edges.',
        'Unwanted effect: thin lines and small texture details can disappear, and',
        'corners can become rounded even though the global MSE decreases.',
    ])
    report_text = '\n'.join(report)
    print('\n' + report_text)
    RESULTS_DIR.mkdir(exist_ok=True)
    report_path = RESULTS_DIR / '02-filter-comparison.txt'
    report_path.write_text(report_text + '\n', encoding='utf-8')
    print('Saved report:', report_path)
    save_figure(impulse_figure, '02-isolated-impulse.png')
    for _, filename, cases, _ in experiments:
        compare_images([('Reference', reference)] + cases, f'02-{filename}',
                       region=HOUSE_REGION)


if __name__ == '__main__':
    main()
