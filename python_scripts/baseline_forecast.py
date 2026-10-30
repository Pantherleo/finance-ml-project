"""Independent next-observed-day High/Low reference forecasts; standard library only."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
from statistics import fmean

ROOT = Path(__file__).resolve().parents[1]
ASSETS = {'gold': 'gold_2007_to_present.csv', 'crude_oil': 'crude_oil_2007_to_present.csv',
          'forex_usd_inr': 'forex_usd_inr_2007_to_present.csv', 'nifty50': 'nifty50_2007_to_now.csv'}


def parse_date(value: str):
    for fmt in ('%d-%m-%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            pass
    raise ValueError('Date must use DD-MM-YYYY or YYYY-MM-DD')


def read_prices(handle) -> tuple[list[dict], dict]:
    reader = csv.DictReader(handle)
    if not {'Date','Close','High','Low'}.issubset(reader.fieldnames or []):
        raise ValueError('Expected canonical Date/Close/High/Low columns; multirow Price headers need explicit normalization')
    rows, rejected = [], Counter()
    input_count = 0
    for raw in reader:
        input_count += 1
        try:
            day = parse_date(raw['Date'])
        except (ValueError, TypeError, AttributeError):
            rejected['invalid_date'] += 1
            continue
        try:
            prices = {key: float(raw[key]) for key in ('Close','High','Low')}
        except (ValueError, TypeError):
            rejected['missing_or_nonnumeric_price'] += 1
            continue
        if not all(math.isfinite(v) for v in prices.values()):
            rejected['nonfinite_price'] += 1
            continue
        if prices['High'] < prices['Low']:
            rejected['high_below_low'] += 1
            continue
        rows.append({'date':day, **prices})
    rows.sort(key=lambda r:r['date'])
    if len({r['date'] for r in rows}) != len(rows):
        raise ValueError('Duplicate dates require an explicit source-data decision')
    if len(rows) < 10:
        raise ValueError('Too few valid observations')
    gaps = [(b['date']-a['date']).days for a,b in zip(rows,rows[1:])]
    return rows, {'input_rows':input_count, 'accepted_rows':len(rows), 'rejected_by_reason':dict(rejected),
                  'first_date':rows[0]['date'].isoformat(), 'last_date':rows[-1]['date'].isoformat(),
                  'max_calendar_gap_days':max(gaps,default=0),
                  'close_outside_high_low_rows':sum(not r['Low']<=r['Close']<=r['High'] for r in rows),
                  'cleaning':'Read-only exclusion of invalid Date/Close/High/Low and High<Low; no fill or resampling'}


def metrics(actual: list[float], predicted: list[float]) -> dict:
    if not actual or len(actual)!=len(predicted):
        raise ValueError('Actual and predicted arrays need equal nonzero lengths')
    if not all(math.isfinite(v) for v in actual+predicted):
        raise ValueError('Nonfinite metric input')
    errors = [a-p for a,p in zip(actual,predicted)]
    sse = sum(e*e for e in errors)
    center = fmean(actual)
    sst = sum((a-center)**2 for a in actual)
    return {'mae':fmean(abs(e) for e in errors), 'rmse':math.sqrt(sse/len(errors)),
            'r2':1-sse/sst if sst else None}


def evaluate_regime(rows: list[dict]) -> tuple[dict,list[dict]]:
    n = len(rows)
    train_end, val_end = int(n*.70), int(n*.85)
    if train_end<2 or val_end>=n-1:
        return {'status':'insufficient_observations','rows':n}, []
    constants = {target:fmean(r[target] for r in rows[1:train_end]) for target in ('High','Low')}
    predictions = []
    # Origin and target must both be inside test. No target crosses a regime/split boundary.
    for origin in range(val_end,n-1):
        today, tomorrow = rows[origin], rows[origin+1]
        row = {'origin_date':today['date'].isoformat(), 'target_date':tomorrow['date'].isoformat()}
        for target in ('High','Low'):
            row[target+'_actual'] = tomorrow[target]
            row[target+'_persistence'] = today[target]
            row[target+'_current_close'] = today['Close']
            row[target+'_train_mean'] = constants[target]
        predictions.append(row)
    scores = {target:{model:metrics([r[target+'_actual'] for r in predictions],
                                    [r[target+'_'+model] for r in predictions])
                      for model in ('persistence','current_close','train_mean')} for target in ('High','Low')}
    return {'status':'completed','rows':n,'train_rows':train_end,'validation_rows':val_end-train_end,
            'test_rows':n-val_end,'test_forecast_pairs':len(predictions),
            'train_start':rows[0]['date'].isoformat(),'train_end':rows[train_end-1]['date'].isoformat(),
            'validation_start':rows[train_end]['date'].isoformat(),'validation_end':rows[val_end-1]['date'].isoformat(),
            'test_start':rows[val_end]['date'].isoformat(),'test_end':rows[-1]['date'].isoformat(),
            'training_constants':constants,'metrics':scores}, predictions


def evaluate(rows: list[dict], regimes: dict) -> tuple[dict,list[dict]]:
    summary, all_predictions = {}, []
    assigned = set()
    for name,(first,last) in regimes.items():
        subset = [r for r in rows if r['date'].year>=first and (last is None or r['date'].year<=last)]
        for row in subset:
            if row['date'] in assigned:
                raise ValueError('Regime definitions overlap')
            assigned.add(row['date'])
        result,predictions = evaluate_regime(subset)
        summary[name] = result
        all_predictions.extend({'regime':name,**p} for p in predictions)
    return summary,all_predictions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,default=ROOT/'data/raw')
    parser.add_argument('--scheme',choices=('cross_asset','tuned'),default='cross_asset')
    parser.add_argument('--output',type=Path,default=ROOT/'reports/runs/reference_baselines')
    args = parser.parse_args()
    regimes = json.loads((ROOT/'configs/regimes.json').read_text(encoding='utf-8'))[args.scheme]['regimes']
    result = {'regime_scheme':args.scheme,'regimes':regimes,
              'forecast_origin':'After the origin observation closes; forecast High/Low of the next available observation',
              'split':'Per-regime chronological 70/15/15 on accepted observations; no cross-boundary forecast pairs',
              'units':'Source price units per asset, unverified; no currency conversion or adjusted-price reconciliation',
              'comparison_limit':'Independent reference; historical model results are not rerun or aligned to these exact samples',
              'assets':{}}
    predictions = []
    for name,filename in ASSETS.items():
        path = args.data_dir/filename
        if not path.is_file():
            parser.error('Missing approved local data: '+str(path))
        with path.open(encoding='utf-8-sig',newline='') as handle:
            rows,quality = read_prices(handle)
        summary,forecast = evaluate(rows,regimes)
        result['assets'][name] = {'file':filename,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                                  'data_quality':quality,'regime_results':summary}
        predictions.extend({'asset':name,**p} for p in forecast)
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'metrics.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    if predictions:
        with (args.output/'predictions.csv').open('w',newline='',encoding='utf-8') as handle:
            writer = csv.DictWriter(handle,fieldnames=list(predictions[0]));writer.writeheader();writer.writerows(predictions)
    print(json.dumps({'scheme':args.scheme,'assets':len(result['assets']),'forecast_pairs':len(predictions),
                      'output':str(args.output),'data_quality':{a:r['data_quality'] for a,r in result['assets'].items()}},indent=2))


if __name__=='__main__':
    main()
