# Hospitalizations and In Hospital Deaths Associated With Malignant Brain Neoplasms in Ecuador From 2015 to 2024

A nationwide analysis of discharge records

## Abstract

**Objective.** To describe hospitalizations and in-hospital deaths associated with malignant brain neoplasm discharge codes in Ecuador during 2015–2024 and examine admission-level associations with death and recorded anatomical coding.

**Methods.** We conducted a retrospective analysis of annual INEC hospital-discharge records. Admissions with a primary discharge diagnosis coded C71.0–C71.9 were retained without patient deduplication. Resident-population rates were directly standardized to Ecuador's observed 2022 census age distribution using annual population estimates. Binary logistic models estimated adjusted odds ratios (aORs) with 95% confidence intervals (CIs). Coding detail and anatomical group were analyzed separately.

**Results.** The reconstruction included {{admissions}} admissions and {{deaths}} in-hospital deaths. Admission-level fatality was {{fatality}}% (95% CI {{fatality_lo}}–{{fatality_hi}}). Resident-population rates excluded {{foreign}} live discharges with foreign residence. The mean annual age-adjusted hospitalization rate was {{aahr}} per 100,000 residents (95% CI {{aahr_lo}}–{{aahr_hi}}), and the corresponding in-hospital death rate was {{death_rate}} ({{death_rate_lo}}–{{death_rate_hi}}). Ages 80 years or older had higher adjusted death odds than ages 0–17 (aOR {{age_or}}, 95% CI {{age_lo}}–{{age_hi}}). Unspecified C71.9 coding accounted for {{unspecified}} admissions ({{unspecified_pct}}%). Among {{site_admissions}} records assigned to either anatomical group, ages 0–17 versus 18–44 had an aOR of {{site_or}} ({{site_lo}}–{{site_hi}}) for infratentorial/midline versus supratentorial coding; estimates varied materially by period.

**Conclusions.** These estimates describe recorded hospital service events and deaths during admission, rather than cancer incidence or overall cancer mortality. Older age was associated with higher adjusted death odds. Frequent unspecified coding, period-sensitive anatomical associations and unresolved repeat-admission dependence limit interpretation.

**Keywords.** Hospital discharge records; malignant brain neoplasms; Ecuador; hospitalization; in-hospital death; administrative health data.

<!-- PAGE -->

## Study framing and objective

Hospital-discharge records describe the use of inpatient care and outcomes observed during admission. For malignant brain neoplasms, these records can describe recorded hospitalization burden, discharge diagnoses and in-hospital deaths. They do not identify incident cancers or deaths occurring outside the included admissions. Our objective was to describe annual age-adjusted hospitalization and in-hospital death rates associated with C71 discharge codes in Ecuador from 2015 to 2024, characterize admission-level fatality and examine exploratory adjusted associations with death, recorded coding detail and anatomical group.

## Study design and data sources

We performed a retrospective repeated cross-sectional analysis of discharge records in Ecuador's annual INEC Registro Estadístico de Camas y Egresos Hospitalarios releases for 2015–2024. The source is a national administrative operation, rather than a population cancer registry. Records represent discharges in the relevant annual release, including stays beginning before that year. National scope does not establish complete capture of every cancer admission or institution. We accessed the annual released SPSS files and available dictionaries, not clinical records or a restricted patient-identification database. [R01, R08]

Annual releases and available dictionaries were acquired on 23 October 2026; additional early-year syntax materials were inspected during the audit. Source URLs, acquisition timestamps, archive members, versions where identifiable and SHA-256 fingerprints are provided in the supplementary source manifests. Population workbooks were acquired separately on 6 November 2026. These national inputs were used to reconstruct the analysis independently of the previously supplied SAV, SPV and two XLSX files, which constitute the complete original analysis package. The reconstructed and historical cohorts are not interchangeable. [R01, R03, R04]

## Record selection and analysis populations

