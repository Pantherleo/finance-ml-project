# GitHub preparation

The prepared project includes organized review notebooks, source/cleanup manifests, research documentation, scoped comments, original figures, historical aggregate exports, a deterministic reference baseline, tests and GitHub Actions checks.

The `.gitignore` keeps original root notebooks, root datasets/outputs, archives, editor backups, saved neural models, prediction tables and local training logs out of Git. The nested MLL_Datasets coursework repository is deliberately excluded and untouched. Data availability in a clone is documented rather than assumed.

Before publication, confirm authors, supervisor, affiliation, source citations, code/data/figure permissions and license choices. Review notebook embedded outputs and figure labels for private or restricted content. The scoped credential scan does not inspect every image/binary payload. Resolve run lineage before presenting historical scores as a unified benchmark.

Run the audit and tests, inspect staged filenames, and choose the desired repository and visibility before uploading. No Git repository is initialized and nothing is uploaded during the research organization step.

```bash
git init -b main
git add .
git status --short
git diff --cached --stat
python python_scripts/audit_project.py
python -m unittest discover -s python_scripts -p "test_*.py" -v
git commit -m "Organize cross-asset forecasting research and add reproducible reference checks"
```

Create the intended repository, add its URL as origin and push main after review. Do not force-add ignored datasets, archives, coursework repositories or model files without an explicit sharing decision.
