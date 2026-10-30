# Research overview

## Scope

The core collection compares price-forecasting architectures across gold, crude oil, USD/INR and NIFTY 50 and partitions observations into four historical regimes. An acquisition experiment also requests Apple and Alphabet data. The associated general machine-learning coursework is a separate nested repository and is not part of the forecasting benchmark.

Recovered implementations include diagnostic statistics, stationarity/volatility tools, LSTM/BiLSTM, TCN, Conv1D–LSTM, ConvLSTM-style networks, CatBoost, XGBoost and statistical forecasting branches. The ConvLSTM-style label is retained as the source author's architecture name; it must not automatically be equated with a canonical ConvLSTM implementation.

`final.1.ipynb` contains a parameterized cross-asset pipeline and a Gold/DF1 ablation. The `final.try.*` notebooks contain longer asset-specific regime, target, tuning and architecture variants. These are related experiments, not a single locked implementation.

## Regime definitions found in source

| Scheme | DF1 | DF2 | DF3 | DF4 |
| --- | --- | --- | --- | --- |
| cross_asset: final.1 / analysis diagnostic | 2007–2011 | 2012–2019 | 2020–2022 | 2023 onward |
| tuned: final.try.nifty final tuning cell | 2007–2010 | 2011–2019 | 2020–2021 | 2022 onward |

These exact definitions are stored in `configs/regimes.json`. Other historical branches must be checked individually. Regime names without years are insufficient for comparing results. Economic or statistical justification of the boundaries has not been established by organization alone.

## Targets and information timing

Several later branches construct `High(t+1)/Close(t)` and `Low(t+1)/Close(t)` targets and reconstruct price forecasts using Close(t). Sequence builders often use `X[i-lookback:i]` while assigning the shifted target at row i. Document the intended forecast origin and whether Close(t) is known at issuance; timestamped reconstruction information must be consistent with the stated forecast task.

The independent reference defines its origin after the origin observation closes and predicts High/Low of the next available observation. It uses no resampling, no imputation and no fitted neural model. Origin and target remain inside the same regime and test partition. Training constants use training target observations only.

## Evaluation requirements

Report input hashes, actual date ranges, row exclusions, lookback, train/validation/test boundaries, target dates, fitted transformations, trial budgets, seeds and exact environments. Separate model-selection evidence from final-test evidence. Compare against simple same-sample reference forecasts and repeat stochastic training to estimate variability.

Price-level error metrics alone do not show strategy returns, execution feasibility or transaction-cost robustness. The present collection is a forecasting study, not a validated trading system. See the code review for concrete leakage and provenance issues that remain in preserved experiments.
