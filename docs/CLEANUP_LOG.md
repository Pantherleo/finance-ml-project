# Preservation, editor recovery and cleanup

All pre-existing files remain at their original locations with unchanged bytes, including the nested coursework repository's Git metadata. Exact full copies of research notebooks are also stored in `archive/original_notebooks/`. The manifest records the original hashes.

Three VS Code backups were preserved, along with relevant local-history snapshots. The NIFTY backup has the same source cells as its saved notebook. The Gold backup adds two empty cells to otherwise matching source. The original zero-byte lab notebook has a four-cell editor backup containing Hill-cipher/cryptography exercises; that full backup is retained under the recovery archive rather than labelled as stock forecasting code. No editor backup or history store was altered.

The 26 valid root research notebooks have organized review copies. Every original cell position and identity remains. Twenty-two cells with named saved exceptions have their source, outputs and execution count cleared only in those copies. Originals retain all removed source and output.

`nift50_latest` cell 6 has KeyboardInterrupt, and `goldd` cell 19 has an unnamed error output. Their code/output are retained for manual review because neither establishes a numerically wrong implementation. The static audit reports these two exceptions explicitly as warnings.

Selected non-error cells receive review comments only. Their original source text remains exact after the documented prefix. Other cells and saved outputs remain unchanged. No entire file is deleted and no surprising score is used as a reason to delete code.

`notebook_review_manifest.json` lists every cell, action, source hashes and error names. `editor_recovery_manifest.json` identifies preserved recovery snapshots. Root data, model artifacts and coursework remain local and excluded from the proposed GitHub project.
