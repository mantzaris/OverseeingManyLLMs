# Transaction provenance and analysis contract

The primary source is **Chen, D. (2015), Online Retail [Dataset], UCI Machine Learning Repository**, DOI [10.24432/C5BW33](https://doi.org/10.24432/C5BW33). The [official dataset page](https://archive.ics.uci.edu/dataset/352/online%2Bretail) identifies a UK-based non-store retailer, recorded transactions and the cancellation prefix. Its current license is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). We downloaded the official ZIP from https://archive.ics.uci.edu/static/public/352/online%2Bretail.zip. Retrieval metadata and hashes are in `artifacts/coordination_injections/downloads.json`; full audit and transformations are in `data_audit.json`.

ZIP SHA256: `f5385cbb54bbebf7196389109c6b0621faab0c304e3702548165e71c84aede8b` (23,715,478 bytes). Raw XLSX and SQLite remain outside Git in `/tmp/coordination-sources/`; the acquisition command reconstructs them. Derived aggregates and prompts are retained with attribution. No customer IDs or descriptions are supplied to the model.

## Audit of actual records

All **541,909 rows** are preserved. Dates range from **2010-12-01 08:26** through **2011-12-09 12:50**. December 2011 is a partial month and excluded from project blocks; the recording does not establish completeness of every earlier operating day. There are 25,900 invoice identifiers, and 43 identifiers have multiple date/customer/country tuples. Invoice IDs are not assumed to identify a single consistent transaction header.

| Condition | Rows or count | Treatment |
|---|---:|---|
| Duplicate rows beyond the first identical record | 5,268 | Retained, because deduplication would be a reporting convention |
| Invoice starts with C | 9,288 | Explicit cancellation flag |
| Negative quantity | 10,624 | Retained; inclusion is contract-specific |
| Negative quantity without C | 1,336 | Not silently reclassified as ordinary sales |
| Zero quantity | 0 | Audited |
| Zero unit price | 2,515 | Retained in raw table; excluded by both declared analysis rules |
| Negative unit price | 2 | Retained in raw table; excluded by both rules |
| Missing customer ID | 135,080 | Included unless a contract requires known IDs |
| Missing description | 1,454 | Retained; grouping uses stock code |
| Missing invoice/stock code/country | 0 | Audited |
| Country values | 38 | Exact source values, no harmonization |

Quantities range from -80,995 to 80,995. Unit prices range from -11,062.06 to 38,970 GBP. Prices have up to three decimal places. We convert decimal strings exactly to integer millionths of GBP, then multiply by quantity. This avoids binary floating-point aggregation differences. Country values include `Unspecified`, `European Community`, `EIRE`, `RSA` and `Channel Islands`; these are source categories, not a cleaned geopolitical taxonomy. Stock codes include non-merchandise entries such as postage and charges.

## Reporting definitions

Source timestamps carry no timezone in the file; windows use recorded calendar dates without an inferred UTC conversion. Stage authorization clocks are separately recorded in UTC.

Every query keeps source duplicates, uses an inclusive start and exclusive end, groups by stock code, orders aggregate descending then stock code ascending, and returns at most five rows. `ALL` is an application sentinel for no country predicate. `customer=all` includes missing IDs; `known` requires a nonmissing ID. The two inclusion rules are authored:

- **Positive non-cancellation lines**: quantity > 0, unit price > 0, and no C prefix.
- **Signed positive-price lines**: unit price > 0, with both signs of quantity and either cancellation flag.

The **recorded quantity aggregate** is sum(quantity) over included rows. **Recorded line value** is sum(quantity * unit_price), reported internally in micro-GBP and displayed with explicit GBP conversion. Neither is profit. The cancellation marker alone cannot establish a business definition of recognized revenue, refunds or net sales. Costs and actual accounting recognition are unavailable.

## Source and constructed layers

| Layer | What it contains |
|---|---|
| Real recorded observations | Original invoice lines, dates, quantities, prices and source categories |
| Constructed application | Four roles, dependencies, briefs, reporting definitions, scopes, user changes, project identities and disturbances |
| Generated evidence | GPU-produced tool parameters, chart specifications, prose, notifications and repair responses |
| Deterministic application/evaluation | Query compilation, arithmetic, public guards, independent Python aggregates, routing and paired analysis |
| Simulated interaction | One authorized change event per project; no participant responses, subjective workload or monetary intervention costs |

Development uses December 2010 and January 2011. Evaluation uses all declared project templates on February through September 2011 blocks. Two constructed projects within a month and generation replicates remain dependent. There is one retailer, eight nonoverlapping evaluation month blocks, not eight independent retailers. Adjacent periods may still be related. The source was audited before generation, but no evaluation aggregates or model outcomes select cases. Repeated pre-change requests are generated separately when their declared IDs/seeds differ; policy continuations start from the same saved checkpoint within a project and replicate.
