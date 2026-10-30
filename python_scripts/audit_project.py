"""Static source, cleanup and optional original-file preservation audit."""
from __future__ import annotations
import argparse
import ast
import csv
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SECRET = re.compile(r'(?:AIza[\w-]{30,}|sk-(?:proj-)?[\w-]{30,}|ghp_[\w]{30,})')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(root: Path, full: bool=False) -> dict:
    errors, warnings = [], []
    manifest = json.loads((root/'docs/notebook_review_manifest.json').read_text(encoding='utf-8'))
    expected_paths = {r['review_path'] for r in manifest}
    actual_paths = {p.relative_to(root).as_posix() for p in (root/'notebooks').rglob('*.ipynb')}
    if expected_paths != actual_paths:
        errors.append('Active notebook paths differ from the review manifest')
    cell_count = 0
    cleared = 0
    preserved_error_outputs = 0
    for record in manifest:
        path = root/record['review_path']
        if not path.is_file():
            errors.append('Missing review notebook: '+record['review_path'])
            continue
        try:
            notebook = json.loads(path.read_text(encoding='utf-8-sig'))
            if notebook.get('nbformat') != 4 or len(notebook.get('cells',[])) != len(record['cells']):
                raise ValueError('Notebook format or cell count differs from review record')
            for cell,expected in zip(notebook['cells'],record['cells']):
                cell_count += 1
                source = ''.join(cell.get('source',[]))
                if hashlib.sha256(source.encode('utf-8')).hexdigest() != expected['review_source_sha256']:
                    errors.append(f'{record["review_path"]}: cell {expected["cell"]}: reviewed source changed')
                if cell.get('id') != expected['id']:
                    errors.append(f'{record["review_path"]}: cell identity changed')
                if SECRET.search(source):
                    errors.append(f'{record["review_path"]}: possible source credential')
                saved_errors = [o.get('ename','') for o in cell.get('outputs',[]) if o.get('output_type')=='error']
                if expected['action']=='clear_named_error':
                    cleared += 1
                    if source or cell.get('outputs') or cell.get('execution_count') is not None:
                        errors.append(f'{record["review_path"]}: cleared error cell is populated')
                elif saved_errors:
                    if saved_errors != expected['preserved_error_names']:
                        errors.append(f'{record["review_path"]}: undocumented saved error')
                    else:
                        preserved_error_outputs += len(saved_errors)
                        warnings.append(f'{record["review_path"]}: cell {expected["cell"]}: preserved interruption/unclassified error, see cleanup log')
                for output in cell.get('outputs',[]):
                    values = [''.join(output.get('text',[]))]
                    for mime,value in output.get('data',{}).items():
                        if mime.startswith('text/'):
                            values.append(''.join(value) if isinstance(value,list) else str(value))
                    if any(SECRET.search(v) for v in values):
                        errors.append(f'{record["review_path"]}: possible credential in text output')
            if full:
                for key in ['original_path','archive_path']:
                    original = root/record[key]
                    if not original.is_file() or digest(original)!=record['original_sha256']:
                        errors.append('Original notebook missing or changed: '+record[key])
        except (ValueError,TypeError,KeyError) as exc:
            errors.append(f'{record["review_path"]}: {exc}')
    scripts = list((root/'python_scripts').glob('*.py'))
    for path in scripts:
        try:
            source=path.read_text(encoding='utf-8-sig');ast.parse(source)
            if SECRET.search(source): errors.append(path.name+': possible source credential')
        except SyntaxError as exc:
            errors.append(f'{path.name}: syntax error at line {exc.lineno}')
    verified = 0
    if full:
        with (root/'docs/original_file_manifest.csv').open(encoding='utf-8',newline='') as handle:
            for record in csv.DictReader(handle):
                path=(root/record['path']).resolve()
                if not path.is_relative_to(root.resolve()) or not path.is_file() or digest(path)!=record['sha256']:
                    errors.append('Original file missing or changed: '+record['path'])
                else: verified += 1
        for record in json.loads((root/'docs/editor_recovery_manifest.json').read_text(encoding='utf-8')):
            path=root/record['preserved_path']
            if not path.is_file() or digest(path)!=record['sha256']:
                errors.append('Editor backup snapshot missing or changed: '+record['preserved_path'])
    else:
        if not (root/'data/raw/gold_2007_to_present.csv').is_file():
            warnings.append('Local research datasets excluded/unavailable; no numerical reproduction was performed')
    return {'review_notebooks':len(manifest),'cell_positions_preserved':cell_count,
            'named_error_cells_cleared_in_copies':cleared,
            'preserved_interrupted_or_unclassified_error_outputs':preserved_error_outputs,
            'python_scripts_checked':len(scripts),'original_file_hashes_verified':verified,
            'errors':errors,'warnings':warnings,
            'scope':'Static hygiene and exact preservation; not execution of historical model experiments'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-originals',action='store_true')
    args=parser.parse_args()
    result=audit(ROOT,args.verify_originals)
    print(json.dumps(result,indent=2))
    raise SystemExit(bool(result['errors']))
