"""Run a pipeline on every slot and evaluate the labeled data."""

import argparse
import csv
import math

from tools import (
    RESULTS, RESOURCES, available_images, labels, load_image, metrics, save_preview, slots,
)
from baseline import predict as baseline
from visualizations import create_figures
from parking_report import create_report, validate_trial_name


def run(predict=None, name="trial1"):
    validate_trial_name(name)
    if predict is None:
        # The baseline remains runnable even if the personal pipeline is unfinished.
        from pipeline import predict
    if name == "baseline" and predict is not baseline:
        raise ValueError("The name baseline is reserved for the supplied method; choose another trial name")
    images = available_images()
    filenames = {row["image_id"]: row["filename"] for row in images}
    boxes = slots()
    reference = load_image(next(row["filename"] for row in images
                                if row["image_id"] == "R00"))
    results = []
    RESULTS.mkdir(parents=True, exist_ok=True)

    for row in images:
        if row["split"] == "reference":
            continue
        image = load_image(row["filename"])
        decisions = {}
        for slot, box in boxes.items():
            score, decision = predict(image, reference, box)
            score = float(score)
            if not math.isfinite(score):
                raise ValueError("A score must be a finite number")
            if decision not in (0, 1):
                raise ValueError("A decision must be 0 or 1")
            decision = int(decision)
            decisions[slot] = decision
            results.append({
                "image_id": row["image_id"], "slot_id": slot,
                "day": row["day"], "time": row["time"],
                "weather": row["weather"], "split": row["split"],
                "score": f"{score:.6f}", "predicted_occupancy": decision,
            })
        save_preview(image, boxes,
                     RESULTS / name / f"{row['image_id']}-decisions.png", decisions)

    output = RESULTS / f"predictions-{name}.csv"
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    print("Predictions saved to:", output)
    page = create_report(results, images, boxes, RESOURCES,
                         RESULTS / name / "report", lang="en")
    print("Interactive report to open in your browser:", page.resolve().as_uri())

    for split in ("calibration", "validation"):
        ground_truth = labels(split)
        subset = [row for row in results if row["split"] == split]
        truth = [ground_truth[(row["image_id"], row["slot_id"])] for row in subset]
        predictions = [row["predicted_occupancy"] for row in subset]
        print(split, metrics(truth, predictions))
        for weather in ("sunny", "overcast", "rainy"):
            indices = [i for i, row in enumerate(subset) if row["weather"] == weather]
            if indices:
                print(" ", weather, metrics(
                    [truth[i] for i in indices], [predictions[i] for i in indices]
                ))
    ground_truth = labels("calibration") | labels("validation")
    create_figures(results, ground_truth, filenames, RESULTS / name)
    print("Diagnostic figures:", RESULTS / name)
    print("Evaluation labels are reserved for the instructor.")
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--method", choices=("personal", "baseline"), default="personal",
                        help="Team pipeline (default) or supplied baseline")
    parser.add_argument("--name",
                        help="Short trial name used to preserve its results")
    options = parser.parse_args()
    name = options.name or ("baseline" if options.method == "baseline" else "trial1")
    method = baseline if options.method == "baseline" else None
    try:
        run(predict=method, name=name)
    except NotImplementedError as error:
        parser.exit(1, f"{error}\n")
