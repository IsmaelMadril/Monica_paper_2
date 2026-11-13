# Interpretation of Malignant Brain Neoplasm Discharges in Ecuador

## Introduction

Malignant brain neoplasm discharge codes describe a recorded diagnosis within an episode of inpatient care. They do not identify a histologically confirmed tumour subtype, a newly diagnosed cancer or a unique patient. The distinction matters when hospital-discharge data are used alongside population cancer estimates. C71 codes identify brain sites, whereas the WHO classification of central nervous system tumours combines histological and molecular information for many diagnostic categories. Site-coded administrative records cannot reproduce that diagnostic detail. [R02, R19]

For Ecuador, the archived GLOBOCAN 2024 fact sheet estimates 561 new brain and central nervous system cancer cases and 463 deaths in 2024, both sexes and all ages. These figures come from Cancer Today 2024 estimates, version 1.0, whose fact sheet is labelled September 2026 and was accessed on 12 November 2026. They are model-based estimates, not counts of observed admissions. The fact sheet describes incidence estimation using national mortality and model-based mortality-to-incidence ratios, and mortality estimation by projecting national rates. Neither quantity measures deaths restricted to an included C71 admission. [R18]

Regional work has described brain and central nervous system cancer incidence using population-based registries and mortality using the WHO mortality database, with rates standardized to a world population. These endpoints and standards differ from C71 hospitalizations standardized to Ecuador's observed census distribution. Consequently, regional cancer incidence or disease-mortality rates cannot be used as numerical benchmarks for our hospitalization or in-hospital death rates. Our analysis addresses the complementary question of recorded inpatient service events and outcomes during those events. [R20]

We analyzed annual INEC discharge records for 2015–2024 to describe hospitalizations and in-hospital deaths associated with a primary discharge diagnosis coded C71.0–C71.9. We estimated resident-population hospitalization and in-hospital death rates, described admission-level fatality and examined exploratory adjusted associations with death, recorded code detail and anatomical group. The contribution is an auditable reconstruction with explicit denominators and model populations, rather than a claim to establish incidence, complete national cancer capture or a new biological anatomical pattern. [R01, R08]

<!-- PAGE -->

## Discussion

### Recorded hospitalization burden and admission outcomes

The reconstructed analysis included 10,972 discharge records and 963 deaths during admission. Pooled admission-level fatality was 8.78% (95% Wilson interval 8.26–9.32). After excluding 3 live discharges with foreign residence, the mean of ten annual age-adjusted hospitalization rates was 6.611 per 100,000 residents (95% gamma interval 6.487–6.737); the corresponding in-hospital death rate was 0.598 (0.561–0.638). These summaries have different denominators: fatality uses included admissions, while the standardized rates use annual resident populations and fixed observed 2022 census weights. Neither is a cancer incidence estimate or a measure of overall brain cancer mortality. [R01; Tables 1–3]

These service-event estimates should not be interpreted as higher or lower cancer occurrence than the IARC estimates or regional registry rates. A person may have several admissions, and a person with cancer may have no admission in an included institution or year. Deaths at home or after discharge are outside the outcome definition. Comparing the standardized in-hospital death rate with a GLOBOCAN disease-mortality rate would therefore not quantify the fraction of all cancer deaths captured in hospital. The cancer definitions, observation processes and age standards also differ. [R18, R20]

### Temporal observations and the historical extract

The resident hospitalization rate was 7.441 per 100,000 in 2019 (95% interval 7.030–7.871) and 5.540 in 2020 (5.191–5.908). The lower 2020 value coincided with the first pandemic year. The records do not measure imaging delays, postponed surgery, emergency prioritization, unmet need or the counterfactual admission rate without the pandemic. The timing alone cannot distinguish changes in disease presentation, admission decisions, service availability, case mix or recording. These are possible explanations to investigate, not mechanisms demonstrated by this analysis.

The reconstructed official releases contained 1,221 C71 admissions in 2017 and 1,095 in 2023, including live discharges in both years. The extreme low counts and all-death 2023 subset in the historical analytic files were not reproduced. This removes the basis for describing those particular historical deficits as national registration disruptions. It does not establish that the official data capture every eligible admission, and the original extraction mechanism remains unresolved. Both years were retained in the primary analysis; their exclusion was only a sensitivity analysis. [Tables 1–3; supplementary annual audit]

