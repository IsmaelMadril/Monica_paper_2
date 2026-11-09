# Rebuilt Table 4 — adjusted associations with in-hospital death

Binary logistic regression, maximum likelihood, all audited C71 admissions (2015–2024). N=10,972; death=1 (963), live discharge=0 (10,009). No primary-model exclusions.

| Predictor | Category vs reference | Admissions in category | Deaths in category | aOR | 95% Wald CI | Wald p | Sparse level |
|---|---|---:|---:|---:|---|---:|---|
| Age (years) | 18-44 vs 0-17 | 2978 | 211 | 1.080 | 0.880–1.324 | 0.463 |  |
| Age (years) | 45-64 vs 0-17 | 2939 | 294 | 1.593 | 1.312–1.934 | 2.59e-06 |  |
| Age (years) | 65-79 vs 0-17 | 1618 | 208 | 2.153 | 1.742–2.661 | 1.34e-12 |  |
| Age (years) | 80+ vs 0-17 | 308 | 48 | 2.631 | 1.864–3.715 | 3.87e-08 |  |
| Sex | Female vs Male | 5028 | 438 | 0.972 | 0.850–1.111 | 0.674 |  |
| Ethnicity | Indigenous vs Mestizo | 89 | 12 | 1.429 | 0.770–2.653 | 0.258 |  |
| Ethnicity | Afro-Ecuadorian/Afrodescendant (source 2) vs Mestizo | 13 | 2 | 1.666 | 0.363–7.633 | 0.511 | Yes |
| Ethnicity | Negro/a (source 3) vs Mestizo | 14 | 2 | 1.809 | 0.395–8.290 | 0.445 | Yes |
| Ethnicity | Mulato/a (source 4) vs Mestizo | 22 | 5 | 3.560 | 1.287–9.843 | 0.0144 | Yes |
| Ethnicity | Montubio vs Mestizo | 32 | 4 | 1.645 | 0.571–4.741 | 0.357 | Yes |
| Ethnicity | White vs Mestizo | 99 | 9 | 0.859 | 0.428–1.725 | 0.669 | Yes |
| Ethnicity | Other vs Mestizo | 550 | 68 | 1.210 | 0.919–1.592 | 0.174 |  |
| Ethnicity | Unknown/not recorded vs Mestizo | 1290 | 99 | 0.739 | 0.589–0.928 | 0.00907 |  |
| Sector | Public vs Private | 6600 | 618 | 1.201 | 1.035–1.394 | 0.0159 |  |
| Recorded anatomical group | Infratentorial/midline vs Supratentorial | 1523 | 131 | 1.281 | 1.035–1.586 | 0.0229 |  |
| Recorded anatomical group | Overlapping vs Supratentorial | 112 | 7 | 0.738 | 0.340–1.605 | 0.444 | Yes |
| Recorded anatomical group | Unspecified vs Supratentorial | 4668 | 454 | 1.246 | 1.074–1.445 | 0.00372 |  |
| Discharge year | 2016 vs 2015 | 1057 | 95 | 0.989 | 0.733–1.334 | 0.942 |  |
| Discharge year | 2017 vs 2015 | 1221 | 113 | 1.001 | 0.751–1.334 | 0.997 |  |
| Discharge year | 2018 vs 2015 | 1148 | 104 | 0.956 | 0.714–1.281 | 0.764 |  |
| Discharge year | 2019 vs 2015 | 1239 | 103 | 0.922 | 0.688–1.236 | 0.587 |  |
| Discharge year | 2020 vs 2015 | 942 | 75 | 0.892 | 0.649–1.227 | 0.482 |  |
| Discharge year | 2021 vs 2015 | 1080 | 87 | 0.912 | 0.672–1.239 | 0.556 |  |
| Discharge year | 2022 vs 2015 | 1098 | 101 | 1.099 | 0.817–1.479 | 0.532 |  |
| Discharge year | 2023 vs 2015 | 1095 | 101 | 1.034 | 0.768–1.391 | 0.827 |  |
| Discharge year | 2024 vs 2015 | 1019 | 87 | 0.930 | 0.684–1.265 | 0.645 |  |

All included covariates: age group, sex, ethnicity, binary sector, recorded anatomical group and categorical discharge year. References: ages 0–17, male, Mestizo (source code 6), private sector, supratentorial group and 2015. Source ethnicity 9 is an explicit unknown category; Other is distinct. Reference rows have aOR=1 by definition and are not separately estimated.

aOR: adjusted odds ratio for death, conditional on the listed covariates. 95% Wald intervals and two-sided coefficient Wald p-values use observed-information covariance. The model has 27 parameters including its intercept. Counts shown are marginal category counts, not separate fitted sample sizes. Final stay and residence area are excluded. Sparse flags mean fewer than ten deaths or live discharges; supplementary profile-likelihood intervals are in provenance/t04/sparse_profile_intervals.csv.

Admission records are assumed independent; patient and facility clustering are unresolved. Exploratory comparisons have no multiplicity adjustment or significance highlighting. These are admission-level associations, not causal effects, survival estimates or validated predictions. CSV retains full numerical p-values; displayed values use three significant digits.

[Model specification, diagnostics and sensitivities](../../Writeable/t04_mortality_analysis.md).
