# Source review findings

Original executable statements are preserved except named-error cells cleared in review copies. Findings without saved exceptions are documented and commented rather than silently rewritten.

| Location | Finding | Required interpretation or follow-up |
| --- | --- | --- |
| `analysis`, cell 3 | Replaces column labels with Date/Open/High/Low/Close/Volume while source canonical order is Date/Close/High/Low/Open/Volume | Check positional reassignment: Open and Close meanings can be swapped |
| `analysis`, cell 3 | Forward fill followed by backward fill | Backward fill can expose later observations; disclose purpose and avoid using future information in predictive preprocessing |
| `final_try_crude`, cell 2 | Selects the NIFTY CSV despite a crude notebook name | Attribute the experiment to the selected input, not filename |
| `final.try.gold`, cell 18 | A later cell selects NIFTY data | Maintain run/cell-level asset provenance |
| `final.1` versus `final.try.nifty` tuning | Different regime boundary years | Store/report exact years; do not merge DF labels across schemes |
| `crude`, cell 6 sequence branch | Fits a scaler on the full feature matrix before split | Holdout distribution information can enter fitted preprocessing; separate from its earlier train-only branch |
| `All_models_script`, cell 22; `forex_true`, cell 27 | Full-matrix X/y scaling branches coexist with train-only branches | Audit each branch independently; one good branch does not validate every model's reported score |
| Statistical notebooks, early neural cells | Multiple scaling/split variants | Verify fit scope and sequence alignment before comparisons |
| Later ratio-target pipelines | Shifted target and Close(t) reconstruction with history windows ending before row i | Define origin, input availability and reconstructed target date explicitly; check off-by-one and boundary labels |
| Generic export filenames | Asset-specific notebooks write identically named result files | The latest writer can overwrite earlier asset exports; generic root tables need explicit run lineage |
| MAPE columns across exports | Some code returns fractional errors; other branches multiply by 100 | Confirm the generating function before labelling percentages or pooling tables |
| Saved errors | 22 named exceptions, one interruption and one unnamed error | Named exceptions are cleared only in review copies; ambiguous/interrupted code remains flagged |
| Large notebook training cells | Training, plotting and file export are combined | A plotting failure does not prove the model implementation is wrong; original complete cells remain available |

New reference checks deliberately do not repair these scientific branches. No high/negative R2 value was treated as evidence that code should be deleted. Source code calling a pipeline corrected is a historical claim, not independent validation.
