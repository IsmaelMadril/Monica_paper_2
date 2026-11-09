# T06 — Descriptive tables and statistical legends

Completed 9 November 2026 for the reconstructed-cohort specification. This task
regenerates Tables 1–2 and standardizes presentation of the executed Tables 4–5.
It does not overwrite the reviewed manuscript PDF. Insertion into the editable
manuscript and matching Results/Methods wording remain T07 work. The T02
2015–2017 residence-label question remains open; T06 handles it by restricting
only residence comparisons to verified years.

## Generated tables and denominators

Readable, tracked review copies are available even before restoring ignored inputs:

- [Table 1: discharge outcome](../provenance/t06/table1_rebuilt.md).
- [Table 2: recorded anatomical group](../provenance/t06/table2_rebuilt.md).
- [Table 4: adjusted death associations](../provenance/t06/table4_rebuilt.md).
- [Table 5: coding and conditional anatomy](../provenance/t06/table5_rebuilt.md).

The generator also writes Markdown and numeric CSV tables to `outputs/tables/`.
The source is `data/processed/admissions_c71_audited.csv`: **10,972 admissions,
963 deaths and 10,009 live discharges**. These are reconstructed INEC records,
not the supplied original 8,249-record cohort. Source-row identifiers are unique;
this does not establish unique patients.

Table 1 reports all, live and dead counts, with each column's explicit denominator
within its characteristic block. A separate fatality column is **100 × category
deaths/category admissions**. Table 2 reports counts and column percentages for
supratentorial (4,669), infratentorial/midline (1,523), overlapping (112) and
unspecified (4,668) records. Percentages sum to 100 within a column and a
characteristic before rounding, not across repeated characteristic blocks.
C719 is a recorded outcome category, not a missing value to drop.

Age, sex, ethnicity, binary and detailed sector, recorded stay and year are shown
in both tables; Table 1 also includes recorded anatomical group. Binary sector
matches the model adjustment; detailed sector prevents hiding the nonprofit and
for-profit composition of the private category. These are related exploratory
summaries, not independent confirmatory hypotheses. All nine source ethnicity
categories remain distinct, including Other and Unknown/not recorded.

No true null values occur in these displayed characteristics in the current
cohort. **1,290 ethnicity records (11.76%)** have source code 9; these remain
explicitly unknown, rather than being reported as complete ethnicity information.
The code preserves an explicit Missing row if a future valid input contains nulls
and rejects unrecognized non-null categories. Recorded stay groups are 0, 1–3,
4–14, 15–30 and 31+ days; zero is displayed as an empty category in this cohort.
An empty category has fatality n.a., not zero fatality.

Residence is a separate **2018–2024** block: **7,621 records, 658 deaths and 6,963
live discharges**. It excludes all **3,351** early-year records (305 deaths and
3,046 live discharges) from that block only. Urban fatality is 545/6,490=8.40%;
rural fatality is 113/1,131=9.99%. The rural column shares, 17.17% among deaths
and 14.62% among live discharges, have different denominators and do not estimate
rural-versus-urban fatality. No all-decade residence comparison is presented.

## Annual reconciliation and the 2024 repair

Both tables use the same source records and year definitions. The 2024 row is
**1,019 admissions, 932 live discharges and 87 deaths**. Its live-discharge column
percentage is **932/10,009=9.31%**, not the old 9.5% or an arithmetic patch to the
legacy 895 count. Its within-year fatality is **87/1,019=8.54%**. The 2024
anatomical cells are regenerated from the same 1,019 records. The reconstructed
2017 and 2023 totals are retained (1,221 and 1,095); this task does not infer a
historical extraction mechanism or registration failure.

Every cell is exported with its integer numerator, column denominator, category
admission denominator, scope and unrounded percentage in
[table1_cells.csv](../provenance/t06/table1_cells.csv) and
[table2_cells.csv](../provenance/t06/table2_cells.csv). Scope, missingness and
characteristic-level checks are separately exported. All **17 characteristic
blocks** reconcile to their stated cohorts and outcome margins.

