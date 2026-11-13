# Lab 2 resources: histograms and contrast

This folder contains eight images with a distinct role. The scripts use values normalized to [0, 1]. Displayed images are not calibrated physical measurements. Keep these filenames unchanged in both language versions.

| File | Role in the lab | Source and preparation |
|---|---|---|
| `01-disque.png` | Counts, areas, loss of spatial information | Copy of `resources/256x256/disque.png`, existing course collection |
| `02-circuit.jpg` | Fine structures, global contrast | Copy of `resources/512x512/circuit_512x512.jpg`, existing course collection |
| `03-maison-reference.png` | Shadows and high intensities in one scene | Copy of `resources/512x512/maisons_512x512_normal.png`, existing course collection |
| `04-maison-ecretee.png` | Loss of intensity differences | Derived from 03: `round(255 * clip(1.8 * I, 0, 1))`, with normalized I |
| `05-image-bruitee.jpg` | Local contrast and fluctuations | Copy of `resources/various/highnoise.jpg`, existing course collection |
| `06-coupe-irm-affichage.png` | Large dark background and display values | Slice 64 (zero-based indexing) of `resources/512x512/t1-head.tif`; source values 0 to 711, divided by 711 and quantized to 8 bits |
| `07-fruits-rgb.jpg` | Color channels, light background, color shifts | `resources/various/fruits.jpg`, resized to 960 pixels wide, JPEG quality 95 |
| `08-balles-rgb.jpg` | Objects of distinct colors and R, G, B histograms | `resources/various/play-balls.jpg`, resized to 960 pixels wide, JPEG quality 95 |

The `resources/` paths are relative to the instructor's `practical-work/` folder.

## Credits

- Medical slice: Jeff Orchard, ImageJ "T1 Head" sample, attribution already recorded in the course credits: https://imagej.net/images/t1-head.txt. This is a display version with no physical units; it does not replace the original 16-bit data.
- Fruit: Bhaskar Peddhapati, "Fruits!", CC BY 2.0. Source established in Lab 1: https://www.flickr.com/photos/peddhapati/9729907217/ ; Commons copy: https://commons.wikimedia.org/wiki/File:Fruits!.jpg. Resized and re-encoded for this lab.
- Balls: Petr Kratochvil, "Play balls", CC0 / public domain, attribution established in Lab 1: https://www.publicdomainpictures.net/en/view-image.php?image=24696&picture=play-balls. Resized and re-encoded for this lab.
- Disk, circuit, house, and noisy image: existing course resources. Their local paths are identified above; no additional author or license is assumed here.

Preparation can be reproduced using `practical-work/scripts/prepare_tp2_resources.py`. The subject and captions distinguish source photographs from controlled digital transforms.
