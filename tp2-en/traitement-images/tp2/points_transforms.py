"""Compare point intensity transforms."""

import matplotlib.pyplot as plt
import numpy as np

from tp2_support import compare_images_and_histograms, load_gray, print_stats


# Change only these settings for the first comparison.
GAMMAS = (0.55, 1.7)
AFFINE_SETTINGS = ((1.4, 0.0), (1.0, 0.08))
LOG_PARAMETERS = (3.0, 12.0)
PERCENTILES = (1, 99)


def gamma_transform(image, gamma):
    # TODO: apply gamma to each image intensity
    return image**gamma


def affine_transform(image, gain, offset):
    # TODO: apply gain and offset, then clip to [0, 1]
    return np.clip(gain * image + offset , 0 , 1)


def logarithmic_transform(image, parameter):
    # TODO: apply log(1 + k I) / log(1 + k)
    if parameter<0:
        raise(ValueError('parameter must be greater than 0'))
    else : 
        return np.log(1 + parameter*image)/(np.log(1 + parameter))

    return 


def percentile_stretch(image, percentiles): #Like the autostretch in image J
    low, high = np.percentile(image, percentiles)
    if high <= low:
        return image.copy()
    # TODO: normalize between low and high, then clip to [0, 1]
    else :

        return np.clip((image - low)/(high - low),
                       0 , 
                       1)

if __name__ == "__main__":
    reference = load_gray("03-maison-reference.png")
    # Controlled digital darkening to isolate the effect of the transforms.
    image = 0.55 * reference + 0.02

    gamma_images = [gamma_transform(image, gamma) for gamma in GAMMAS]
    stretched = percentile_stretch(image, PERCENTILES)
    gamma_cases = [("Darkened", image)]
    gamma_cases.extend((f"Gamma {gamma:g}", result) for gamma, result in zip(GAMMAS, gamma_images))
    gamma_cases.append((f"Stretch q{PERCENTILES[0]}-q{PERCENTILES[1]}", stretched))

    affine_images = [affine_transform(image, gain, offset) for gain, offset in AFFINE_SETTINGS]
    logarithmic_images = [logarithmic_transform(image, parameter) for parameter in LOG_PARAMETERS]
    pointwise_cases = [("Darkened", image)]
    pointwise_cases.extend(
        (f"Gain {gain:g}, offset {offset:g}", result)
        for (gain, offset), result in zip(AFFINE_SETTINGS, affine_images)
    )
    pointwise_cases.extend(
        (f"Logarithm k={parameter:g}", result)
        for parameter, result in zip(LOG_PARAMETERS, logarithmic_images)
    )

    compare_images_and_histograms(
        gamma_cases,
        "Power transform and percentile stretch",
        "03-puissance-et-etirement.png",
    )
    compare_images_and_histograms(
        pointwise_cases,
        "Affine and logarithmic transforms",
        "04-affine-et-logarithme.png",
    )

    all_cases = gamma_cases + pointwise_cases[1:]
    for label, result in all_cases:
        print_stats(label, result)

    # Separate case: clipping has removed intensity differences.
    clipped = load_gray("04-maison-ecretee.png")
    clipping_cases = [("Reference", reference), ("Clipped", clipped),
                    ("Gamma after clipping", gamma_transform(clipped, 0.55))]
    compare_images_and_histograms(clipping_cases, "Limits of correction after clipping",
                                "02-limites-ecretage.png")
    print("Fraction of pixels equal to 1 in the clipped image:", np.mean(clipped == 1))