Rates are described with model-based intervals, without a formal trend or interrupted-time-series analysis. The equal-year mean is not a test of stability. Likewise, an omnibus year comparison of fatality or a regression year interval containing one cannot demonstrate stable mortality, unchanged care or protected emergency services. No causal COVID effect, absence of temporal change or intervention effect is inferred.

<!-- PAGE -->

### Death associations and clinical interpretation

In the primary death model, ages 80 or older versus ages 0–17 had an aOR of 2.631 (95% Wald interval 1.864–3.715). This corrected direction does not support the historical protective-age interpretation. The saved original model coded live discharge as its event and also failed to reach a final solution; reciprocating its reported odds ratios would not repair the old cohort or failed fit. Our estimates describe adjusted odds of death during an admission, not individual prognosis after cancer diagnosis or survival benefit. [Table 4; supplementary event-coding audit]

Public versus private sector had an adjusted death OR of 1.201 (1.035–1.394). Sector labels do not identify tertiary status, treatment complexity, referral pathways or quality of care. Selection into admission and unmeasured severity can affect the comparison. Differences in sector composition or death odds cannot demonstrate inequitable access or that one sector caused better outcomes. The available covariates do not establish comparable clinical populations across sectors. Final stay was excluded from the primary model because death and discharge timing can determine its duration; a stay-duration coefficient cannot be interpreted as a treatment benefit or a diagnostic/surgical window.

### Recorded code detail and conditional anatomy

Unspecified C71.9 coding remained common: 4,668 admissions (42.54%) overall and 379 in 2024. Its 2024 resident age-adjusted hospitalization rate was 2.152 per 100,000 (95% interval 1.941–2.381), not zero. The coding model associated 2024 versus 2015 with greater odds of non-C71.9 coding (aOR 1.890, 1.582–2.259). More detailed coding can occur without more accurate diagnosis, and case mix or documentation practice can change. No chart/pathology validation establishes improved coding accuracy, diagnostic precision or elimination of unspecified records. [Tables 2–3, 5]

The site comparison excluded C71.8 and C71.9 by definition and included 6,192 records assigned to either operational anatomical group. Ages 0–17 versus 18–44 had an aOR of 1.141 (0.985–1.320) for infratentorial/midline versus supratentorial coding. This all-year interval includes one, without proving identical distributions. In the 2018–2024 core sensitivity the contrast was 1.698 (1.429–2.017). The material period sensitivity limits a single general anatomical conclusion; no formal interaction test established its cause. The later-period estimate is not substituted for the primary result because it is more statistically clear. [Table 5; supplementary sensitivity fits]

The conditional-site analysis describes selected coded admissions, not the anatomical distribution of all cancers or all C71 records. Missing site detail may be nonrandom. C71.5 ventricular codes are not universally infratentorial, and C71.8 is not assigned to one compartment. We therefore do not infer a new biological pediatric pattern, an ethnicity-specific tumour propensity or a population anatomical risk from these models. The coding and site models have different outcome populations and cannot be combined as an established correction for site-selection bias. [R02; Table 5]

<!-- PAGE -->

### Limitations and contribution

The observation is a discharge record. Reliable patient linkage was unavailable, so repeat admissions could not be identified and records with matching observed attributes were retained. The analysis cannot separate first admissions, readmissions and recurrent disease at person level. Treating records as independent can misstate interval precision; patient and facility dependence may remain. HC0 covariance is record-based and does not resolve clustering. The direction or size of these uncertainty errors cannot be determined here.

The administrative diagnosis was not validated against case notes, imaging or pathology. C71 coding does not provide integrated histological/molecular classification, tumour grade, treatment, functional status, comorbidity, referral severity or palliative intent. Those omissions limit adjustment and biological interpretation. Unknown ethnicity was retained explicitly rather than made known by imputation. The rural/urban labels for 2015–2017 remain provisional; residence comparisons were restricted to verified 2018–2024 labels and cannot describe the entire decade. [R08, R19]