## Exploratory omnibus comparisons

The [specification](../provenance/t06/analysis_specification.md) was recorded
before generating these test results. One unadjusted independence comparison is
reported per characteristic per table. These are associations among admission
records; none is a test of population incidence, a trend test, an effect size or
a clinical importance assessment. No multiplicity adjustment, p-value-based
category merging or significance highlighting is applied.

The implemented conservative dispatch rule is:

- Uncorrected Pearson chi-square when every observed and expected active cell is ≥5.
- Two-sided Fisher exact for sparse 2×2 tables.
- Fixed-margin Monte Carlo Pearson for other sparse tables, using 99,999 Patefield
  draws, deterministic per-comparison seeds and the upper tail of the Pearson
  statistic including ties. This tests departures in either direction; it is not
  a doubled-tail normal test or a Fisher probability-ordering test.

Zero-margin rows/columns are removed from testing only; their descriptive zeros
remain visible. Of 17 current comparisons, **13 use Pearson and four use Monte
Carlo**; none requires the Fisher branch. The source for these implementations
and the conservative cell rule is the [SciPy contingency documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html),
with [fixed-margin random tables](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.random_table.html)
and [two-sided Fisher conventions](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html).
The choice to include exploratory tests remains a study decision.

Monte Carlo p=(exceedances+1)/(99,999+1). The death-by-ethnicity comparison has
1,243 exceedances, p=0.01244, approximate simulation SE=0.000351, and a 95%
Clopper-Pearson interval for the underlying simulated tail probability of
0.01175–0.01314. The age, ethnicity and year comparisons in Table 2 have zero
exceedances and minimum attainable simulation p=0.00001. This is **not** a precise
estimate or a bound on the true tail probability: its simulation interval is
0–0.00003689. More draws are unnecessary for the current descriptive reporting
purpose; no finer significance claim is made.

Exact test inputs/results, active dimensions, statistic, expected-cell checks,
replicates, seeds, exceedances and simulation uncertainty are in
[independence_tests.csv](../provenance/t06/independence_tests.csv). P-values are
stored without presentation rounding; Markdown uses three significant digits,
scientific notation for small values and an explicit label at simulation
resolution. The [Monte Carlo documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.monte_carlo_test.html)
also discusses tail definitions and floating-point ties; our conservative tie
tolerance is declared in the specification and code.

## Model legends and verification

Tables 4–5 now use one shared renderer with English variable/sex labels and
consistent p precision. Their legends give events, reference outcomes, included
covariates, all predictor references, model N/events, model type, covariance and
interval methods, explicit unknown categories/exclusions and dependence limits.
No schizophrenia footnote, duplicated title or significance highlighting remains.
The primary aORs and full-precision intervals/p-values are unchanged from the
executed T04/T05 evidence. T06 checks exact cohort hashes and saved fit diagnostics
before refreshing presentation; original model scripts also use the same renderer.

Validation on macOS: **61 project tests pass, no skips**, including 11 new T06
method/integration checks. Controls independently enumerate a small conditional
2×3 distribution to verify the simulation tail, hand-calculate a Pearson statistic,
check two-sided Fisher routing, distinguish missing from unknown, compare every
exported cell to source counts, verify all margins and confirm unchanged model
CSV values. Software/input/code fingerprints are preserved in `provenance/t06/`.
Windows commands are provided; this new stage has not been executed on Windows.

All tests and intervals assume independent records. Repeated admissions and
unobserved facility dependence remain unresolved, as do diagnostic/coding error,
missing severity and selection into admission. Stay is descriptive and cannot be
interpreted as a baseline exposure. The year/outcome omnibus p does not establish
stable risk. Reporting follows the principles of STROBE items 12, 14 and 16
([explanation](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0040297));
a checklist does not validate these assumptions. See rationale decisions D30–D32.
