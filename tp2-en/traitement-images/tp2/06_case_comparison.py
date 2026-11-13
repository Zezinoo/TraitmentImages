"""Choose and compare two transforms for a given case."""
import numpy as np
from skimage import exposure
from tp2_support import load_gray, compare_images_and_histograms, print_stats
from points_transforms import gamma_transform , affine_transform , logarithmic_transform   , percentile_stretch

# Choose one file, then study the other if time allows.
IMAGE_FILE = "06-coupe-irm-affichage.png"
# IMAGE_FILE = "04-maison-ecretee.png"
LABEL_A = "A: gain = 1.2 , offset = 0.3"
LABEL_B = "B: stretch 10,90 percentiles"


def transform_a(image):
    # TODO : reuse a studied transform and choose its parameters
    return affine_transform(image , 1.2 , 0.3)


def transform_b(image):
    # TODO : apply another transform for a meaningful comparison
    return percentile_stretch(image , [10,90])


original = load_gray(IMAGE_FILE)
result_a = transform_a(original)
result_b = transform_b(original)
for result in (result_a, result_b):
    assert result.shape == original.shape, "Keep the original image shape"
    assert np.isfinite(result).all(), "The result contains a nonfinite value"
    assert result.min() >= 0 and result.max() <= 1, "Keep values within [0, 1]"
cases = [("Input", original), (LABEL_A, result_a), (LABEL_B, result_b)]
if IMAGE_FILE == "04-maison-ecretee.png":
    cases.append(("Reference before clipping", load_gray("03-maison-reference.png")))
compare_images_and_histograms(cases, "Compare methods for a stated observation goal", f"06-{IMAGE_FILE}")
for label, result in cases:
    print_stats(label, result)