Selection into inpatient care limits applicability to people who are never admitted or receive care outside the included releases. Institutional coverage, transfer practices, source coding and annual registration can change; reconstructing ten official files does not independently validate complete or constant national ascertainment. No patient, institution or external death linkage was available to resolve those mechanisms. In-hospital death cannot substitute for overall cancer mortality, long-term survival or postdischarge outcome.

Direct standardization improves comparability of the specified age distributions, but five broad age bands can leave residual age differences. The narrower-band sensitivity assesses one aspect of that choice, not every source of confounding. The annual population estimates and observed census weights are treated as fixed in the rate intervals. Those intervals do not include population-estimation error, systematic undercapture or miscoding, and the mean annual rate is not cumulative cancer risk. [R03–R07]

The death and coding/site models were finite and passed the stated numerical diagnostics; this supports estimability under their designs, not clinical validity or causal identification. Sparse ethnicity contrasts remain imprecise, including when supplementary asymptotic profile intervals are used. Exploratory comparisons were not multiplicity-adjusted, and individual p-values should not be selected as confirmed subgroup effects. Restricting the site model to assignable groups does not correct nonrandom missing detail or unmeasured case mix.

The study provides reproducible release identifiers, selection rules, age/stay recodes, matched rate denominators, model populations and numerical diagnostics. Its practical contribution is a documented description of recorded inpatient events that complements cancer-registration estimates. External literature supplies context and classification; the current data supply the admission counts and associations. Future chart validation and valid record linkage could examine coding accuracy, readmission patterns and outcomes beyond discharge. Such work would be needed before attributing sector differences to care quality or prescribing specific referral, surgical or imaging policies. [R08, R09]

<!-- PAGE -->

## Conclusion

Among 10,972 C71-coded admissions in Ecuador during 2015–2024, 963 ended in death during the recorded admission. The mean annual resident age-adjusted hospitalization and in-hospital death rates were 6.611 and 0.598 per 100,000, respectively. Older age was associated with higher adjusted admission-level death odds. Unspecified coding remained frequent, and anatomical comparisons were conditional on recorded site groups and sensitive to the observation period. These findings describe recorded inpatient service events; they do not establish cancer incidence, overall cancer mortality, improved coding accuracy, causal care disparities or a stable temporal burden. Transparent source reconstruction and explicit denominators provide a basis for further validation and service-description research.

## References for the replacement sections

R01–R09 retain the primary-source identities in the reconstruction bibliography. Tables and supplementary audits refer to the rebuilt T02–T06 outputs, not the historical manuscript tables.

R01. INEC. Registro Estadístico de Camas y Egresos Hospitalarios, annual releases 2015–2024. Source URLs, versions and hashes are preserved in the annual source manifest.

R02. PAHO/WHO. ICD-10 chapter II, C71 definitions. https://ais.paho.org/classifications/Chapters/CAP02.html

R03–R07. INEC annual population estimates and observed 2022 census counts; NCI SEER direct standardization; Fay–Feuer gamma intervals; Wilson score intervals. Full entries and exact source locators are in the reconstruction bibliography and T03 methods.

R08. Benchimol EI et al. The RECORD statement. PLoS Medicine. 2015;12:e1001885. https://doi.org/10.1371/journal.pmed.1001885

R09. Vandenbroucke JP et al. STROBE explanation and elaboration. PLoS Medicine. 2007;4:e297. https://doi.org/10.1371/journal.pmed.0040297

R18. Ervik M et al. Global Cancer Observatory Cancer Today. 2024 estimates, version 1.0. IARC; 2026. Ecuador fact sheet, September 2026 release, p. 2. Accessed 12 November 2026. https://gco.iarc.who.int/media/globocan/factsheets/populations/218-ecuador-fact-sheet.pdf

R19. Louis DN et al. The 2021 WHO Classification of Tumors of the Central Nervous System a summary. Neuro-Oncology. 2021;23:1231–1251. https://doi.org/10.1093/neuonc/noab106

R20. Piñeros M, Sierra MS, Izarzugaza MI, Forman D. Descriptive epidemiology of brain and central nervous system cancers in Central and South America. Cancer Epidemiology. 2016;44 Suppl 1:S141–S149. https://doi.org/10.1016/j.canep.2016.04.007
