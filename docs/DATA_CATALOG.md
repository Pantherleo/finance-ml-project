# Data catalogue

Observed CSV schemas and row counts are in [csv_inventory.json](csv_inventory.json). Full checksums are in the original-file manifest. The new parser diagnostics describe accepted Date/Close/High/Low observations only; they are not a complete source-price validation.

| Asset | Input rows | Accepted | First accepted date | Last accepted date | Max calendar gap (days) |
| --- | ---: | ---: | --- | --- | ---: |
| gold | 4745 | 4744 | 2007-01-02 | 2025-11-09 | 5 |
| crude_oil | 4746 | 4746 | 2007-01-02 | 2025-11-09 | 5 |
| forex_usd_inr | 4889 | 4889 | 2007-01-01 | 2025-11-10 | 26 |
| nifty50 | 4462 | 4462 | 2007-09-17 | 2025-11-25 | 6 |

The canonical four tables use day-first date strings. Alternative Apple/Alphabet/NIFTY exports contain provider-style metadata rows and a Price header. They are preserved in full and need deliberate schema normalization before use.

The acquisition notebook requests GC=F, CL=F, USDINR=X, GOOG and AAPL through yfinance. This records source-code intent; it does not prove exact file lineage, adjustment defaults or redistribution rights. NIFTY acquisition appears in other notebooks. Download timestamps and complete settings remain unverified.

The parser reports missing/nonnumeric/nonfinite prices and High<Low exclusions, retains/report Close values outside the source high/low range, and does not fill gaps. A calendar gap is not automatically a missing trading day. Actual coverage above supersedes names ending in present. See [data_quality.json](data_quality.json) for details.
