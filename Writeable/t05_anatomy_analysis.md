# T05 — Recorded coding and conditional anatomical-group analysis

Completed 9 November 2026 for the documented exploratory specification. **The old four-outcome multinomial Table 5 is replaced, not reproduced under another label.** Its baseline combined unspecified coding with anatomical outcomes. The supplied NOMREG output also reports a singular Hessian and uncertain fit validity. The new analysis separates two questions, preserves every category descriptively, and explicitly changes the estimands.

## Decision and scientific scope

The [pre-fit specification](../provenance/t05/analysis_specification.md) defines two binary models:

| Panel | Population | Event=1 | Reference outcome=0 |
|---|---|---|---|
| A: recorded coding detail | All 10,972 C71 discharges | C710–C718: non-C719 coding, n=6,304 | C719: unspecified, n=4,668 |
| B: conditional anatomical group | 6,192 discharges assigned to either operational group | C715–C717: infratentorial/midline, n=1,523 | C710–C714: supratentorial, n=4,669 |

Panel A includes C718 but does not assert that overlapping-category records identify a single site. The non-C719 contrast is not validated diagnostic accuracy, coding correctness or a biological location outcome. Even C710 is broad cerebrum coding. Panel B excludes 112 C718 records and 4,668 C719 records by definition; it does not impute their location or correct for nonrandom selection into recorded-site groups.

