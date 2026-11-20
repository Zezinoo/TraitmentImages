"""Diagnostic figures; students remain responsible for interpreting them."""

from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tools import crop, load_image, metrics, slots


def create_figures(results, ground_truth, filenames, directory):
    """Save comparable views for every evaluated method."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    known = {
        (row["image_id"], row["slot_id"]): ground_truth[(row["image_id"], row["slot_id"])]
        for row in results if (row["image_id"], row["slot_id"]) in ground_truth
    }

    # 1. Class score distributions do not impose a decision threshold.
    score_values = [float(row["score"]) for row in results
                    if (row["image_id"], row["slot_id"]) in known]
    bins = np.histogram_bin_edges(score_values, bins=12)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, split in zip(axes, ("calibration", "validation")):
        subset = [row for row in results if row["split"] == split]
        for label, title, color, hatch in ((0, "free", "0.85", "///"),
                                           (1, "occupied", "0.50", "...")):
            values = [float(row["score"]) for row in subset
                      if known[(row["image_id"], row["slot_id"])] == label]
            ax.hist(values, bins=bins, alpha=0.7, label=title, color=color,
                    edgecolor="black", linewidth=0.7, hatch=hatch)
        ax.set(title="Tuning" if split == "calibration" else "Validation",
               xlabel="Method score", ylabel="Number of slots")
        ax.legend()
    fig.tight_layout()
    fig.savefig(directory / "score-distributions.png", dpi=160)
    plt.close(fig)

    # 2. The same scores can produce different decisions at another threshold.
    fig, ax = plt.subplots(figsize=(8, 4.5))
    scores = [float(row["score"]) for row in results if row["split"] != "evaluation"]
    thresholds = np.linspace(min(scores), max(scores), 100)
    for split, title, color, style in (
        ("calibration", "Tuning", "black", "-"),
        ("validation", "Validation", "0.45", "--"),
    ):
        subset = [row for row in results if row["split"] == split]
        truth = [known[(row["image_id"], row["slot_id"])] for row in subset]
        values = [float(row["score"]) for row in subset]
        f1 = [metrics(truth, [int(score > threshold) for score in values])["F1"]
              for threshold in thresholds]
        ax.plot(thresholds, f1, label=title, color=color, linestyle=style, linewidth=2)
    ax.set(xlabel="Decision threshold", ylabel="F1", ylim=(0, 1.04),
           title="Threshold sensitivity with unchanged scores")
    ax.legend()
    fig.tight_layout()
    fig.savefig(directory / "threshold-sensitivity.png", dpi=160)
    plt.close(fig)

    # 3. Use the same TP, TN, FP, FN conventions for both splits.
    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    for ax, split in zip(axes, ("calibration", "validation")):
        subset = [row for row in results if row["split"] == split]
        truth = [known[(row["image_id"], row["slot_id"])] for row in subset]
        predictions = [row["predicted_occupancy"] for row in subset]
        values = metrics(truth, predictions)
        matrix = np.array([[values["TN"], values["FP"]],
                           [values["FN"], values["TP"]]])
        maximum = max(1, matrix.max())
        ax.imshow(matrix, cmap="Greys", vmin=0, vmax=maximum)
        for (i, j), value in np.ndenumerate(matrix):
            color = "white" if value >= 0.65 * maximum else "black"
            ax.text(j, i, str(value), ha="center", va="center",
                    color=color, fontsize=14)
        ax.set(xticks=[0, 1], yticks=[0, 1],
               xticklabels=["free", "occupied"],
               yticklabels=["free", "occupied"],
               xlabel="Predicted", ylabel="Ground truth",
               title="Tuning" if split == "calibration" else "Validation")
    fig.tight_layout()
    fig.savefig(directory / "confusion-matrices.png", dpi=160)
    plt.close(fig)

    # 4. Overall performance can hide a weather-specific failure.
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for ax, split in zip(axes, ("calibration", "validation")):
        by_weather = defaultdict(list)
        for row in results:
            if row["split"] == split:
                by_weather[row["weather"]].append(row)
        for i, weather in enumerate(("sunny", "overcast", "rainy")):
            subset = by_weather[weather]
            truth = [known[(row["image_id"], row["slot_id"])] for row in subset]
            predictions = [row["predicted_occupancy"] for row in subset]
            values = metrics(truth, predictions)
            ax.bar(i - 0.19, values["accuracy"], width=0.36, color="0.85",
                   edgecolor="black", linewidth=0.7, hatch="///",
                   label="Accuracy" if i == 0 else None)
            ax.bar(i + 0.19, values["F1"], width=0.36, color="0.50",
                   edgecolor="black", linewidth=0.7, hatch="...",
                   label="F1" if i == 0 else None)
        ax.set(xticks=range(3), xticklabels=["sunny", "overcast", "rainy"],
               ylim=(0, 1.08), title="Tuning" if split == "calibration" else "Validation")
        ax.legend()
    fig.tight_layout()
    fig.savefig(directory / "metrics-by-weather.png", dpi=160)
    plt.close(fig)

    # 5. More images make day-by-day analysis meaningful.
    fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharey=True)
    for ax, split in zip(axes, ("calibration", "validation")):
        days = sorted({row["day"] for row in results if row["split"] == split})
        accuracies, f1, weathers = [], [], []
        for day in days:
            subset = [row for row in results if row["day"] == day]
            truth = [known[(row["image_id"], row["slot_id"])] for row in subset]
            predictions = [row["predicted_occupancy"] for row in subset]
            values = metrics(truth, predictions)
            accuracies.append(values["accuracy"])
            f1.append(values["F1"] if any(truth) else np.nan)
            weathers.append(subset[0]["weather"])
        x = np.arange(len(days))
        ax.bar(x - 0.18, accuracies, width=0.36, label="Accuracy", color="0.85",
               edgecolor="black", linewidth=0.7, hatch="///")
        ax.bar(x + 0.18, f1, width=0.36, label="F1", color="0.50",
               edgecolor="black", linewidth=0.7, hatch="...")
        ax.set(xticks=x,
               xticklabels=[f"{day}\n{weather}" for day, weather in zip(days, weathers)],
               title="Tuning" if split == "calibration" else "Validation",
               ylabel="Score", ylim=(0, 1.08))
        ax.tick_params(axis="x", labelrotation=35)
        ax.legend()
    fig.text(0.5, 0.005, "F1 omitted when no slot is actually occupied",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(directory / "metrics-by-day.png", dpi=160)
    plt.close(fig)

    # 6. Daily occupied-slot counts for three representative days.
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
    for ax, weather in zip(axes, ("sunny", "overcast", "rainy")):
        day = next(row["day"] for row in results
                   if row["split"] == "calibration" and row["weather"] == weather)
        subset = [row for row in results if row["day"] == day]
        times = sorted({row["time"] for row in subset})
        truth = [sum(known[(row["image_id"], row["slot_id"])]
                     for row in subset if row["time"] == time) for time in times]
        predictions = [sum(row["predicted_occupancy"]
                           for row in subset if row["time"] == time) for time in times]
        ax.plot(times, truth, "o-", color="black", label="Ground truth")
        ax.plot(times, predictions, "s--", color="0.45", label="Prediction")
        ax.set(title=f"{weather}: {day}", xlabel="Time", ylim=(-0.2, 8.2))
        ax.tick_params(axis="x", labelrotation=55)
    axes[0].set_ylabel("Occupied slots among the eight monitored")
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(directory / "daily-occupancy.png", dpi=160)
    plt.close(fig)

    # 7. Show diverse concrete errors rather than only the earliest images.
    errors = [row for row in results
              if (row["image_id"], row["slot_id"]) in known
              and row["predicted_occupancy"] != known[(row["image_id"], row["slot_id"])]]
    if errors:
        groups = defaultdict(list)
        for error in errors:
            truth = known[(error["image_id"], error["slot_id"])]
            groups[(error["split"], error["weather"], truth)].append(error)
        selected = []
        while groups and len(selected) < 12:
            for key in list(groups):
                if groups[key]:
                    selected.append(groups[key].pop(0))
                if not groups[key]:
                    del groups[key]
                if len(selected) == 12:
                    break
        boxes = slots()
        fig, axes = plt.subplots(3, 4, figsize=(12, 9))
        for ax, row in zip(axes.flat, selected):
            image = load_image(filenames[row["image_id"]])
            region = crop(image, boxes[row["slot_id"]])
            ax.imshow(np.mean(region, axis=2), cmap="gray", vmin=0, vmax=1)
            truth = known[(row["image_id"], row["slot_id"])]
            ax.set_title(f"{row['image_id']} / slot {row['slot_id']}\n"
                         f"truth={truth}, prediction={row['predicted_occupancy']}",
                         fontsize=9)
            ax.axis("off")
        for ax in list(axes.flat)[len(selected):]:
            ax.axis("off")
        fig.tight_layout()
        fig.savefig(directory / "error-examples.png", dpi=160)
        plt.close(fig)
    else:
        # Reusing a trial name must not retain examples from an older run.
        (directory / "error-examples.png").unlink(missing_ok=True)
