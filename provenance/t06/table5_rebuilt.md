# Rebuilt Table 5 — recorded coding and conditional anatomical group

Two exploratory maximum-likelihood binary logistic models replace the former multinomial model. Both include age group, sex, binary sector and categorical discharge year (16 parameters including intercept each). Results are adjusted odds ratios (aORs), not aRRRs.

## A. Non-C719 versus C719 coding

event=1: C710–C718; reference=0: C719. N=10,972; events=6,304; non-events=4,668. No records excluded; C718 is included without asserting a single site.

| Predictor | Category vs reference | aOR | 95% Wald CI | Wald p |
|---|---|---:|---|---:|
| Age (years) | 0-17 vs 18-44 | 1.897 | 1.705–2.112 | 1.12e-31 |
| Age (years) | 45-64 vs 18-44 | 0.863 | 0.777–0.958 | 0.00561 |
| Age (years) | 65-79 vs 18-44 | 0.993 | 0.877–1.125 | 0.915 |
| Age (years) | 80+ vs 18-44 | 0.935 | 0.736–1.190 | 0.586 |
| Sex | Female vs Male | 1.008 | 0.932–1.090 | 0.843 |
| Sector | Public vs Private | 1.745 | 1.607–1.895 | 5.88e-40 |
| Discharge year | 2016 vs 2015 | 0.960 | 0.807–1.142 | 0.646 |
| Discharge year | 2017 vs 2015 | 0.858 | 0.726–1.015 | 0.0738 |
| Discharge year | 2018 vs 2015 | 1.035 | 0.873–1.226 | 0.693 |
| Discharge year | 2019 vs 2015 | 1.722 | 1.455–2.039 | 2.84e-10 |
| Discharge year | 2020 vs 2015 | 1.602 | 1.337–1.919 | 3.12e-07 |
| Discharge year | 2021 vs 2015 | 1.746 | 1.465–2.080 | 4.48e-10 |
| Discharge year | 2022 vs 2015 | 2.025 | 1.698–2.415 | 4.17e-15 |
| Discharge year | 2023 vs 2015 | 1.861 | 1.562–2.216 | 3.41e-12 |
| Discharge year | 2024 vs 2015 | 1.890 | 1.582–2.259 | 2.51e-12 |

## B. Infratentorial/midline versus supratentorial

event=1: C715–C717; reference=0: C710–C714. N=6,192; events=1,523; non-events=4,669. Excludes 112 C718 and 4,668 C719 records.

| Predictor | Category vs reference | aOR | 95% Wald CI | Wald p |
|---|---|---:|---|---:|
| Age (years) | 0-17 vs 18-44 | 1.141 | 0.985–1.320 | 0.0784 |
| Age (years) | 45-64 vs 18-44 | 0.446 | 0.372–0.535 | 2.59e-18 |
| Age (years) | 65-79 vs 18-44 | 0.328 | 0.260–0.415 | 8.09e-21 |
| Age (years) | 80+ vs 18-44 | 0.563 | 0.371–0.853 | 0.00679 |
| Sex | Female vs Male | 0.991 | 0.878–1.119 | 0.882 |
| Sector | Public vs Private | 0.451 | 0.399–0.510 | 8.23e-37 |
| Discharge year | 2016 vs 2015 | 0.966 | 0.706–1.323 | 0.831 |
| Discharge year | 2017 vs 2015 | 1.376 | 1.027–1.843 | 0.0323 |
| Discharge year | 2018 vs 2015 | 1.846 | 1.379–2.472 | 3.81e-05 |
| Discharge year | 2019 vs 2015 | 1.585 | 1.198–2.095 | 0.00124 |
| Discharge year | 2020 vs 2015 | 1.509 | 1.121–2.030 | 0.00662 |
| Discharge year | 2021 vs 2015 | 1.464 | 1.102–1.945 | 0.00853 |
| Discharge year | 2022 vs 2015 | 1.484 | 1.120–1.966 | 0.00601 |
| Discharge year | 2023 vs 2015 | 1.557 | 1.173–2.068 | 0.00222 |
| Discharge year | 2024 vs 2015 | 1.211 | 0.897–1.634 | 0.212 |

## C. All recorded categories (descriptive)

| Category | Admissions | Percent of all 10,972 admissions |
|---|---:|---:|
| Supratentorial | 4669 | 42.55% |
| Infratentorial/midline | 1523 | 13.88% |
| Overlapping | 112 | 1.02% |
| Unspecified | 4668 | 42.54% |

References in both models: ages 18–44, male, private sector and 2015; reference aOR=1 by definition. Both primary models exclude ethnicity, final stay, death and residence area as predictors. Ethnicity is retained descriptively and in separate extended sensitivity models.

95% Wald intervals and two-sided coefficient Wald p-values use observed-information covariance assuming independent admission records. Patient/facility clustering and systematic coding error are unresolved. Comparisons are exploratory without multiplicity adjustment or significance highlighting. CSV retains full numerical p-values; displayed values use three significant digits.

C715 ventricular codes belong to the operational midline group; a sensitivity excludes them. Non-C719 coding is not validated coding accuracy. Panel B is conditional on recorded site classification, not a missing-site correction or population tumour-location risk model. C718 remains descriptive, with no forced compartment assignment. Period sensitivity is material; the pediatric contrast changes with the study years.

The legacy NOMREG Hessian warning and new separation certificates explain why the former four-outcome model is not reported. All sample flows, fit/separation diagnostics, sensitivity estimates and sparse extended-ethnicity profile intervals are in provenance/t05/.

[Model decision, methods and primary sources](../../Writeable/t05_anatomy_analysis.md).
