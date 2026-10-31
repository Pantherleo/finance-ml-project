# GitHub publication

The complete prepared research project is approved for publication to https://github.com/Pantherleo/finance-ml-project on `main`. The user explicitly approved the destination and prepared payload on 2026-10-31.

The earlier GitHub commit contained only the first partial upload. On 2026-10-31 its history was merged into the complete local research tree, restoring the 110 missing prepared files without rewriting the remote history.

## Verification on 2026-10-31

- Static project audit: zero errors; two documented preserved notebook interruptions/unclassified errors remain.
- All six protocol/parser/metric tests passed.
- Both independent baseline schemes reran across all four assets (2,817 cross-asset and 2,819 tuned forecast pairs). Their metrics exactly match the committed reference JSON files.
- Full local preservation audit: 186 of 187 original hashes match. The sole difference is `MLL_Datasets/.git/FETCH_HEAD`, mutable Git fetch metadata in the excluded coursework repository. The historical manifest is retained unchanged; no research-content mismatch was reported.

Raw datasets, root originals, archives, editor backups, saved models, prediction tables and the separate coursework repository remain excluded through `.gitignore`. Local reproduction requires the data described in the data catalogue. Historical neural models were not retrained; existing scientific limitations remain documented.

For subsequent updates:

```bash
python python_scripts/audit_project.py
python -m unittest discover -s python_scripts -p "test_*.py" -v
git status --short
git add <reviewed-files>
git commit -m "Describe the research update"
git push origin main
```

Authorship, licensing, source permissions and benchmark lineage remain research documentation limitations, not claims resolved by repository publication.
