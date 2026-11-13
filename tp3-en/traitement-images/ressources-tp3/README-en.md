# Lab 3 resources: spatial filtering

Scripts load these grayscale PNG files and divide their codes by 255. No per-image min-max stretching is applied when loading. Every student receives the same perturbed images.

| File | Source and preparation |
|---|---|
| `01-mire.png` | Synthetic test pattern created for this lab: 192 rows, 256 columns, levels 0.2 and 0.8. Boundary at x=128; lines 1, 3, and 7 pixels wide at columns 45, 58, and 75, spanning rows 40 through 151. |
| `02-facade-reference.png` | Derived from `practical-work/tp2/ressources/03-maison-reference.png`, a historical course resource. Transform `0.1 + 0.8 * image`, then round to 8-bit codes. This is the reference for the digital experiment, not a certified noise-free acquisition. |
| `03-facade-bruit-additif.png` | Zero-mean Gaussian noise with standard deviation 0.10 added to 02, then clipping to [0, 1] and 8-bit rounding. About 2.87% of values are clipped, so the stored noise is no longer exactly Gaussian. |
| `04-facade-bruit-impulsionnel.png` | From 02: probability 0.025 of replacing a pixel with 0, probability 0.025 of replacing it with 1. Other pixels remain unchanged. |
| `05-circuit-reference.png` | Grayscale decoding of `practical-work/tp2/ressources/02-circuit.jpg`, a historical course resource, saved as PNG. |
| `06-circuit-bruite.png` | Zero-mean Gaussian noise with standard deviation 0.04 added to 05, then clipping and 8-bit rounding. |
| `07-cellule.png` | Pixel copy of `skimage.data.cell()`, without added noise or resampling. Phase image of a cell in saline, represented with 8-bit codes. The background patterns are part of the supplied data. |

## Credits

- Test pattern and digital perturbations: teaching material created for this lab.
- House and circuit: historical course resources reused from Lab 2. The original author and license are not documented in the available files; no additional reuse license is assigned here.
- Cell: CC0 data (public domain) distributed by *scikit-image*. Reference: Paul Müller, Mirjam Schürmann, Salvatore Girardo, Gheorghe Cojoc, and Jochen Guck, "Accurate evaluation of size and refractive index for spherical objects in quantitative phase imaging", *Optics Express* 26(8), 10729-10743, 2018, https://doi.org/10.1364/OE.26.010729. Description and license: https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.cell.

No conversion from cell image codes to a physical quantity is provided here. This lab has no perfect reference image of the same cell.

## Reproducibility

The instructor preparation script is `practical-work/scripts/prepare_tp3_resources.py`. It uses `numpy.random.default_rng(2027)` in this order: additive house noise, impulse locations, additive circuit noise. All outputs are rounded to the nearest integer after multiplication by 255. Prepared files are distributed; no random generation or Internet connection is required during the lab.
