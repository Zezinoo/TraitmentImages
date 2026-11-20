"""Package a compact snapshot at the end of a classroom session."""

import argparse
from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile

from tools import ROOT, RESULTS


def export(number, trial, extra_figures=()):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", trial):
        raise ValueError("A trial name may contain only letters, digits, _ or -")

    log = ROOT / "project-log.md"
    predictions = RESULTS / f"predictions-{trial}.csv"
    figures = [
        RESULTS / trial / "confusion-matrices.png",
        RESULTS / trial / "metrics-by-day.png",
    ]
    files = [log, predictions, *figures]
    files.extend(path for path in ROOT.rglob("*.py")
                 if not any(part == "results" or part.startswith(".")
                            for part in path.relative_to(ROOT).parts))
    files.append(ROOT / "parking_report.html")
    for figure in extra_figures:
        path = Path(figure)
        if path.parent == Path("."):
            path = RESULTS / path
        path = path.resolve()
        if not path.is_relative_to(RESULTS.resolve()):
            raise ValueError("Additional figures must be inside case_study/results/")
        if path.suffix.lower() not in {".png", ".pdf", ".svg"}:
            raise ValueError("Additional figures must be PNG, PDF, or SVG files")
        files.append(path)
    missing = [str(path) for path in files if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing files: " + ", ".join(missing))

    output = RESULTS / f"checkpoint-{number}.zip"
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(set(files)):
            archive.write(path, Path("case_study") / path.relative_to(ROOT))
    print("Archive to submit on Moodle:", output)
    print("Check that you have completed the project log before submitting.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("number", type=int, choices=(1, 2),
                        help="Checkpoint number")
    parser.add_argument("--trial", required=True,
                        help="Name used with run.py --name")
    parser.add_argument("--figure", action="append", default=[],
                        help="Figure filename in results/ or a path inside that folder; repeat as needed")
    arguments = parser.parse_args()
    export(arguments.number, arguments.trial, arguments.figure)
