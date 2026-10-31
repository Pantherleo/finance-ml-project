# Verification record

Prepared on 2026-10-30 using Python 3.12.4.

- All 187 pre-existing files retain their original paths and SHA-256 hashes. This includes 158 project-content files plus the nested coursework Git metadata.
- All 38 saved notebooks were inspected. Twenty-six root research notebooks have organized copies retaining all 465 cell positions and identities. Eleven coursework notebooks are unchanged and excluded from the main research layout.
- Twenty-two named-error cells are cleared only in organized copies. Full code and outputs remain in exact originals. All other retained source is verified exact after any review comment prefix.
- One KeyboardInterrupt and one unnamed error are intentionally preserved and reported as warnings. They are not classified as incorrect numerical output.
- Three live editor-backup snapshots and matching notebook payloads are preserved, including the complete four-cell cryptography lab backup. Relevant editor history snapshots are preserved separately. No editor store is altered.
- All four canonical asset files were parsed without modifying any source data. Quality and actual date ranges are recorded.
- Six synthetic protocol/parser/metric tests passed. Both regime schemes completed independent reference baselines across all four assets.
- All 26 organized notebook schemas passed nbformat validation. Python tools passed static syntax checks.
- Historical model training, provider downloads, ablation reruns and saved-model loading were not performed. No global packages were installed or changed.
- No original file was deleted or moved. No Git repository was initialized and no files were uploaded.

The audit is `python python_scripts/audit_project.py --verify-originals`. Source and recovery manifests record the exact preservation boundary. Model validity and economic interpretation remain subject to the documented review findings.

## Follow-up verification on 2026-10-31

The Git repository is now initialized and the complete prepared tree is being published to `Pantherleo/finance-ml-project`, preserving the earlier partial-upload commit. Static audit passed with zero errors and the same two documented warnings; all six tests passed. Both baseline schemes reran across all four assets and exactly reproduced the stored metrics.

The full preservation recheck matched 186 of 187 original hashes. Only the excluded coursework repository's mutable `MLL_Datasets/.git/FETCH_HEAD` differs from the preparation snapshot. No research-content mismatch was reported. The original manifest remains unchanged, preserving the historical record. See [GitHub publication](GITHUB_PREPARATION.md).
