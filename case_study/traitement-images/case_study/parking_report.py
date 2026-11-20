"""Export an offline report from student predictions; never run an occupancy method.

The same helper is supplied in both language editions. Only Python's standard
library is needed here; image processing remains in pipeline.py.
"""

import csv
import json
import math
from pathlib import Path
import re
import shutil


def validate_trial_name(name):
    """Keep each trial inside its own results directory."""
    if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
        raise ValueError("Nom d'essai / Trial name: letters, digits, _ or - only")


def _field(row, french, english):
    return row[french] if french in row else row[english]


def create_report(results, frames, boxes, resources, output, lang="fr"):
    """Display the supplied decisions, without reading any ground-truth labels.

    Accept French or English result/manifest columns. Require exactly one
    prediction per monitored space for every observation in the result CSV.
    Reusing an output directory refreshes this trial's report. Other trials
    remain independent. Return the path to the generated HTML file.
    """
    if lang not in ("fr", "en"):
        raise ValueError("Language must be fr or en")
    if not boxes:
        raise ValueError("Aucune place / No monitored spaces")
    for box in boxes.values():
        x0, y0, x1, y1 = box
        if not (0 <= x0 < x1 and 0 <= y0 < y1):
            raise ValueError(f"Rectangle invalide / Invalid rectangle: {box}")
    indexed = {}
    for frame in frames:
        key = frame["image_id"]
        if key in indexed:
            raise ValueError(f"Image dupliquée / Duplicate image: {key}")
        indexed[key] = frame
    grouped = {}
    for row in results:
        key = row["image_id"]
        if not re.fullmatch(r"[A-Za-z0-9_-]+", key) or key not in indexed:
            raise ValueError(f"Image inconnue ou invalide / Unknown or invalid image: {key}")
        frame = indexed[key]
        if _field(frame, "partition", "split") == "reference":
            raise ValueError("La référence n'est pas une observation / Reference is not an observation")
        slot = int(_field(row, "place_id", "slot_id"))
        score = float(row["score"])
        raw_decision = _field(row, "occupation_predite", "predicted_occupancy")
        if str(raw_decision) not in ("0", "1") or not math.isfinite(score):
            raise ValueError(f"Prédiction invalide / Invalid prediction: {key}, {slot}")
        decisions = grouped.setdefault(key, {})
        if slot not in boxes or slot in decisions:
            raise ValueError(f"Place inconnue ou dupliquée / Unknown or duplicate space: {key}, {slot}")
        decisions[slot] = {"place_id": slot, "score": score,
                           "occupation_predite": int(raw_decision)}
    if not grouped:
        raise ValueError("Aucune prédiction / No predictions")

    image_directory = (Path(resources) / "images").resolve()
    output = Path(output)
    summaries, sources = [], []
    for key, frame in indexed.items():
        if key not in grouped:
            continue
        if set(grouped[key]) != set(boxes):
            raise ValueError(f"Prédictions incomplètes / Missing space predictions: {key}")
        filename = Path(_field(frame, "fichier", "filename"))
        source = (image_directory / filename).resolve()
        if filename.is_absolute() or ".." in filename.parts or not source.is_relative_to(image_directory):
            raise ValueError(f"Chemin d'image invalide / Invalid image path: {filename}")
        if not source.is_file() or source.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            raise ValueError(f"Image absente ou non prise en charge / Missing or unsupported image: {filename}")
        preview = f"images/{key}{source.suffix.lower()}"
        destination = (output / preview).resolve()
        if destination == source:
            raise ValueError("Le rapport doit être séparé des images sources / Report must be separate from source images")
        ordered = [grouped[key][slot] for slot in sorted(boxes)]
        occupied = sum(d["occupation_predite"] for d in ordered)
        summaries.append({
            "image_id": key, "jour": _field(frame, "jour", "day"),
            "heure": _field(frame, "heure", "time"),
            "meteo": _field(frame, "meteo", "weather"),
            "partition": _field(frame, "partition", "split"),
            "occupees": occupied, "libres": len(boxes) - occupied,
            "taux_occupation_percent": 100 * occupied / len(boxes),
            "preview_file": preview, "decisions": ordered,
        })
        sources.append((source, output / preview))
    regions = [dict(zip(("place_id", "x0", "y0", "x1", "y1"), (slot, *boxes[slot])))
               for slot in sorted(boxes)]
    data = json.dumps({"frames": summaries, "regions": regions, "trial": output.parent.name,
                       "version": "student-python"},
                      ensure_ascii=False, allow_nan=False)
    data = data.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    template = Path(__file__).with_name("parking_report.html").read_text(encoding="utf-8")
    counts_name = "occupation.csv" if lang == "fr" else "occupancy.csv"
    html = template.replace("__LANG__", lang).replace("__DATA__", data)
    html = html.replace('href="occupation.csv"', f'href="{counts_name}"')
    capacity = len(boxes)
    count_columns = (["image_id", "jour", "heure", "meteo", "partition", "capacite", "occupees", "libres", "taux_occupation_percent"]
                     if lang == "fr" else ["image_id", "day", "time", "weather", "split", "capacity", "occupied", "free", "occupancy_percent"])
    prediction_columns = (["image_id", "place_id", "score", "occupation_predite"]
                          if lang == "fr" else ["image_id", "slot_id", "score", "predicted_occupancy"])

    # All predictions and paths are checked before changing the report.
    output.mkdir(parents=True, exist_ok=True)
    (output / "images").mkdir(exist_ok=True)
    for source, destination in sources:
        shutil.copyfile(source, destination)
    with (output / counts_name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(count_columns)
        writer.writerows([r["image_id"], r["jour"], r["heure"], r["meteo"], r["partition"],
                          capacity, r["occupees"], r["libres"], r["taux_occupation_percent"]]
                         for r in summaries)
    with (output / "predictions.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(prediction_columns)
        writer.writerows([r["image_id"], d["place_id"], d["score"], d["occupation_predite"]]
                         for r in summaries for d in r["decisions"])
    page = output / "index.html"
    page.write_text(html, encoding="utf-8")
    return page
