# Limitations

- Historical neural, statistical and tuned models were not rerun from fresh kernels. Saved outputs and result tables are preserved evidence, not independently reproduced findings.
- Regime definitions, splits, scaling and target alignment differ between branches. Exact years and forecast origin must accompany comparisons.
- Full-data transformation fitting, manual column relabelling, backward fill and asset-filename mismatches are present in preserved source. See the code review before using those branches.
- Cleared named-error cells may contain useful training code as well as failing diagnostics; complete original cells remain available. A clean saved output record is not proof of executable completeness.
- An interrupted training cell and an unnamed error remain flagged because their outputs do not establish incorrect mathematics.
- Source-provider permissions, download timestamps, adjustment defaults, currency/contract conventions, and complete data derivation are not frozen. Filenames do not establish actual temporal coverage.
- Calendar gaps may be weekends, closures or missing observations; no exchange/calendar or timezone audit is claimed. Source OHLC relationships and adjusted-price conventions require review.
- Generic result filenames may have been overwritten across assets. Historical model and trial artifacts need a run identifier, data hash, cell and environment before assigning definitive lineage.
- Fractions and percentages in MAPE columns are not automatically comparable. Price-level R2 is not a trading backtest or evidence of economic profitability.
- Seeds alone do not establish deterministic neural execution. Repeat runs, uncertainty, held-out temporal robustness and test-set independence need evaluation.
- The new persistence/close/mean reference has its own explicit protocol; it does not certify or reproduce historical trained models.
- Authors, affiliation, data/figure sharing permissions and licenses remain to be confirmed. No institution, publication status or acronym expansion is invented.