The combined C715–C717 group is operational: C715 denotes cerebral ventricles and is not universally infratentorial. A sensitivity excludes C715 and compares only C716/C717 with C710–C714. C718 is retained as its recorded category; its ICD inclusion notes also encompass corpus callosum. No algorithm assigns all C718 observations to one compartment. Code meanings are supported by [PAHO's ICD-10 tabular classification](https://ais.paho.org/classifications/Chapters/CAP02.html), section C71. The two-model structure and reference choices are **study decisions**, not a guideline requirement.

These models describe admissions with recorded codes. They do not estimate population cancer incidence, a patient's probability of tumour location, clinical diagnostic precision or a causal sector/ethnicity effect. They cannot be multiplied as if they formed a complete selection-correction model: Panel A includes overlaps, whereas Panel B excludes them.

## Why the previous conventional multinomial model is not retained

The supplied SPV member `00000000072_lightWarningData.bin` says that the Hessian contains unexpected singularities and the validity of the NOMREG fit is uncertain. Exact text, archive/member hashes and interpretation are preserved in [legacy_nomreg_evidence.json](../provenance/t05/legacy_nomreg_evidence.json). This saved warning is distinct from the rebuilt-data checks.

In the reconstructed cohort, C718/overlapping observations are absent in four nonreference source ethnicity levels:

| Source ethnicity code | Recorded category | C718 records | Other outcome records |
|---|---|---:|---:|
| 1 | Indigenous | 0 | 89 |
| 3 | Negro/a | 0 | 14 |
| 4 | Mulato/a | 0 | 22 |
| 5 | Montubio | 0 | 32 |

For each such dummy level, decreasing only its coefficient in the overlapping-outcome logit increases the probability of the observed alternative outcome for every affected observation. It leaves other observations unchanged. The likelihood keeps increasing as that coefficient tends to minus infinity. This is a constructive no-finite-MLE direction in the full four-outcome model including those ethnicity dummies; it is stronger evidence than simply seeing an empty cell somewhere in a table.

The certificates, reference predictor (Mestizo) and reference outcome (unspecified) are exported in `four_outcome_separation_certificates.csv`. A test demonstrates monotonically increasing multinomial likelihood along such a direction. No conventional finite OR, confidence interval or p-value is manufactured for these contrasts. No failed four-outcome solver output is presented as repaired. A simpler four-category model could answer a different descriptive mixed-outcome question, but would still mix code detail with anatomy; it is not the chosen Table 5 estimand.

Binary Firth regression was not applied to an unchanged multinomial model. Penalization might regularize that model but would not resolve the interpretation problem. The supported binary replacements have finite ordinary maximum-likelihood solutions.

## Predictors and references

Both primary models use age group, sex, public/private sector and categorical discharge year. References are **age 18–44, male, private sector and 2015**. There are 16 parameters including the intercept. No automated significance selection or interactions were used.

The adult age reference was chosen to make pediatric/adult comparisons explicit before fitting. The original Table 5 instead compared pediatric ages with 80+; T04 uses pediatric ages as its mortality reference. These are different contrasts and are labelled accordingly. Re-expressing the new Panel B fit as pediatric versus 80+ gives aOR 2.027 (95% interval 1.341–3.063), but that still compares infratentorial/midline with supratentorial coding, not infratentorial with unspecified coding as in the old aRRR. Exact covariance-based re-expressions for both new panels are in `reference_contrasts.csv`.

Ethnicity is omitted from the smaller primary adjustment set because the fine source categories have little support for uniform site comparisons (for example, only five single-group records for code 2 and four for code 3). All categories remain in the descriptive evidence. Full-cohort extended sensitivity models add all nine source codes, using Mestizo code 6 as reference and explicit unknown code 9. No ethnic category is pooled to obtain significance or dropped based on its fitted estimate. The main estimates are not claimed to control all potential confounding.

Final LOS and death are not predictors. LOS occurs during care and its final duration is not an explanation measured before anatomical disease location. Rural/urban residence is used only in restricted-year sensitivities with verified labels; the 2015–2017 interpretation remains provisional.

## Rebuilt Table 5 and main results

[Generated Table 5](../outputs/tables/table5_rebuilt.md) and [its CSV](../outputs/tables/table5_rebuilt.csv) contain every primary contrast. The title and footnotes identify the outcomes, populations, covariates, reference categories, omitted categories and interval assumptions. Effects are **adjusted odds ratios (aORs), not aRRRs**.

| Contrast | Panel A: non-C719 vs C719 aOR (95% Wald interval) | Panel B: infratentorial/midline vs supratentorial aOR (95% Wald interval) |
|---|---:|---:|
| Ages 0–17 vs 18–44 | 1.897 (1.705–2.112) | 1.141 (0.985–1.320) |
| Ages 45–64 vs 18–44 | 0.863 (0.777–0.958) | 0.446 (0.372–0.535) |
| Ages 65–79 vs 18–44 | 0.993 (0.877–1.125) | 0.328 (0.260–0.415) |
| Ages 80+ vs 18–44 | 0.935 (0.736–1.190) | 0.563 (0.371–0.853) |
| Female vs male | 1.008 (0.932–1.090) | 0.991 (0.878–1.119) |
| Public vs private | 1.745 (1.607–1.895) | 0.451 (0.399–0.510) |
| Year 2024 vs 2015 | 1.890 (1.582–2.259) | 1.211 (0.897–1.634) |

The two pediatric results must not be conflated. Pediatric records have greater adjusted odds of a non-C719 code, but the all-year conditional anatomical comparison with ages 18–44 has an interval including one. It does not support a uniform statistically clear pediatric-versus-young-adult anatomical association under this primary specification. Nor does an interval including one prove identical distributions. Older adult groups have lower conditional infratentorial/midline odds than the 18–44 reference.

Public-sector records have greater non-C719 coding odds and lower conditional infratentorial/midline-versus-supratentorial odds. These can reflect case mix, referral, documentation practices and record selection. They do not establish diagnostic quality, sector performance, inequitable access or causal mechanisms.

The higher 2024-versus-2015 non-C719 odds are a recorded code-detail association. They do not validate improved accuracy or disappearance of unspecified coding. There are still 379 C719 records in 2024.

## Descriptive categories retained

| Recorded group | All admissions | Percent of all 10,972 |
|---|---:|---:|
| Supratentorial | 4,669 | 42.554% |
| Infratentorial/midline | 1,523 | 13.881% |
| C718/overlapping category | 112 | 1.021% |
| C719/unspecified | 4,668 | 42.545% |

Descriptive proportions with Wilson intervals are in `anatomy_descriptive.csv`; predictor-by-outcome counts, including zero cells, are in `anatomy_predictor_cells.csv`. Rural/urban counts across all years are explicitly marked as partly provisional and are not used as verified primary covariates. No hypothesis-test p-values are attached to the descriptive category totals.

## Sensitivity analyses and substantive uncertainty

Fifteen fits were specified and completed: seven for coding detail and eight for the conditional-site question. Every fit is finite, full rank and converged without captured warnings or LP separation. This establishes numerical estimability under these designs, not scientific validity of every interpretation.

| Model | Coding n/events | Site n/events | Site pediatric vs 18–44 aOR (95% interval) |
|---|---:|---:|---:|
| Primary | 10,972 / 6,304 | 6,192 / 1,523 | 1.141 (0.985–1.320) |
| Resident only | 10,969 / 6,302 | 6,190 / 1,523 | 1.141 (0.985–1.320) |
| Exclude 2017 and 2023 | 8,656 / 5,029 | 4,928 / 1,190 | 1.239 (1.052–1.460) |
| Verified-label years 2018–2024, core | 7,621 / 4,644 | 4,555 / 1,169 | 1.698 (1.429–2.017) |
| Same years, add residence | 7,621 / 4,644 | 4,555 / 1,169 | 1.681 (1.414–1.998) |
| Record-level HC0 covariance | 10,972 / 6,304 | 6,192 / 1,523 | 1.141 (0.984–1.322) |
| Add source ethnicity | 10,972 / 6,304 | 6,192 / 1,523 | 1.118 (0.965–1.295) |
| Exclude ventricular C715 | Not applicable | 6,016 / 1,347 | 1.165 (1.000481–1.357) |

The pediatric anatomical association changes **materially with the observation period**. The later-year result cannot be substituted for the all-year primary result because it is more statistically significant. No formal age-by-year interaction or heterogeneity test has been performed. The primary model's common adjusted contrast should not be described as a stable effect in every year. Verified-year models use year 2018 as reference; sensitivity comparisons do not treat their year contrasts as if the reference were 2015.

Excluding C715 yields a lower interval endpoint only slightly above one (1.000481); this is borderline numerical evidence in an exploratory sensitivity, not a robust confirmation based on rounding to 1.000. It also changes the outcome group to cerebellum/brainstem codes and the analysis population. No interpretation should depend on whether a rounded interval appears to touch one.

In verified years, rural residence has aOR 0.793 (0.694–0.905) for non-C719 coding and aOR 1.327 (1.090–1.616) for the conditional-site contrast. These describe different recorded outcomes in selected years; they do not validate early labels or demonstrate geographic disease risk.

The eight sparse extended-ethnicity contrasts have supplementary profile-likelihood intervals; the main tables retain consistently labelled Wald intervals. Some are extremely broad: in the site model, code 2 has aOR 3.209 with profile interval 0.411–20.085, based on two events and three non-events. Such estimates are unsuitable for confident clinical/ethnicity conclusions. Profile intervals use the asymptotic likelihood-ratio cutoff chi-square(1)=3.841 and do not guarantee reliable small-sample coverage. Individual p-values are exploratory without multiplicity adjustment.

HC0 changes record-level covariance, not coefficients; it is not patient/facility clustering correction. Repeated admissions, unknown facility identities, nonrandom site documentation, missing histology/grade/treatment and unmeasured severity remain limitations. Restriction to specified operational groups is not a missing-at-random assumption justified by these data and is not an imputation or selection-bias correction.

## Validation, evidence and reproducibility

Primary coding: 16/16 design rank, five iterations, maximum absolute score 3.44×10⁻¹² and information condition number approximately 209. Primary site: 16/16 rank, five iterations, maximum absolute score 2.20×10⁻¹² and condition number approximately 272. All 15 fits have positive observed-information eigenvalues and no separation direction from the binary LP checks.

The four-outcome model is explicitly marked **not estimated**, with constructive certificates. The binary replacements have no ambiguous “–” cells representing invalid estimates. Their omitted outcome categories and smaller primary adjustment set are explained in the table footnotes. No penalty or category pooling was introduced merely to obtain a publishable p-value.

With the audited cohort present and the local environment active on either operating system:

```sh
python -m pip install -r requirements.txt
python -X utf8 scripts/fit_anatomy.py
python -X utf8 -m unittest discover -s tests -v
```

No new dependencies were required. T05 modelling has been executed on macOS; the new stage has not yet been executed on Windows. Existing path/UTF-8 conventions are retained. The optional original SPV is read only to export the saved NOMREG warning; when absent, historical evidence is preserved, and fitting uses the audited CSV alone. The supplied original SAV/SPV/XLSX package remains complete; no additional original SAV or cleaning script is required.

Tracked evidence under `provenance/t05/`:

- `analysis_specification.md`: decisions recorded before adjusted fitting.
- `model_flow.csv`: both eligibility definitions, exclusions and event denominators.
- `anatomy_predictor_cells.csv`, `anatomy_descriptive.csv`: category counts and sparse/zero-cell evidence.
- `four_outcome_separation_certificates.csv`, `legacy_nomreg_evidence.json`: reasons for not reporting the original conventional model.
- `all_model_coefficients.csv`, `crude_odds_ratios.csv`, primary covariance matrices and `model_diagnostics.json`: estimates, references and fit checks.
- `sensitivity_comparison.csv`, `reference_contrasts.csv`, `sparse_profile_intervals.csv`: sensitivity and uncertainty evidence.
- `run_metadata.json`, environment and validation records: fingerprints and implementation versions.

**All 50 project tests pass**, including 12 T05 tests of outcome coding, conditional selection, adult references, an independent 2×2 logistic control, constructive multinomial likelihood behavior, all-model diagnostics, covariance invariance and sparse profile bounds. These tests establish the declared computational controls, not clinical validation.

**T05's technical decision and replacement analysis are complete.** These are newly defined exploratory estimands, not recovered versions of the original aRRRs. Coauthors should review the question change and temporal sensitivity before adopting Table 5 in the manuscript. Follow-up, 9 November 2026: T06 descriptive tables and model legends are complete; see [the T06 report](t06_descriptive_tables.md). T07 manuscript language and later figures still require the planned revisions.

## Bibliographic support and limits

- [PAHO/WHO ICD-10, Chapter II, C71.5–C71.9](https://ais.paho.org/classifications/Chapters/CAP02.html): source code meanings. It does not mandate either new model or validate individual diagnoses.
- [RECORD statement](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1001885): reporting of record selection, codes and data preparation. It does not establish missing-at-random site availability or validate the models.
- [statsmodels GLM documentation, version 0.15.0](https://www.statsmodels.org/stable/glm.html): binomial logit implementation; numerical fit checks are local evidence.
- [statsmodels MNLogit documentation](https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.MNLogit.html) and [pitfalls](https://www.statsmodels.org/stable/pitfalls.html): model structure and finite-MLE/convergence concerns. The new zero-cell certificates are a mathematical argument for this specific design, not proof supplied by a generic software warning.
- [Wilks, 1938](https://doi.org/10.1214/aoms/1177732360): asymptotic likelihood-ratio framework for the supplementary profile intervals; no claim of exact small-sample coverage.

See the updated decision register, rationale and BibTeX library for how source-defined meanings, study choices and local verification are kept distinct.
