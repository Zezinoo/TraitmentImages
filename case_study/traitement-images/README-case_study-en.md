# Case study: setup

1. Extract this archive in a working directory. It contains `traitement-images/case_study/` and `traitement-images/ressources-case_study/`.
2. Copy these two folders into the `traitement-images/` project used in earlier labs, then open that project in Visual Studio Code.
3. Select the interpreter from your existing `.venv` virtual environment. If a dependency is missing, run `python3 -m pip install -r ressources-case_study/requirements.txt` from the project root, in a terminal where this environment is activated.
4. From the project root, run `python3 case_study/explore.py`. Follow the subject instructions to inspect the images and record your initial pipeline proposal before running trials. Then run `python3 case_study/run.py --method baseline --name baseline`. Results are saved in `case_study/results/`.
5. Update `case_study/project-log.md` as you work. At the end of each classroom session, use `case_study/export_checkpoint.py` as described in the subject, then submit the generated archive on Moodle.

The subject PDF details the required work and submission instructions. The solution scripts and evaluation-set labels are not included in this archive.
