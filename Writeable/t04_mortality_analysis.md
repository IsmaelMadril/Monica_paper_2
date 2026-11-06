# T04 — Mortality model repair and validation

Completed 6 November 2026 for the documented reconstructed-cohort association model. The primary analysis includes **10,972 admissions, 963 in-hospital deaths and 10,009 live discharges**. The supplied SAV/SPV/XLSX files remain the complete original analysis package; no additional original SAV is required. The manuscript PDF and its historical Table 4 have not been edited.

## Main finding: the original modelled event was survival

The supplied SPV's dependent-variable encoding table was decoded directly:

| Original SPSS label | Internal value |
|---|---:|
| `Fallecid` (truncated death label) | 0 |
| `Vivo` (live discharge) | 1 |

SPSS models the internally coded event 1. Thus the original mortality-labelled model estimated **odds of live discharge**, not death. This is now decoded evidence rather than an inference from counterintuitive age/stay results. The table labels remain distinguishable after SPSS's eight-byte truncation; the truncation warning alone is not evidence that the two outcomes were conflated.

The same archive's model summary says the iteration limit was reached and a final solution could not be found. The original commands specify an iteration cap of 20. Simply reciprocating the printed aORs would leave the failed fit, all-death legacy 2023 subset, anatomical miscoding and other preparation differences unresolved.

Evidence, source/member hashes and exported warning text are in [legacy_model_evidence.md](../provenance/t04/legacy_model_evidence.md) and `legacy_encoding.json`. A restricted decoder follows the documented SPV numeric-value, category-leaf and cell structures and fails on unsupported layouts. It is not a general SPSS viewer or a full export of every table. The saved warning text contains an unresolved footnote argument placeholder; it is preserved as evidence rather than presented as a fully rendered viewer export.

## Primary model and coding decisions

The [specification](../provenance/t04/analysis_specification.md) was written before fitting the rebuilt models. Outcome coding is explicitly **death=1** for source discharge codes 2/3 and **live discharge=0** for source code 1. Cross-tabulation confirms 963 and 10,009, respectively. All outcomes and required predictor fields are recognized; no admissions are excluded from the primary analysis.

The unit is an admission/discharge record, not a unique patient. The purpose is adjusted association with death during that admission. It is neither causal risk-factor estimation nor a validated prediction tool.

| Predictor | Reference | Treatment |
|---|---|---|
| Age group | 0–17 years | 0–17, 18–44, 45–64, 65–79, 80+ |
| Sex | Male (`Hombre`) | Source categories preserved |
| Ethnicity | Mestizo, source code 6 | All source codes retained as distinct categories; code 9 is explicit unknown |
| Health sector | Private | Public versus private; source private nonprofit/for-profit groups combined as in the binary specification |
| Anatomy | Supratentorial | Corrected four-category C71 grouping |
| Discharge year | 2015 | Ten categorical years; 2017 and 2023 included |

No significance-based selection or interaction search was performed. The model has 27 parameters including the intercept. There are approximately 35.7 deaths per parameter overall, but this aggregate ratio does not resolve sparse individual ethnicity categories.

**Length of stay is excluded from the primary model.** Its final duration is partly determined by discharge/death timing, so it is not an admission-time exposure. **Rural/urban residence is excluded from the all-year primary model** because 2015–2017 labels remain provisional. Those labels are used neither as verified values nor as a reason to discard the early years. Source ethnicity code 9 remains unknown; it is not merged with Other or treated as known ethnicity through imputation.

Anatomical category and calendar year are recorded at discharge, and the dataset does not establish admission-time ascertainment for all covariates. This is therefore a descriptive adjustment model, not a model in which every covariate is asserted to precede the outcome. Histology, tumour grade, treatment, comorbidity, palliative intent and referral severity are not adjusted for.

## Rebuilt Table 4 and interpretation

[Generated Table 4](../outputs/tables/table4_rebuilt.md) and [its CSV](../outputs/tables/table4_rebuilt.csv) contain every adjusted contrast, reference, sample count, interval, p-value and sparse-category flag. Primary results include:

| Contrast | Adjusted death OR | 95% Wald interval |
|---|---:|---:|
| Age 18–44 vs 0–17 | 1.080 | 0.880–1.324 |
| Age 45–64 vs 0–17 | 1.593 | 1.312–1.934 |
| Age 65–79 vs 0–17 | 2.153 | 1.742–2.661 |
| Age 80+ vs 0–17 | 2.631 | 1.864–3.715 |
| Female vs male | 0.972 | 0.850–1.111 |
| Public vs private sector | 1.201 | 1.035–1.394 |
| Infratentorial/midline vs supratentorial | 1.281 | 1.035–1.586 |
| Unspecified vs supratentorial | 1.246 | 1.074–1.445 |
| Year 2023 vs 2015 | 1.034 | 0.768–1.391 |

