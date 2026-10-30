# Research outputs

`figures/` contains byte-identical copies of the original research PNGs with relative source subdirectories retained. `historical_tables/` contains aggregate metric, parameter and trial exports. They are historical outputs whose exact run lineage is not always recorded.

`baseline_reference/cross_asset/metrics.json` and `baseline_reference/tuned/metrics.json` are newly executed deterministic reference results with input hashes, data quality, observed coverage and exact split dates. They are independent of the saved trained-model outputs.

Prediction rows and `runs/` remain local because they contain source observations. The original neural models and tuning directories remain at their original locations and are excluded from Git.

`verification/project_audit.json` records source/preservation checks. Known interrupted and unclassified saved outputs are explicit review warnings, not hidden successes.
