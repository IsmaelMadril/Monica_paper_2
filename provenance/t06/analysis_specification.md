# T06 table specification — 9 November 2026

Implement Tables 1–2 from the audited C71 cohort before inspecting new test results.
The admission is the observation; retain all ten years for validated characteristics.
Table 1: total, live and dead counts with explicit column denominators plus within-category
fatality (deaths/category admissions). Table 2: four operational anatomy groups,
counts with column percentages and explicit column denominators. Include age, sex,
all nine ethnicity codes, binary sector (matching models), detailed sector, stay,
year and residence area. Anatomy itself appears only in Table 1.

Residence area is a separately labelled 2018–2024 block using verified mappings;
exclude 2015–2017 from that block only. Show excluded records and their outcomes.
Do not resolve provisional labels by publishing them as accepted all-year labels.
Null categories become explicit Missing; source ethnicity 9 remains Unknown/not recorded.
Unused predefined levels are displayed as zero and excluded from a test only when
an entire row or column margin is zero; report active dimensions.

One exploratory omnibus independence comparison per characteristic per table.
Use uncorrected Pearson chi-square only when all observed and expected cells are
at least 5 (a conservative implementation rule following SciPy's documented guideline).
For sparse 2x2 tables use two-sided Fisher exact. For other sparse tables use
conditional fixed-margin Monte Carlo Pearson statistics, 99,999 replicates, deterministic
per-comparison seeds starting at 20261109. Tail includes ties with numerical tolerance;
p=(exceedances+1)/(B+1). Export B, seed, exceedances, simulation standard error and
a 95% Clopper-Pearson interval for the underlying simulated tail probability (not a
confidence interval for an association). No multiplicity adjustment or significance
highlighting; no trend, causality or patient/facility-independence validation claim.

Preserve full numeric p-values in CSV; display three significant digits and scientific
notation for values below .001, never round a small p to zero or substitute exactly .001.
If no exceedances, display the minimum attainable simulation p and zero exceedance count, not an upper bound on the true p.
Tables 4–5 retain the executed T04/T05 models and self-contained legends, with
English variable/sex labels and the same p formatting. Regenerate their presentation
from saved coefficients only after checking cohort hashes and diagnostics; do not refit
or change estimates during T06. Existing model scripts use the same renderer thereafter.

Primary sources: STROBE explanation items 12,14,16 (R09); SciPy contingency and
random-table documentation (new R17). These support reporting/procedures, not
unobserved independence, absence of bias or the choice to perform exploratory tests.
