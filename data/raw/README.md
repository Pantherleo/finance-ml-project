# Local source tables

Seven original root CSVs are copied here byte-for-byte for a stable data layout. They remain excluded from Git pending provenance/redistribution review. Root originals are untouched for historical path compatibility.

The independent baseline uses the canonical Date/Close/High/Low columns of gold, crude oil, USD/INR and NIFTY 50 files. Apple, Alphabet and the alternate nifty50.csv have multirow Price/Ticker/Date headers and are not silently substituted into that parser.

No verified frozen public download URL or license was supplied. The acquisition notebook records requested ticker names, but exact retrieval settings and dates remain to be documented. Use hashes in the original-file manifest and the baseline metrics to identify approved local inputs. See `docs/DATA_CATALOG.md`.
