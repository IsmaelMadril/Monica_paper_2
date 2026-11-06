# Bibliographic rationale for reconstruction and reanalysis

Recorded 6 November 2026. This register covers the implemented T01-T03 reconstruction, the optional legacy comparison, Table 3, and the current reproduction/verification workflow. It does not certify unimplemented T04-T10 analyses.

## How the evidence is used

Each change has three distinct supports: the official source defines the recorded data; methodological literature defines a procedure or reporting principle; local computational evidence establishes this project's results. A reference cannot prove that a code ran correctly or that a diagnosis was clinically valid. RECORD and STROBE are reporting guidelines, not validation certificates. [R08](#r08), [R09](#r09).

The decisions below include explicit study choices and unresolved questions. Calling a choice "supported" does not mean that a guideline mandates it. The supplied SAV/SPV/XLSX package was confirmed complete by the author on 6 November 2026; that is project correspondence, not a published source. Historical discrepancies must remain linked to preserved artifacts.

## Decisions and supporting evidence

The machine-readable version is [reconstruction_decisions.csv](../provenance/reconstruction_decisions.csv). Paths in that file are relative to the repository root.

| ID | Change and reason | Bibliographic support | Nature of support and limits |
|---|---|---|---|
| D01 | **Reconstruct independently of legacy files.** The INEC cohort depends on official releases, not the availability of a previous analytic extract. The optional legacy comparison is a separate provenance question. | [R10](#r10), [R08](#r08) | Implementation choice. --compare-legacy still verifies the thesis baseline; absence of those files cannot validate a historical comparison. |
| D02 | **Select primary discharge diagnosis C71.0-C71.9.** Use the source diagnosis field and exact normalized subcodes; exclude other neoplasms from this operational target. | [R01](#r01), [R02](#r02) | Source-defined coding plus study scope. C71-coded admissions are not histologically confirmed incident patients. |
| D03 | **Correct C71.4 and C71.7 placement.** Occipital-lobe and brainstem codes must not inherit incompatible legacy labels. | [R02](#r02) | Coding correction. The combined C71.5-C71.7 infratentorial/midline category remains a study-defined grouping; C71.5 is not universally infratentorial. |
| D04 | **Retain all eligible discharge records.** No reliable patient linkage has been established; demographic equality cannot establish duplicate admissions. Retain repeated projections and count source records. | [R01](#r01), [R08](#r08) | Unit-of-analysis decision. No patient deduplication or independent-event validation is claimed. |
| D05 | **Retain 2017 and 2023.** The reconstructed releases contain 1221 and 1095 eligible admissions. Legacy low counts do not establish a national registration failure. | [R01](#r01) | Empirical correction. The mechanism of historical record losses is unknown; no pandemic or administrative causal claim follows. |
| D06 | **Recode discharge deaths from codes 2 and 3.** Annual value labels distinguish alive, death before 48 hours and death at 48 hours or later. | [R01](#r01) | Source metadata. Labels support the recode, not validation against medical records. |
| D07 | **Respect source age units and valid ranges.** INEC labels specify hours 1-23, days 1-28, months 1-11 and years 1-115. Valid subyear ages have zero completed years; invalid values remain unknown. | [R01](#r01) | Source metadata. Early-year application must remain auditable against each annual schema; no selected record is unclassifiable. |
| D08 | **Use mutually exclusive stay categories.** Preserve recorded stay; assign day 30 only to 15-30 and use 31+ for the next group. Retain date discrepancies as audit fields. | [R01](#r01), [R09](#r09) | Study categorization and arithmetic correction. No clinical threshold is validated; the inferred same-day minimum-one convention is descriptive, not proven from a manual. |
| D09 | **Preserve missing and unknown values.** Unknown ethnicity is distinct from Other; covariate missingness does not remove otherwise eligible discharges at reconstruction. | [R01](#r01), [R09](#r09) | Source coding and analytic retention. This is not a missing-data solution for future regression; model-specific handling remains pending. |
| D10 | **Separate residence, facility geography and sector.** Use prov_res for resident eligibility; keep prov_ubi separately. Preserve three source sectors and explicitly label the binary aggregation. | [R01](#r01) | Source-defined meanings; study aggregation. Facility location is not resident origin; binary sector is not the only possible grouping. |
| D11 | **Flag unverified early rural/urban labels.** The 2015-2017 residence-area interpretation lacks independent label confirmation. Preserve codes and provisional status. | [R01](#r01) | Unresolved evidence. No bibliographic assertion closes this gap. These labels are not used in Table 3. |
| D12 | **Match resident numerator to resident denominators.** Exclude three foreign-resident live discharges only from primary population rates; keep them in the full cohort and sensitivity analysis. | [R01](#r01), [R03](#r03), [R05](#r05) | Study eligibility decision. The exact exclusion policy is our decision; sources define variables and the rate framework, not an Ecuador-specific mandated exclusion. |
| D13 | **Use annual midyear population denominators.** Use national both-sex single-age estimates from Revision 2024 sheet 1.1 for each corresponding year. | [R03](#r03) | Official demographic source. Projected populations remain estimates; their uncertainty is not propagated into intervals. |
| D14 | **Use actual 2022 census standard weights.** Normalize observed census age counts (16938986) to fixed weights, separately from annual population estimates. | [R04](#r04), [R05](#r05) | Data source plus study standard. Using Ecuador 2022 is a study choice consistent with the manuscript; it is not SEER's US standard or a universally preferred standard. |
| D15 | **Use five primary age bands plus narrower sensitivity.** Keep the manuscript's 0-17, 18-44, 45-64, 65-79 and 80+ primary bands; also calculate 18 five-year/tail bands. | [R05](#r05), [R09](#r09) | Study specification. Broad bands can leave residual age differences. Agreement of overall means does not prove stability in each category. |
| D16 | **Calculate rates by direct standardization.** Sum each year's age-specific discharge/death rates multiplied by the same fixed age weights; express per 100000. | [R05](#r05) | Established statistical definition. The numerator is discharge events, so the result is not unique-patient incidence or all-cause cancer mortality. |
| D17 | **Use Fay-Feuer gamma rate intervals.** Apply the weighted independent-Poisson construction with the maximum coefficient, including zero-event strata. | [R06](#r06) | Established statistical method. Independence and fixed denominators are assumptions; the paper does not validate them for these admissions. |
| D18 | **Define the mean and pooled summaries separately.** The primary mean weights ten annual standardized rates equally; the alternative pools age-specific population-years. Mean intervals use coefficients divided by ten. | [R05](#r05), [R06](#r06) | Study estimand plus algebraic extension. The primary mean is not a guideline-mandated estimator, a ten-year risk, or an average of interval endpoints. |
| D19 | **Calculate admission fatality with Wilson intervals.** Use deaths/admissions and a binomial score interval; keep it separate from population-based standardized death rates. | [R07](#r07) | Established interval; explicit denominator. Admission fatality is not patient survival; repeat admissions may violate binomial independence. |
| D20 | **Retain sparse estimates and label uncertainty.** Flag annual event counts below ten, preserve zero-event upper limits, and avoid inferring significance from overlapping intervals. | [R06](#r06), [R12](#r12) | Study reporting convention. Below ten is a local flag, not a cited universal suppression or reliability rule. |
| D21 | **Interpret intervals conditionally.** State Poisson/binomial assumptions and omitted clustering, coding errors and demographic uncertainty; avoid causal trend conclusions. | [R12](#r12), [R09](#r09) | Model limits and cautious interpretation. No trend hypothesis test, clinical diagnostic validation or causal pandemic analysis has been performed. |
| D22 | **Freeze source bytes and record software versions.** Use immutable archives, SHA-256 checks and scripted regeneration; preserve historical manifests rather than resetting expected hashes. | [R10](#r10), [R11](#r11) | Reproducibility and integrity controls. Byte identity is distinct from scientific correctness; small platform floating-point differences require numeric comparison. |
| D23 | **Verify table values and reconcile manuscript changes.** Check source cells, independent formulas, component totals, mean definitions and displayed rounding; expose manuscript differences. | [R10](#r10) | Project-specific computational evidence. Published references justify methods; the local verification establishes the actual numbers. The old PDF and Figure 1 still need revision. |
| D24 | **Require evidence for subsequent changes.** Record the change, rationale, source locator, result checks and unresolved assumptions before carrying it into manuscript claims. | [R08](#r08), [R09](#r09), [R10](#r10) | Project reporting rule. T04-T10 are not retroactively validated; each later model, exclusion and interpretation needs its own evidence. |

## Statistical argument for Table 3

For year t and age group i, the implemented rate is R_t = 100,000 x sum_i(w_i k_it/P_it), where P_it is the annual population and w_i is the fixed census age proportion. The same denominators and weights are used for every anatomical component. Consequently, exhaustive components add to the total before rounding, and a component's death rate cannot exceed its hospitalization rate when deaths are a subset of admissions. These identities follow from the formula; they are not independent epidemiological findings. [R03](#r03), [R04](#r04), [R05](#r05).

The primary period summary is M = sum_t(R_t)/10, an explicit choice to summarize an average year. For its interval, the year/age counts form a weighted sum with coefficients a_it = w_i/(10 P_it). This is an application of the Fay-Feuer weighted-Poisson framework, rather than a claim that the original paper selected this study's summary. Pooled population-year rates are separately labelled because changing the denominators changes the estimand. [R06](#r06).

For an unscaled weighted count rate R = sum(a k), variance V = sum(a^2 k), and b = max(a), the implemented interval uses Gamma(0.025; shape R^2/V, scale V/R) below and Gamma(0.975; shape (R+b)^2/(V+b^2), scale (V+b^2)/(R+b)) above, with zero lower limit when R=0. Zero-event strata remain in b. These intervals assume independent events and fixed population values; their use does not account for dependence between admissions. [R06](#r06), [R12](#r12).

Fatality is 100 x deaths/admissions and receives a Wilson score interval. It is a different denominator and must not be estimated by dividing standardized death and hospitalization rates. [R07](#r07). The exact study counts and verified numerical estimates are documented in [the verification report](table3_verification.md), not supplied by the methodological papers.

## Manuscript-ready methods wording

Hospital-discharge records with a primary discharge diagnosis coded C71.0-C71.9 were selected from the annual INEC releases for 2015-2024, using explicit source-code selection and preserving the admission/discharge record as the unit of analysis. The complete selection and recoding specification, annual source versions, and exclusions are provided in the decision register and source manifests. Codes identify recorded malignant brain neoplasms; they do not establish unique patients or histological confirmation. [R01](#r01), [R02](#r02).

Age-adjusted hospitalization and in-hospital death rates per 100,000 residents were calculated by direct standardization to the observed age distribution of the Ecuador 2022 census. Annual national midyear population estimates from INEC Revision 2024 supplied the age-specific denominators. The five manuscript age groups were retained for the primary analysis, and narrower age groups and inclusion of foreign-resident discharges were evaluated as sensitivity analyses. Rate confidence intervals used the Fay-Feuer gamma method; admission-fatality intervals used Wilson's score method. The arithmetic mean of ten annual standardized rates and a separately labelled pooled population-year estimator were calculated. [R03](#r03), [R04](#r04), [R05](#r05), [R06](#r06), [R07](#r07).

## Evidence gaps and limits

- The C71.5-C71.7 combined "infratentorial/midline" grouping is operational. The source C71.5 code identifies cerebral ventricles, not a universally infratentorial location. Report the exact included subcodes; do not present the grouping as WHO's anatomical classification.
- Early-year residence-area labels remain provisional. No source found in this task resolves the 2015-2017 gap; those labels are not used for Table 3.
- Identical projected fields do not establish duplicate admissions, and source-row keys do not establish patient identity. Repeated-event independence remains an assumption.
- The same-day minimum-one recorded-stay convention is inferred from local date comparisons; the evidence inspected here does not establish a universal INEC rule.
- The exact historical filtering mechanism behind the legacy 8,249-record cohort is unavailable. Source reconstruction does not demonstrate INEC under-registration, a coding-accuracy improvement, or a causal COVID effect.
- Five broad age bands, the choice of 2022 Ecuador as the standard, the equal-year mean, the below-ten flag, and optional legacy comparison are declared study or implementation choices. They should not be described as requirements imposed by the cited literature.
- Regression estimates, future missing-data treatments, ethics determinations, manuscript interpretations and figures require their own subsequent evidence. They are outside the present bibliographic validation.

## Rule for subsequent revisions

For each later substantive change, extend this register with: the concrete change and trigger; the scientific or source-specific argument; an exact citation and section/table/code locator; a link to the local evidence; verification results; and assumptions or unresolved limitations. Where support is unavailable, label the choice provisional or unsupported and describe what evidence is needed. Do not replace source evidence with a generic citation. Keep the bibliography and generated table notes synchronized with the code.

## References

Reference IDs are stable within this reconstruction package. The [BibTeX library](../references/reconstruction.bib) contains matching citation keys. Institutional data references are located by workbook/sheet/cell or annual archive; access dates do not substitute for release versions and hashes.

<a id="r01"></a>

**R01.** Instituto Nacional de Estadistica y Censos (INEC). Registro Estadistico de Camas y Egresos Hospitalarios: annual microdata and metadata, 2015-2024. Quito: INEC. Accessed 6 November 2026. [Primary source](https://www.ecuadorencifras.gob.ec/camas-y-egresos-hospitalarios/).

Source locator and scope: Use the exact annual archive URLs and SHA-256 hashes in provenance/inec_download_manifest.csv; annual variable/value labels are preserved in provenance/t02/YYYY_schema.json. The current landing page alone does not identify all historical versions.

<a id="r02"></a>

**R02.** Pan American Health Organization / World Health Organization. International Statistical Classification of Diseases and Related Health Problems, Tenth Revision: Chapter II, Neoplasms, C71. Official Spanish tabular classification. Accessed 6 November 2026. [Primary source](https://ais.paho.org/classifications/Chapters/CAP02.html).

Source locator and scope: The official PAHO tabular text was inspected for C71.0-C71.9. It supports code meanings; it does not prescribe the study's four combined anatomical groups or validate individual diagnoses.

<a id="r03"></a>

**R03.** INEC. Estimaciones y Proyecciones de Poblacion de Ecuador, Revision 2024. Expanded area-residence tabulations, Tabulados_Estimacion_Proyeccion_v2.xlsx, sheet 1.1: national population at 30 June, by sex and single age. Accessed 6 November 2026. [Primary source](https://www.ecuadorencifras.gob.ec/proyecciones-poblacionales/). [Exact workbook](https://www.ecuadorencifras.gob.ec/documentos/web-inec/Poblacion_y_Demografia/Proyecciones_Poblacionales/censo_2022/revision_2024_areas/Tabulados_Estimacion_Proyeccion_v2.xlsx).

Source locator and scope: The landing page confirms the revision and 30 June reference date. Exact workbook version/hash: provenance/t03/population_manifest.csv; extracted source-cell coordinates: population_single_age.csv.

<a id="r04"></a>

**R04.** INEC. Censo Ecuador 2022: Estructura poblacional. 01_2022_CPV_Estructura_poblacional.xlsx, sheet 3, Total Nacional, single completed ages 0-99 and 100+. Archived workbook verified 6 November 2026. [Primary source](https://www.censoecuador.gob.ec/wp-content/uploads/2024/04/01_2022_CPV_Estructura_poblacional.xlsx).

Source locator and scope: The current web endpoint returned HTTP 403 during bibliographic checking. Evidence was inspected directly in the previously archived, checksum-verified workbook, not inferred from a search snippet. Exact version/hash: population_manifest.csv; cells: census_2022_single_age.csv.

<a id="r05"></a>

**R05.** National Cancer Institute. SEER*Stat Tutorials: Calculating Age-adjusted Rates. Accessed 6 November 2026. [Primary source](https://seer.cancer.gov/seerstat/tutorials/aarates/definition.html).

Source locator and scope: Supports direct standardization as a weighted sum of age-specific rates. SEER's US standard and age groups are not adopted here; the Ecuador census and manuscript-compatible groups are explicit study choices.

<a id="r06"></a>

**R06.** Fay MP, Feuer EJ. Confidence intervals for directly standardized rates: a method based on the gamma distribution. Statistics in Medicine. 1997;16(7):791-801. [Primary source](https://wonder.cdc.gov/controller/pdf/FayFeuerConfidenceIntervals.pdf). DOI: [10.1002/(SICI)1097-0258(19970415)16:7<791::AID-SIM500>3.0.CO;2-#](https://doi.org/10.1002/(SICI)1097-0258(19970415)16:7%3C791::AID-SIM500%3E3.0.CO;2-%23).

Source locator and scope: Original paper inspected, especially the weighted-Poisson construction. Supports the implemented gamma interval; it does not establish independence of repeated hospital admissions.

<a id="r07"></a>

**R07.** Wilson EB. Probable inference, the law of succession, and statistical inference. Journal of the American Statistical Association. 1927;22(158):209-212. [Primary source](https://jhanley.biostat.mcgill.ca/c607/ch08/wilson_jasa_1927.pdf). DOI: [10.1080/01621459.1927.10502953](https://doi.org/10.1080/01621459.1927.10502953).

Source locator and scope: Original paper available as a scan hosted by McGill University; publisher DOI page was inaccessible. Supports the score interval used for admission-level proportions.

<a id="r08"></a>

**R08.** Benchimol EI, Smeeth L, Guttmann A, et al.; RECORD Working Committee. The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) Statement. PLoS Medicine. 2015;12(10):e1001885. [Primary source](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1001885). DOI: [10.1371/journal.pmed.1001885](https://doi.org/10.1371/journal.pmed.1001885).

Source locator and scope: Relevant items: 6.1-6.2 (codes/validation), 12.1-12.3 (access/cleaning/linkage), 13.1 (selection), 22.1 (access to protocol/data/code). Reporting guidance is not evidence of clinical validation.

<a id="r09"></a>

**R09.** Vandenbroucke JP, von Elm E, Altman DG, et al.; STROBE Initiative. Strengthening the Reporting of Observational Studies in Epidemiology (STROBE): Explanation and Elaboration. PLoS Medicine. 2007;4(10):e297. [Primary source](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0040297). DOI: [10.1371/journal.pmed.0040297](https://doi.org/10.1371/journal.pmed.0040297).

Source locator and scope: Relevant items: 11 (quantitative-variable groupings), 12(b)/(e) (missing data/sensitivity), 13-14 (flow/missingness), 19-20 (limitations/interpretation). It does not dictate a specific estimator or certify this study's quality.

<a id="r10"></a>

**R10.** Sandve GK, Nekrutenko A, Taylor J, Hovig E. Ten simple rules for reproducible computational research. PLoS Computational Biology. 2013;9(10):e1003285. [Primary source](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285). DOI: [10.1371/journal.pcbi.1003285](https://doi.org/10.1371/journal.pcbi.1003285).

Source locator and scope: Supports scripted workflows, preserved inputs/intermediates, software-version recording and traceable outputs. The optional legacy-comparison command is our implementation of these principles.

<a id="r11"></a>

**R11.** National Institute of Standards and Technology. Secure Hash Standard (SHS). Federal Information Processing Standards Publication 180-4. August 2015. [Primary source](https://csrc.nist.gov/pubs/fips/180-4/upd1/final). DOI: [10.6028/NIST.FIPS.180-4](https://doi.org/10.6028/NIST.FIPS.180-4).

Source locator and scope: Technical source for SHA-256 digests used to detect byte changes. Matching hashes establish file identity against the recorded version, not validity of source data or correctness of scientific results.

<a id="r12"></a>

**R12.** Centers for Disease Control and Prevention. Confidence Intervals. U.S. Cancer Statistics technical notes. Updated 1 June 2026; accessed 6 November 2026. [Primary source](https://www.cdc.gov/united-states-cancer-statistics/technical-notes/confidence-intervals.html).

Source locator and scope: Supports explicit interpretation of model-based rate uncertainty and limitations beyond Poisson variation. Its production interval variant is not used as a substitute for the Fay-Feuer implementation.