The annual files contained {{source_records}} discharge records. We trimmed whitespace, converted diagnosis strings to uppercase and removed the decimal point, then required an exact normalized primary-diagnosis code C710 through C719. A C71 prefix alone was insufficient. Of {{prefix_records}} prefix-matching records, {{prefix_rejected}} did not satisfy the exact subcode rule; {{other_records}} source records in total were outside the eligible definition. The final extract contained {{admissions}} eligible admissions, with no postselection deletion for duplicate projections or covariate availability. The annual selection flow and code list are supplied in the supplementary audit. [R01, R02, R08]

We retained all eligible discharge records, including records with identical observed attributes. Annual source-row keys preserve record identity but cannot establish person identity or distinguish a readmission from a duplicate across institutions. No person-level deduplication or person-level database linkage was performed. All ten years were retained; the severe 2017/2023 count deficits in the historical extract were not reproduced by the national-source reconstruction. Their historical processing mechanism remains unknown.

The descriptive and primary regression populations contain all {{admissions}} admissions. Primary population-denominator rates use {{resident_admissions}} records after excluding {{foreign}} live discharges coded as foreign residence, thereby matching the national resident denominators. Rural/urban comparisons alone use the verified 2018–2024 mappings and include {{verified_admissions}} admissions; {{early_admissions}} early-year records are excluded from those comparisons only.

<!-- PAGE -->

## Outcome definitions and anatomical groups

The primary binary outcome was death during the recorded admission, explicitly coded 1 for INEC discharge conditions 2 or 3 (death before 48 hours or at 48 hours or later) and 0 for condition 1 (live discharge). There were no unrecognized discharge outcomes. The endpoint is admission-level death, with no follow-up after discharge; it is not patient survival or disease-specific mortality after diagnosis. [R01]

The diagnosis scope was malignant brain neoplasm coded C71.0–C71.9 as the primary discharge diagnosis. This does not establish histological confirmation or a first primary tumour. The operational groups were supratentorial C71.0–C71.4, infratentorial/midline C71.5–C71.7, overlapping C71.8 and unspecified C71.9. C71.5 identifies cerebral ventricles and is not universally infratentorial; its placement in the combined midline group is a study choice. C71.8 was not forced into a single compartment. C71.9 records unspecified coding, not a biological anatomical site. No clinical validation against pathology or case notes was available. [R02]

## Covariate construction and data checks

Age was reconstructed in completed years using source age units. Valid ages recorded in hours, days or months were assigned zero completed years; valid ages in years were grouped as 0–17, 18–44, 45–64, 65–79 and 80 or older. Invalid or unknown age codes were not assigned to the oldest category. Sex retained the recorded male/female categories. Ethnicity retained all nine distinct source categories, including source code 9 as Unknown/not recorded and a separate Other category. The source coding, rather than inferred ethnicity from other fields, was used. [R01]

Health sector was classified as public versus private; private nonprofit and private for-profit were combined for regression and also displayed separately descriptively. Discharge year was categorical. Recorded length of stay used mutually exclusive categories 0, 1–3, 4–14, 15–30 and 31 or more days. Day 30 belonged only to 15–30. We retained recorded stays rather than substituting calendar differences or capping long stays. There were 827 same-calendar-day admissions with a recorded one-day stay, and the longest recorded stay was 1,684 days with a matching date interval. Stay was a descriptive measure and excluded from primary regression because its final value can depend on death/discharge timing.

Province of residence and treating-facility province were retained as distinct variables. Foreign residence was distinct from missing residence. Urban/rural residence labels were verified for 2018–2024; the 2015–2017 mappings remained provisional. Neither provisional values nor their apparent categories were used in primary models or national rate calculations. No province was used as a proxy for patient or facility identity.

