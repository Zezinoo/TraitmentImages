# View and improve your method

From the root of `traitement-images/`, run `python3 case_study/explore.py`. Examine the images and record an initial processing pipeline proposal in the project log before running trials. Then run the baseline supplied separately in `baseline.py`:

```sh
python3 case_study/run.py --method baseline --name baseline
```

The file `pipeline.py` contains an editable copy of the simple method. You may improve it or rewrite your pipeline entirely. Keep the documented `predict()` interface. Both approaches require the same understanding and justification of your choices. Run your trial:

```sh
python3 case_study/run.py --name trial1
```

Open `case_study/results/trial1/report/index.html` in Firefox or another browser. The terminal also prints the report's local URL. Displaying the report requires no additional library, server, or Internet connection.

The single archive contains French and English documentation. Scripts, commands, and result filenames are shared by both languages. Use the report's "Langue / Language" menu to switch between French and English without rerunning image processing.

For each photograph, the report shows predicted free and occupied spaces, their identifiers, counts, and the occupancy rate for the eight monitored spaces. Dashed outlines indicate a predicted free space; solid outlines indicate a predicted occupied space. The table associates each parking-space ID with its predicted state. The report's `occupancy.csv` file contains counts and occupancy rates for each photograph; `predictions.csv` contains scores and decisions for each space.

Decision previews in PNG format use these outline styles over a grayscale photograph. Each identifier is followed by `0` for a space predicted free or `1` for a space predicted occupied. In exploration previews, `?` means that no decision is displayed. Grayscale conversion affects only the PNG previews: the original files and the RGB arrays used by your method remain unchanged.

For a trial of your own pipeline, the report uses the decisions computed by your `predict()` function, without calling the demonstrator. Compare these predictions with the reference labels. Use the trial's confusion matrices and other diagnostic figures to analyze errors on the tuning and validation sets. Evaluation-set labels remain reserved for the instructor.

The report does not automatically show masks or other intermediate steps of your method. Add the visualizations needed to explain your choices. Diagnostic plots use grayscale, hatching, and line styles to remain readable in black-and-white print.

The `--method baseline` option runs the baseline and generates the corresponding report. By default, `run.py` calls your `predict()` function defined in `pipeline.py`. The trial name `baseline` is reserved for the baseline method to protect this point of comparison.

After changing your processing pipeline or its parameters, use a new name to keep the previous trial's results. A trial name does not save the code or its parameters: keep them separately so that you can reproduce the results. For example:

```sh
python3 case_study/run.py --name trial2
```

To compare two trials, open their reports in separate tabs and select the same photograph. After changing the code, rerun the trial to recompute the results and regenerate the report. If you reuse a trial name, that run replaces the corresponding results and report; then refresh the browser page.

To create or regenerate the report from `case_study/results/predictions-trial1.csv` without rerunning the processing pipeline, use:

```sh
python3 case_study/view_results.py --trial trial1
```

Keep the entire `report/` folder when moving or sharing a report: it contains the HTML page, CSV files, and photographs needed to view it.

Checkpoint archives contain the current Python code, the `parking_report.html` template, the project log, the prediction CSV, and the figures `confusion-matrices.png` and `metrics-by-day.png`. Add personal figures with the repeatable `--figure` option. They must be PNG, PDF, or SVG files inside `case_study/results/`. Archives do not include the `report/` folder or dataset photographs.

## Checkpoint 1: run a personal processing step

Submit code for one processing step motivated by your observations and run on at least one parking space. The full pipeline may remain unfinished. Save personal Python files inside `case_study/` so that the archive includes them. Save an input-and-result figure as `case_study/results/first-step.png`. Explain the choice, result, and reproduction command in the log.

After running the baseline, create the archive:

```sh
python3 case_study/export_checkpoint.py 1 --trial baseline --figure first-step.png
```

The baseline results accompany your personal code and figure. The exporter does not import `pipeline.py`: a syntax error in the pipeline under development does not prevent archive creation. If no figure could be produced, omit `--figure` and its path so that you can still submit the code and explain the difficulty.

## Checkpoint 2: a prototype in progress and analyzed trials

Present the steps actually run, their results, and one difficult situation. Explain the mask and measurement if available; identify missing steps. A complete pipeline is not required at this stage.

To attach `case_study/results/checkpoint-2.png` with results from a completed trial named `trial1`, run:

```sh
python3 case_study/export_checkpoint.py 2 --trial trial1 --figure checkpoint-2.png
```

If your method does not produce decisions yet, replace `trial1` with `baseline`. Your sources and personal figure are also included. Analyze intermediate results in the log and distinguish them from baseline results.

## Final submission: a complete pipeline and a finished report

The final version must run on all supplied images, return finite scores and decisions of 0 or 1, and be reproducible using the stated parameters, commands, and libraries. Measure and analyze errors; successful execution does not guarantee that every decision is correct. Include the finished report and files required by the subject in the final compressed folder.
