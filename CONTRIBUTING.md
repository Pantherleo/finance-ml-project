# Contributing

Preserve complete original notebooks and distinguish historical outputs from newly reproduced experiments. Add an experiment record with code revision, dataset hashes, asset, exact regime years, target definition, forecast origin, split dates and transformation fit scope.

Fit transforms and tune hyperparameters inside training/validation data. Keep the final test interval out of model selection. Audit shifted labels at split boundaries and disclose whether Close(t) is available when a prediction is issued. Do not mix MAPE fractions and percentages or select a winner across mismatched test samples.

Use `python_scripts/` for Python tools and the appropriate notebook group for new experiments. Update the review manifest for intentional source changes. Root originals, unrelated coursework and backups remain unchanged provenance records.

Run `python python_scripts/audit_project.py` and `python -m unittest discover -s python_scripts -p "test_*.py" -v`. For behavior changes, also execute the selected notebook from a fresh kernel in an isolated copy and report what ran. Do not treat a retained saved output as a fresh reproduced result.