We checked identifiers, diagnosis mappings, source age units, category bounds, discharge outcomes, parsed dates, annual totals and missing values. All selected records had classifiable age, sex, sector, diagnosis and outcome values under the executed definitions. No displayed characteristic had a true null, but {{unknown_ethnicity}} records had source-coded unknown ethnicity. Unknown ethnicity was retained explicitly and not imputed. No multiple imputation was performed. Distinct source rows with repeated attributes were retained. Code checks were not validation of clinical diagnoses, self-reported characteristics or registration completeness. [R08, R09]

<!-- PAGE -->

## Population denominators and standardization

Annual denominators were INEC national population estimates at 30 June, both sexes combined, from Estimaciones y Proyecciones de Población Revisión 2024, expanded v2 workbook, national sheet 1.1. Single-age data through age 99 and 100 or older were aggregated to the five analysis age groups. Fixed standard weights came from observed Ecuador 2022 census counts, workbook 01_2022_CPV_Estructura_poblacional, sheet 3, Total Nacional. The standard contained 16,938,986 persons. It was not reused as every year's denominator: the 2022 midyear estimate was 17,715,301. Exact cell locators and source hashes are supplied with the population extraction. [R03, R04]

For discharge year t and age group i, let H_it be resident admissions, D_it deaths during those admissions, P_it the annual resident population and w_i the fixed census age proportion, with sum_i(w_i)=1. Age-specific rates were 100,000 × H_it/P_it and 100,000 × D_it/P_it. The age-adjusted hospitalization rate was AAHR_t = 100,000 × sum_i(w_i H_it/P_it), and the age-adjusted in-hospital death rate was AAIMR_t = 100,000 × sum_i(w_i D_it/P_it). The AAIMR abbreviation denotes this population-denominator measure only. Both outcomes and all anatomical components used identical denominators and weights. [R05]

The primary period summary was the arithmetic mean of ten annual standardized rates, sum_t(rate_t)/10. It was not a cumulative risk or a pooled population-year rate. A separately labelled sensitivity standardized pooled age-specific counts and population-years. Admission-level fatality was 100 × deaths/admissions within the stated record population, not AAIMR/AAHR. The abstract's fatality uses all admissions; population-denominator rate summaries use resident admissions.

## Uncertainty and alternative rate specifications

Age-specific rate intervals used central Poisson/gamma limits; directly standardized rates used Fay–Feuer gamma limits. For the unscaled weighted count R=sum(a_i k_i), V=sum(a_i² k_i) and b=max(a_i), the lower limit used the 0.025 gamma quantile with shape R²/V and scale V/R when R>0, or zero when R=0. The upper limit used the 0.975 quantile with shape (R+b)²/(V+b²) and scale (V+b²)/(R+b). All strata, including zero-event strata, remained in b. Limits were multiplied by 100,000. For the mean annual rate, the weighted count pooled year/age cells with coefficients w_i/(10 P_it); annual endpoints were not averaged. Fatality intervals used the Wilson score method. [R06, R07]

Intervals are conditional on fixed denominators and weights and independent admission events, with Poisson variation for rates and binomial variation for fatality. They do not include demographic-estimation error, incomplete capture, miscoding or dependence between repeat admissions. They are not complete uncertainty bounds for a national census of service events. Sensitivities used 18 narrower age bands (0–4 through 80–84, 85 or older), all discharges including foreign residents, and pooled population-year summaries. Event counts below ten were flagged rather than suppressed. No formal trend or COVID-effect test was performed.

<!-- PAGE -->

## Primary regression models

We estimated maximum-likelihood binary logistic models for exploratory admission-level associations, not causal effects or validated prediction. The death model included categorical age, sex, all source ethnicity categories, binary sector, recorded anatomical group and discharge year, with 27 parameters including the intercept. References were ages 0–17, male, Mestizo (source code 6), private sector, supratentorial group and 2015. It included {{admissions}} admissions and {{deaths}} deaths, with no primary complete-case exclusions. Final stay and residence area were excluded. [R13]