Older admission-age groups have higher adjusted death odds than the pediatric reference in this reconstructed cohort. The earlier claim that advanced age was protective is not supported. The crude death OR for 80+ versus 0–17 is 2.675 (95% interval 1.905–3.756), consistent in direction with the adjusted association.

The 2023 coefficient is now finite and ordinary. There is no reconstructed all-death year. Its interval includes one; that does not prove equality with 2015 or validate a claim of temporal stability.

Public-sector and anatomical associations are conditional on the recorded covariates. They do not establish hospital quality, access barriers, biological effects of unspecified coding or policy effects. Severity and referral differences can confound these associations. Odds ratios are not risk ratios or patient-level survival probabilities.

The new age aOR is not expected to equal the reciprocal of the old aOR: the cohort, age-unit treatment, anatomy coding, ethnicity categories, references and covariates also changed. The old failed fit cannot be used as a valid comparator estimator.

## Convergence, separation and sparse estimates

Every specified fit converged in six IRLS iterations, with no captured fitting warning. For the primary model:

- Design rank: **27/27**.
- Largest absolute score component: **1.42 × 10⁻¹¹**.
- Minimum observed-information eigenvalue: **1.655**; information condition number: approximately **1,181**.
- Finite coefficients, standard errors and confidence limits; maximum leverage approximately **0.126**.
- Linear-programming separation check finds no complete or quasi-separating direction. The check is performed for each model; synthetic complete/quasi-separated controls are detected in tests.

These findings support a finite unpenalized maximum-likelihood solution. Firth/bias-reduced fitting was therefore not automatically applied. If future inputs produce separation or fit failure, the script stops rather than emitting an apparently valid primary table; any alternative estimator must then be specified and checked.

Six nonreference categories have fewer than ten deaths: ethnicity codes 2, 3, 4, 5, 7 and overlapping anatomy. They are flagged and retained without significance-driven merging. Their Wald intervals are imprecise. Supplementary 95% **profile-likelihood** intervals were calculated by fixing the focal coefficient, refitting nuisance coefficients, and finding the likelihood-ratio cutoff chi-square(1)=3.841. For example:

| Sparse level | Admissions/deaths | aOR | 95% profile interval |
|---|---:|---:|---:|
| Afro-Ecuadorian/Afrodescendant, code 2 | 13/2 | 1.666 | 0.255–6.324 |
| Negro/a, code 3 | 14/2 | 1.809 | 0.277–6.845 |
| Mulato/a, code 4 | 22/5 | 3.560 | 1.151–9.197 |
| Overlapping anatomy | 112/7 | 0.738 | 0.309–1.493 |

See `provenance/t04/sparse_profile_intervals.csv` for all six. Profile intervals are asymptotic likelihood-based intervals, not exact intervals and not a correction for selection bias or dependence. The primary table consistently reports Wald intervals and Wald p-values; profile intervals are supplementary. Ethnicity comparisons are exploratory, with no multiplicity adjustment; isolated small-cell p-values should not be promoted as confirmed clinical or biological findings.

## Sensitivity analyses

All seven sensitivity fits also converged without separation or warnings:

| Fit | Admissions | Deaths | Age 80+ aOR | Public-sector aOR |
|---|---:|---:|---:|---:|
| Primary: all admissions, no final LOS | 10,972 | 963 | 2.631 | 1.201 |
| Resident only | 10,969 | 963 | 2.630 | 1.202 |
| Exclude 2017 and 2023 | 8,656 | 749 | 1.965 | 1.216 |
| Verified residence years 2018–2024, core model | 7,621 | 658 | 1.890 | 1.507 |
| Same verified years, add residence | 7,621 | 658 | 1.899 | 1.490 |
| Add final LOS, descriptive only | 10,972 | 963 | 2.930 | 1.066 |
| Known ethnicity only | 9,682 | 864 | 2.555 | 1.215 |
| Same primary coefficients, HC0 covariance | 10,972 | 963 | 2.631 | 1.201 |

