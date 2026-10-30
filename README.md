# Finance ML Project: Cross-Asset Forecasting

A notebook-led research collection for predicting market High/Low values across gold, crude oil, USD/INR and NIFTY 50. The experiments include LSTM/BiLSTM, TCN, Conv1D–LSTM, ConvLSTM-style models, tree-based regressors, statistical time-series comparisons, regime-specific tuning and an architecture/training-protocol ablation.

**Research status:** exploratory experiments with preserved historical results. The code has been inventoried and reviewed; historical models have not been retrained during repository preparation. An independent, executable next-observation baseline provides a documented reference.

## Start here

1. [Notebook catalogue](docs/NOTEBOOK_CATALOG.md) and [research overview](docs/RESEARCH_OVERVIEW.md).
2. [Reproduction guide](docs/REPRODUCIBILITY.md) and [data catalogue](docs/DATA_CATALOG.md).
3. [Code review](docs/CODE_REVIEW.md), [historical results](docs/HISTORICAL_RESULTS.md) and [limitations](docs/LIMITATIONS.md).
4. [Cleanup and recovery log](docs/CLEANUP_LOG.md), [verification](docs/VERIFICATION.md) and [GitHub preparation](docs/GITHUB_PREPARATION.md).

## Repository layout

```text
notebooks/00_acquisition/             Data-download experiment
notebooks/01_diagnostics/             Diagnostics, statistics and workshops
notebooks/02_model_comparisons/       Broad model comparisons
notebooks/03_tuning/                  Asset/regime and optimizer experiments
notebooks/04_cross_asset_and_ablation/Parameterized cross-asset pipeline and ablation
notebooks/05_asset_exploration/       Earlier asset-specific experiments
python_scripts/                      Standard-library baseline, audit and tests
configs/                             Explicit regime definitions from source
data/raw/                            Unchanged local copies of source CSVs
reports/figures/                     Organized original PNG outputs
reports/historical_tables/           Historical aggregate result/trial exports
reports/baseline_reference/          Newly executed aggregate reference metrics
docs/                                Methods, review findings and manifests
archive/                             Full original notebook copies and editor/history snapshots
```

Every original file remains at its original path with unchanged contents. The root notebooks are complete originals, and additional exact notebook copies are archived. Organized notebooks are review copies retaining every original cell position. Only cells with named saved exceptions are cleared there. An interrupted run and an unnamed error remain explicitly flagged for manual review. [Cleanup log](docs/CLEANUP_LOG.md).

## Run the verified tools

Python 3.12 and the standard library are sufficient:

```bash
python python_scripts/audit_project.py
python -m unittest discover -s python_scripts -p "test_*.py" -v
python python_scripts/baseline_forecast.py
```

The baseline requires the four approved local price CSVs in `data/raw/`. It predicts next-observed-day High/Low using persistence, current Close and a training-only constant mean. It uses explicit per-regime chronological 70/15/15 partitions and excludes forecast pairs crossing split/regime boundaries. [Reference metrics](reports/baseline_reference/cross_asset/metrics.json) record data checksums, date ranges and quality exclusions.

The default `cross_asset` regime years come from `final.1.ipynb`. A separate `tuned` scheme reproduces the different years in the tuned NIFTY experiment. These labels are not interchangeable. Neither independent baseline is a rerun of a trained notebook model.

For complete local preservation:

```bash
python python_scripts/audit_project.py --verify-originals
```

## Research environment and data

Install `requirements-research.txt` in a clean environment for notebook work. The requirements reflect imports, not a recovered lockfile. Notebook cells share state and some export filenames overlap, so use a disposable execution copy and explicitly select the project root as the working directory.

Source CSVs, original root notebooks, archived backups, trained models, local logs and prediction tables are excluded from Git. The separate `MLL_Datasets` coursework repository remains untouched and is excluded from the research upload. Original figures and aggregate historical exports are proposed tracked outputs, subject to source and sharing review.

The acquisition notebook requests data through yfinance, but download dates, adjustment settings, provider permissions and complete derivation histories are not frozen. Filenames ending in present do not establish actual coverage. [Data catalogue](docs/DATA_CATALOG.md).

## Interpreting results

Report exact assets, dates, regimes, targets, forecast origins and protocols alongside metrics. Historical price-prediction scores do not constitute a trading backtest. Authors, supervisors, institutional affiliation, source citations and licenses require confirmation; none has been invented.