Two separate primary models addressed recorded coding and anatomy. The coding model used non-C71.9 diagnoses (C71.0–C71.8) as event 1 and C71.9 as reference 0, including {{admissions}} records and {{coding_events}} events. C71.8 was included without implying a single recorded site. The conditional-site model used infratentorial/midline C71.5–C71.7 as event 1 and supratentorial C71.0–C71.4 as reference 0; it included {{site_admissions}} records and {{site_events}} events after excluding {{overlapping}} C71.8 and {{unspecified}} C71.9 records. Both models adjusted for age group, sex, binary sector and categorical year, with 16 parameters including the intercept and references ages 18–44, male, private sector and 2015. Ethnicity was descriptive and used in separate extended sensitivity models, not primary anatomy/coding adjustment.

The four-outcome multinomial model was not retained: unspecified coding mixes documentation with anatomy, and zero C71.8 cells in source ethnicity levels yield explicit directions without a finite unpenalized maximum. The saved original NOMREG also reported Hessian singularities. A larger iteration cap alone was not treated as a remedy. The binary replacements answer different, declared questions; their aORs are not the original adjusted relative risk ratios. [R14, R15]

No significance-based selection, interaction search or outcome-driven ethnicity merging was performed. Age, sex, sector and year provide a limited descriptive adjustment set; they do not establish exchangeability or control for severity, histology, grade, treatment, comorbidity or referral pathways. Anatomical coding and year are recorded at discharge and are not asserted to be measured before all clinical events.

## Model diagnostics and precision

Every fitted specification was checked for full design rank, complete/quasi-separation using linear programming, captured warnings, convergence, finite coefficients and standard errors, score residuals and positive information eigenvalues. Output generation stops on failure. All eight death-model and 15 coding/site fits passed their executed checks. Primary aORs have observed-information 95% Wald intervals and two-sided coefficient Wald p-values. Sparse contrasts were flagged when fewer than ten events or non-events occurred in a category. Supplementary profile-likelihood intervals used nuisance-parameter refitting and the asymptotic likelihood-ratio cutoff 3.841 for one degree of freedom; these are not exact small-sample intervals. [R13, R15, R16]

<!-- PAGE -->

## Sensitivity analyses and descriptive comparisons

Death-model sensitivities restricted to residents, excluded 2017/2023 as a historical-error stress test, restricted to verified residence years with and without residence adjustment, added final stay descriptively, excluded unknown ethnicity, and used HC0 covariance. Coding/site sensitivities used residents, the same year exclusions, verified years with and without residence, HC0 covariance and all ethnicity categories in extended models. A further site fit excluded C71.5. Sensitivities did not replace the primary fit because of a p-value or preferred direction. Excluding 2017/2023 did not imply that their official releases were incomplete. HC0 covariance does not correct unobserved person/facility clustering.

Tables 1–2 present counts and column percentages with explicit denominators. Table 1 additionally presents within-category fatality. Each characteristic partitions its stated population; percentages are not added across characteristic blocks. Residence blocks alone use 2018–2024. We performed one exploratory omnibus independence comparison per characteristic. Uncorrected Pearson chi-square was used only when every observed and expected active cell was at least five. Sparse 2×2 tables used two-sided Fisher exact; other sparse tables used fixed-margin Monte Carlo Pearson tests with 99,999 Patefield draws and deterministic per-comparison seeds. The Monte Carlo tail included ties, and p=(exceedances+1)/(draws+1). Zero-margin rows remained visible descriptively but were excluded from testing. Seeds, exceedances, approximate simulation errors and exact binomial intervals for the simulated tail probabilities are supplied. [R17]

Full p precision is retained in machine-readable outputs; presented p-values use three significant digits and scientific notation for small values. Zero-exceedance simulations are labelled at their minimum attainable p rather than as exact probabilities or bounds. No multiplicity adjustment or significance highlighting was used. These comparisons are exploratory and do not establish clinical importance, causal effects or stability over time.