- Restricting to residents changes little. Unlike T03 population rates, the primary admission-level outcome model can include foreign residents; the populations are explicitly distinguished.
- Omitting 2017/2023 is a stress test motivated by the legacy errors, not an assertion that those official years are incomplete. Age estimates shift materially even though their direction remains positive. Neither this stress test nor the 2018–2024 subset replaces the primary all-year model.
- The verified-year core and residence models use identical rows. Rural residence has aOR **1.119** (95% interval **0.900–1.392**) after adjustment in those years. This is a restricted-period result, not a validation of the provisional 2015–2017 labels or proof of no rural disparity.
- Verified-year models use **2018** as the year reference; other primary references stay the same. The comparison CSV does not calculate coefficient changes for year contrasts with different references. Comparing models on different years is descriptive, not a formal heterogeneity test.
- Adding final LOS gives an aOR **3.574** (95% interval **2.879–4.436**) for **31+ versus 1–3 days**. This does not establish harm from longer hospitalization, just as the old result did not establish protection. Final duration is outcome-dependent. Public-sector aOR also changes from 1.201 to 1.066 after conditioning on LOS; this is not a mediation analysis.
- Known-ethnicity analysis excludes 1,290 records with 99 deaths. It is a missingness sensitivity, not proof that complete-case analysis is unbiased.
- HC0 changes covariance/intervals, not point estimates; public-sector interval becomes **1.029–1.403**. HC0 at the record level cannot adjust repeated admissions by the same person or correlated outcomes within an unidentified facility.

**Patient/facility clustering remains unresolved.** Available source-row keys identify records, not persons. Province, institution type and institutional ownership descriptors are not validated unique facility identifiers. No substitute facility ID or patient linkage has been invented. Reported uncertainty assumes independent admission records and may be too narrow when clustering exists. This is a material limitation despite numerical convergence.

## Reproduction and deliverables

After generating `data/processed/admissions_c71_audited.csv`, use the local environment on macOS or Windows PowerShell:

```sh
python -m pip install -r requirements.txt
python -X utf8 scripts/fit_mortality.py
python -X utf8 scripts/profile_sparse_mortality.py
python -X utf8 -m unittest discover -s tests -v
```

To regenerate the legacy encoding evidence when the supplied SPV is restored:

```sh
python -X utf8 scripts/inspect_legacy_mortality.py
```

The rebuilt model does not require the legacy SPV or SAV at runtime. When the SPV is unavailable, the inspection script preserves existing historical evidence and reports that it was not reread locally. It does not infer an event from an absent file. The restricted reader has been checked against the supplied SPV and a malformed numeric-cell control.

The T04 CSV uses LF line endings while the recorded T03 input hash corresponds to
CRLF bytes. Converting only those line endings reproduces the exact T03 hash,
confirming that this difference does not change the data. Both variants and the
match are recorded in `provenance/t04/cross_stage_input_check.json`; the historical
T03 metadata and original inputs were not rewritten.

`provenance/t04/` includes the prespecified analysis choices, source encoding, model flow, marginal event counts, crude ORs, full adjusted coefficients, covariance matrix, diagnostics, sensitivity comparisons, supplementary profile intervals, software versions and input hashes. Main generated outputs are `outputs/tables/table4_rebuilt.md` and `.csv`. No individual model predictions are published to the tracked evidence files.

**All 38 project tests pass** on this workstation, including independent 2×2 logistic controls, outcome reversal, complete/quasi separation, profile bounds, reference levels and integration checks. Numerical modelling was run on macOS; the new T04 stage has not yet been executed on Windows. The existing cross-platform path and UTF-8 conventions are preserved.

**T04's technical analysis is complete for this specification.** Covariate choices, residual confounding, sparse comparisons and uncertainty assumptions still need coauthor review before submission. T02's residence-label question remains open; T05's multinomial model repair is next. The original article will need updated interpretation and tables during the planned manuscript revision tasks.

## Primary documentation used

- [IBM SPSS Regression 25](https://www.ibm.com/docs/SSLVMB_25.0.0/pdf/en/IBM_SPSS_Regression.pdf): event coding and reference-category interpretation.
- [GNU PSPP developer format documentation](https://www.gnu.org/software/pspp/pspp-dev/html_node/index.html): SPV light-member category, value and cell structures used by the restricted encoding decoder.
- [statsmodels generalized linear models](https://www.statsmodels.org/stable/glm.html): binomial logistic fitting and result methods. Installed version is recorded as 0.15.0.
- [statsmodels covariance documentation/source](https://github.com/statsmodels/statsmodels/blob/main/statsmodels/base/covtype.py): HC0 covariance options; recorded package versions fix the implementation used here.
