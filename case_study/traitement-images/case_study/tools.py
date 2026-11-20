"""Shared data loading, visualization, and evaluation for the case study."""

import csv
from pathlib import Path

import numpy as np
import matplotlib
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
RESOURCES = ROOT.parent / "ressources-case_study"
if not RESOURCES.is_dir():
    RESOURCES = ROOT.parent / "ressources"
RESULTS = ROOT / "results"
PREVIEW_FONT = ImageFont.truetype(
    str(Path(matplotlib.get_data_path()) / "fonts/ttf/DejaVuSans.ttf"), 16
)


def read_csv(filename):
    with (RESOURCES / filename).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def available_images():
    """Give English field names to the shared image manifest."""
    splits = {"reference": "reference", "calibrage": "calibration",
              "validation": "validation", "evaluation": "evaluation"}
    return [{
        "image_id": row["image_id"], "filename": row["fichier"],
        "day": row["jour"], "time": row["heure"],
        "weather": row["meteo"], "split": splits[row["partition"]],
    } for row in read_csv("images.csv")]


def slots():
    return {
        int(row["place_id"]): tuple(
            int(row[column]) for column in ("x0", "y0", "x1", "y1")
        ) for row in read_csv("parking_spaces.csv")
    }


def load_image(filename):
    """Return a floating-point RGB image in [0, 1], shape (750, 1000, 3)."""
    image = np.asarray(Image.open(RESOURCES / "images" / filename).convert("RGB"))
    assert image.shape == (750, 1000, 3), (filename, image.shape)
    return image.astype(np.float32) / 255.0


def labels(split):
    if split not in ("calibration", "validation"):
        raise ValueError("Labels are unavailable for this split")
    filename = ("labels_tuning.csv" if split == "calibration"
                else "labels_validation.csv")
    return {
        (row["image_id"], int(row["place_id"])): int(row["occupation"])
        for row in read_csv(filename)
    }


def crop(image, box):
    """Extract a space with exclusive upper bounds x1 and y1."""
    x0, y0, x1, y1 = box
    return image[y0:y1, x0:x1]


def metrics(truth, prediction):
    """Binary classification metrics with occupied as the positive class."""
    truth = np.asarray(truth, dtype=bool)
    prediction = np.asarray(prediction, dtype=bool)
    if truth.shape != prediction.shape or truth.size == 0:
        raise ValueError("Labels and predictions are incompatible")
    tp = int(np.count_nonzero(truth & prediction))
    tn = int(np.count_nonzero(~truth & ~prediction))
    fp = int(np.count_nonzero(~truth & prediction))
    fn = int(np.count_nonzero(truth & ~prediction))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "TP": tp, "TN": tn, "FP": fp, "FN": fn,
        "accuracy": (tp + tn) / truth.size,
        "precision": precision, "recall": recall, "F1": f1,
    }


def save_preview(image, boxes, filename, decisions=None):
    """Grayscale preview: dashed=predicted free, solid=predicted occupied.

    Each identifier is followed by 0, 1, or ? when no decision is supplied.
    Grayscale conversion affects the displayed file only.
    """
    output = Image.fromarray(np.uint8(np.clip(image * 255, 0, 255))).convert("L")
    draw = ImageDraw.Draw(output)
    for slot, (x0, y0, x1, y1) in boxes.items():
        value = None if decisions is None else decisions.get(slot)
        rectangle = (x0, y0, x1 - 1, y1 - 1)
        draw.rectangle(rectangle, outline="white", width=7)
        if value == 0:
            for x in range(x0, x1, 15):
                end = min(x + 8, x1 - 1)
                for y in (y0, y1 - 1):
                    draw.line((x, y, end, y), fill="black", width=3)
            for y in range(y0, y1, 15):
                end = min(y + 8, y1 - 1)
                for x in (x0, x1 - 1):
                    draw.line((x, y, x, end), fill="black", width=3)
        else:
            draw.rectangle(rectangle, outline="black", width=1 if value is None else 3)
        state = "?" if value is None else str(int(value))
        draw.text((x0 + 5, y0 + 5), f"{slot} : {state}", fill="black",
                  font=PREVIEW_FONT, stroke_width=2, stroke_fill="white")
    filename = Path(filename)
    filename.parent.mkdir(parents=True, exist_ok=True)
    output.save(filename)
