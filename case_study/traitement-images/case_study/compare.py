"""Compare several saved runs quantitatively."""

import argparse
import csv

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tools import RESULTS, labels, metrics
from parking_report import validate_trial_name


def main(names):
    ground_truth = labels("calibration") | labels("validation")
    measurements = []
    for name in names:
        validate_trial_name(name)
        filename = RESULTS / f"predictions-{name}.csv"
        with filename.open(newline="", encoding="utf-8") as stream:
            predictions = list(csv.DictReader(stream))
        for split in ("calibration", "validation"):
            subset = [row for row in predictions if row["split"] == split]
            truth = [ground_truth[(row["image_id"], int(row["slot_id"]))]
                     for row in subset]
            predicted = [int(row["predicted_occupancy"]) for row in subset]
            values = metrics(truth, predicted)
            measurements.append({"method": name, "split": split, **values})
            print(name, split, values)

    fig, ax = plt.subplots(figsize=(max(7, len(names) * 2.2), 4))
    x = np.arange(len(names))
    for offset, split, title, color, hatch in (
        (-0.18, "calibration", "Tuning", "0.85", "///"),
        (0.18, "validation", "Validation", "0.50", "..."),
    ):
        values = [next(row["F1"] for row in measurements
                       if row["method"] == name and row["split"] == split)
                  for name in names]
        ax.bar(x + offset, values, width=0.36, label=title, color=color,
               edgecolor="black", linewidth=0.7, hatch=hatch)
    ax.set(xticks=x, xticklabels=names, ylim=(0, 1.05), ylabel="F1 score")
    ax.legend()
    fig.tight_layout()
    output = RESULTS / "method-comparison.png"
    fig.savefig(output, dpi=160)
    plt.close(fig)
    print("Figure:", output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("names", nargs="+", help="Names of runs already completed")
    main(parser.parse_args().names)
