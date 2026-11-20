"""Rebuild a trial's interactive report without running image processing again."""

import argparse
import csv

from tools import RESULTS, RESOURCES, available_images, slots
from parking_report import create_report, validate_trial_name


def view(trial):
    validate_trial_name(trial)
    with (RESULTS / f"predictions-{trial}.csv").open(newline="", encoding="utf-8") as stream:
        results = list(csv.DictReader(stream))
    page = create_report(results, available_images(), slots(), RESOURCES,
                         RESULTS / trial / "report", lang="en")
    print("Open this report in your browser:", page.resolve().as_uri())
    print("After running another trial under the same name, refresh the browser page.")
    return page


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trial", default="baseline", help="Name used with run.py --name")
    view(parser.parse_args().trial)
