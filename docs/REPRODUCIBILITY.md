# Reproduction guide

## Verified standard-library tools

```bash
python python_scripts/audit_project.py
python -m unittest discover -s python_scripts -p "test_*.py" -v
python python_scripts/baseline_forecast.py --scheme cross_asset
python python_scripts/baseline_forecast.py --scheme tuned
python python_scripts/audit_project.py --verify-originals
```

The baseline needs four approved local canonical price files in `data/raw/`. It reads Date/Close/High/Low, accepts explicit DD-MM-YYYY or YYYY-MM-DD dates, rejects duplicate accepted dates, sorts chronologically, and excludes invalid/missing/nonfinite rows and High<Low records. It reports exclusions without changing source data. It does not forward/backward fill, resample or assume a trading-day calendar. Close outside High/Low is reported rather than automatically rewritten because adjusted-price semantics are not confirmed.

The forecast origin is after the origin observation closes. Persistence uses that day's High/Low, current-close predicts both next High and Low from that day's Close, and a fixed training mean uses training target observations only. Within each configured regime, rows are split at floor(0.70*n) and floor(0.85*n). Forecast origin and next-observation target must both lie in test; cross-boundary pairs are excluded. Validation is reserved but not used for tuning these fixed references.

Metrics are MAE, RMSE and R2 on source price scales. Constant-target R2 is unavailable. Forecasts span the next retained observation, so gaps can exceed one calendar day. The reference is deterministic for fixed files and options. It is not directly matched to historical models' exact lookbacks, exclusions or test pairs.

Reference aggregate files are in `reports/baseline_reference/{cross_asset,tuned}/metrics.json`. Row-level predictions include source values and remain local. Default new runs go under ignored `reports/runs/`.

## Notebook environment

```bash
python -m venv .venv
```

Activate with `.\.venv\Scripts\Activate.ps1` in PowerShell or `source .venv/bin/activate` on macOS/Linux, then:

```bash
python -m pip install -r requirements-research.txt
python -m jupyterlab
```

Requirements are inferred from research imports, not a validated historical lockfile. Record Python, library versions, platform, hardware and all seeds when a full workflow succeeds. No packages are installed or changed during repository preparation.

## Historical execution

Original datasets remain under their original root filenames, so no input paths were silently rewritten. Jupyter may set its working directory to the organized notebook's folder. In a new setup cell, explicitly select the project root:

```python
from pathlib import Path
import os
ROOT = next(p for p in [Path.cwd(), *Path.cwd().parents]
            if (p / 'docs' / 'notebook_review_manifest.json').is_file())
os.chdir(ROOT)
```

Run selected experiments in a disposable project copy because exports and download cells can overwrite filenames. The review copies clear 22 named-error cells, potentially removing definitions needed later. Use the full original cell for debugging or a deliberate implementation fix rather than assuming the cleaned copy is automatically runnable end to end.

Two saved error outputs are intentionally retained: an interrupted run and an unnamed error. The audit reports them as known review warnings; it does not hide them as successful runs. The cryptography lab backup and general coursework remain non-benchmark supporting material.

## Preservation and scope

The full audit verifies every original file hash, exact notebook snapshots and editor/history copies. A normal data-free clone verifies the review manifest and Python syntax, and reports unavailable datasets. CI uses only the standard library and synthetic tests. Notebook model training, data download, ablation reruns and saved-model loading are not performed by these checks.
