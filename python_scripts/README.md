# Python tools

- `baseline_forecast.py`: read-only canonical-CSV parser, explicit regime splits and next-observation persistence/Close/training-mean reference forecasts.
- `test_baselines.py`: six synthetic tests covering origin/target alignment, training-only constants, metrics, missing data, duplicates and overlapping regimes.
- `audit_project.py`: static notebook/source/cleanup checks and optional original/recovery checksum verification.

All require the Python standard library only. They do not retrain historical models or modify source datasets. Historical implementations remain in the notebooks with exact full copies preserved locally.