## Bias and reproducibility

Selection into admission, variable coverage, repeated admissions, clinical coding error, temporal recording changes and unmeasured severity can affect estimates. Records were not linked to pathology, cancer incidence, longitudinal patient files or out-of-hospital death records. Annual files were stacked; population totals were matched by year and age only, not by individual identity. Hospital/facility clustering and person dependence could not be resolved by valid identifiers. The conditional-site analysis selects records with assignable group codes and is not a correction for nonrandom missing site information. A change in non-C71.9 coding cannot validate improved diagnostic accuracy.

The revised analysis used Python 3.14.7, pandas 3.1.0, SciPy 1.18.1, statsmodels 0.15.0 and pyreadstat 1.3.7 in the recorded macOS environment. Earlier rate-stage Windows runs are documented separately. The historical SPSS output was audited but was not used as a validated model estimate. Source manifests, code lists, variable definitions, selection flow, scripts, model specifications, diagnostics and aggregate outputs accompany the reproducibility materials. Public access to source releases does not establish permission to redistribute every file; availability is described artifact by artifact. [R08, R09, R10]

A companion STROBE and RECORD crosswalk identifies covered items and unresolved reporting requirements. It does not assert blanket compliance. Clinical code validation and an independent clinical assessment were unavailable. 

<!-- PAGE -->

## Source notes

R identifiers match the project's numbered bibliography and source manifests. Full locators, artifact versions, code and local numerical verification are in the accompanying reproducibility materials. The following are the primary references for these sections.

R01. INEC. Registro Estadístico de Camas y Egresos Hospitalarios. Annual releases 2015–2024 and year-specific dictionaries. https://www.ecuadorencifras.gob.ec/camas-y-egresos-hospitalarios-informacion-historica/

R02. PAHO. ICD-10 chapter II, C71 code definitions. https://ais.paho.org/classifications/Chapters/CAP02.html

R03. INEC. Estimaciones y Proyecciones de Población Revisión 2024, expanded v2 workbook, national sheet 1.1. https://www.ecuadorencifras.gob.ec/proyecciones-poblacionales/

R04. INEC. Censo Ecuador 2022, observed population structure workbook, sheet 3. https://www.censoecuador.gob.ec/resultados-censo/

R05. NCI SEER. Direct age adjustment definition. https://seer.cancer.gov/seerstat/tutorials/aarates/definition.html

R06. Fay MP, Feuer EJ. Confidence intervals for directly standardized rates. Statistics in Medicine. 1997;16:791–801. https://wonder.cdc.gov/controller/pdf/FayFeuerConfidenceIntervals.pdf

R07. Wilson EB. Probable inference, the law of succession, and statistical inference. Journal of the American Statistical Association. 1927;22:209–212. https://doi.org/10.1080/01621459.1927.10502953

R08. Benchimol EI et al. RECORD statement. PLoS Medicine. 2015;12:e1001885. https://doi.org/10.1371/journal.pmed.1001885

R09. Vandenbroucke JP et al. STROBE explanation and elaboration. PLoS Medicine. 2007;4:e297. https://doi.org/10.1371/journal.pmed.0040297

R10. Sandve GK et al. Ten simple rules for reproducible computational research. PLoS Computational Biology. 2013;9:e1003285. https://doi.org/10.1371/journal.pcbi.1003285

R13–R15. statsmodels developers. Binomial GLM, MNLogit and estimation pitfalls, version 0.15.0 documentation. https://www.statsmodels.org/stable/glm.html

R16. Wilks SS. The large-sample distribution of the likelihood ratio for testing composite hypotheses. Annals of Mathematical Statistics. 1938;9:60–62. https://doi.org/10.1214/aoms/1177732360

R17. SciPy developers. Contingency testing and fixed-margin random tables. Documentation identifies 1.18.0; execution uses 1.18.1. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html
