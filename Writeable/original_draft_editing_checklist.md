# Minimal-change editing guide for the original article

Prepared 16 November 2026.

## How to use this guide

Edit a copy of **`tumores encefalo Monica art completo.docx.pdf`**, preserving the original. Locations below use its **22-page PDF pagination**, as recorded in [the original page-by-page review](current_state_review.md), together with section, table and phrase anchors. They are not page numbers in the seven-page T07 replacement document. Word pagination will change as you edit; use the anchors after the first revision. These locations are based on the existing review and evidence ledgers, not a new extraction of the PDF in this editing pass.

**Preservation rule:** keep the original section order, useful transitions, accurate background and supported discussion. Change only sentences whose numbers, definitions, claims or citations conflict with the reconstructed analysis. T07/T08 are sources of verified replacement passages, not instructions to discard the entire original paper. Do not retain an old number simply because its paragraph otherwise reads well.

The supplied SAV, SPV and XLSX files are the complete original package. No missing SAV is being requested. The revised results come from a reconstruction using official annual releases; the original preparation history remains unknown.

## 1. Title page and abstract — PDF pp. 1–2

- [ ] **Title, p. 1:** keep Ecuador and 2015–2024. Replace wording implying population cancer incidence, survival follow-up or all cancer mortality. Suggested title: **“Hospitalizations and in-hospital deaths associated with malignant brain neoplasms in Ecuador, 2015–2024: a nationwide discharge-record analysis.”** Preserve the authors and verified affiliations; supply the missing affiliation 6 after author confirmation.
- [ ] **Abstract objective, p. 2:** retain the hospitalization/in-hospital mortality objective. If anatomy remains an objective, specify that recorded coding detail and anatomical group are separate exploratory questions.
- [ ] **Abstract Methods:** keep retrospective/nationwide wording, repair its grammar, and identify INEC discharge records and C71.0–C71.9. Replace the old multinomial-method sentence with: “Binary logistic models examined death during admission, recorded coding detail and anatomical group in separately defined populations.” Add annual population denominators and the fixed observed 2022 census standard for rates.
- [ ] **Abstract Results:** replace the numerical block in full. Include **10,972 admissions, 963 deaths; admission fatality 8.78% (95% CI 8.26–9.32)**. Mean annual standardized hospitalization rate: **6.611 per 100,000 (6.487–6.737)**; corresponding in-hospital death rate: **0.598 (0.561–0.638)**. These rates use 10,969 resident admissions. If retaining an age-model result, use age ≥80 versus 0–17: **aOR 2.631 (1.864–3.715)** for death. Use [T07 Abstract](t07_manuscript_sections.md#abstract) for the full checked paragraph and optional anatomical estimate.
- [ ] **Abstract Conclusions:** remove coding-accuracy improvement, elimination of unspecified coding, protective older age, stability, and causal pandemic/early-stay explanations. Suggested concise wording: “These estimates describe recorded admissions and deaths during admission. Older age was associated with higher adjusted death odds. Unspecified coding and unresolved repeat-admission dependence limit interpretation.”
- [ ] **Abstract duplication/keywords:** remove repeated AAIMR and length-of-stay sentences. Retain suitable original keywords, but ensure they identify brain neoplasms, hospital discharge data and in-hospital outcomes rather than claiming a study of all CNS cancers.

## 2. Introduction — PDF pp. 3–4

- [ ] **Repeated primary/metastatic paragraph, p. 3:** retain one supported general-context paragraph and remove the duplicate. Add: “This analysis concerns discharge diagnoses coded C71.0–C71.9; the records do not establish histological or molecular classification.” Do not imply that the eligible code range includes metastatic lesions, or that a primary discharge diagnosis proves primary tumour origin.
- [ ] **General disease importance and regional context:** keep original sentences whose source supports the exact claim. Broader CNS evidence can remain as clearly labelled background; it cannot silently define this study’s narrower population. No wholesale replacement of the Introduction is required.
- [ ] **GLOBOCAN paragraph, p. 4:** the numbers **561 new cases and 463 deaths** may stay, described as **estimates** from the archived GLOBOCAN 2024 v1.0 Ecuador fact sheet. Replace “recorded” and the general homepage citation with the exact fact-sheet reference R18. Use its verified 12 November 2026 access date; the earlier July date does not authenticate the September-labelled artifact. See [T08 evidence ledger](t08_evidence_ledger.md#globocan-edition-and-historical-access).
- [ ] **Novelty sentence (“first”, “unique”, “first decade-long”):** delete the priority claim while retaining the study’s contribution. Suggested wording: “This study provides a reproducible description of C71-coded hospital admissions and in-hospital outcomes in Ecuador over 2015–2024.”
- [ ] **Final objective, p. 4:** preserve its existing service-event focus. Add coding detail/conditional anatomy only if these analyses remain in the paper; ensure the objective matches the revised Results.

Optional source passages: [T08 Introduction](t08_interpretation_sections.md). Its shorter reference list does not mean every omitted original source is invalid.

## 3. Methods — PDF pp. 4–7

Keep the original subsections and valid direct-standardization formulas. Make the following targeted amendments; use the matching headings in [T07 Methods](t07_manuscript_sections.md) for full wording.

| Done | Original location/anchor | Required edit |
|---|---|---|
| [ ] | p. 4, design/data source | Specify retrospective repeated cross-sectional discharge-record analysis, INEC annual releases, discharge years 2015–2024 and archived source versions/manifests. National scope does not prove complete capture. State that the analysis was reconstructed from official releases. |
| [ ] | p. 4, inclusion/cleaning | State exact normalized C710–C719 eligibility; retain all ten years. Include the final 10,972 records and a supplementary selection flow. Do not claim patient deduplication or repeat-admission removal. Keep the existing warning that repeat admissions cannot be identified. |
| [ ] | p. 4, analysis population | Distinguish all-admission descriptive/models (10,972), resident rates (10,969; three foreign live discharges excluded), and verified rural/urban comparisons (2018–2024, 7,621). |
| [ ] | pp. 4–5, outcome definition | Explicit death=1 for source discharge codes 2/3; live=0 for code 1. Endpoint is death during that admission, without postdischarge follow-up. |
| [ ] | pp. 4–5, anatomical groups | State C710–C714 supratentorial; C715–C717 operational infratentorial/midline; C718 overlapping; C719 unspecified. Acknowledge C715 is not universally infratentorial and describe its exclusion sensitivity. |
| [ ] | p. 5, age/stay/ethnicity | Account for recorded age units. Keep five age groups with explicit bounds. Correct final stay category to **31+ days**, with 15–30 immediately before it. Distinguish source unknown ethnicity (1,290 records) from missing values and Other. |
| [ ] | pp. 5–6, denominators/standardization | Add annual INEC Revisión 2024 midyear estimates and observed 2022 census weights; census standard total 16,938,986. Annual denominators differ by year. Give weights or a supplementary table. Retain the correctly stated distinction between population-denominator rates and admission fatality. |
| [ ] | pp. 5–6, rate summaries/uncertainty | Define the mean as the arithmetic mean of ten annual rates. Add Fay–Feuer intervals, Wilson fatality intervals and narrower-age-band sensitivity. State fixed-denominator/independent-event assumptions. Do not average annual CI endpoints. |
| [ ] | p. 5, mortality regression | Replace the old model specification: death outcome; age, sex, ethnicity, sector, anatomy and categorical year; references documented in Table 4. **Exclude final length of stay and provisional early rural/urban labels from the primary model.** Describe relevant sensitivity models separately. |
| [ ] | p. 5, multinomial regression | Replace this subsection completely with two binary models: non-C719 versus C719 (10,972 records), then infratentorial/midline versus supratentorial (6,192 selected records). Both primary models adjust for age, sex, sector and year; age reference 18–44. Report aORs, not aRRRs. |
| [ ] | pp. 5–7, statistical tests | Align with rebuilt table legends: actual Pearson/Fisher/Monte Carlo procedures, appropriate denominators, sparse flags and model diagnostics. Use “multivariable” for multiple predictors. Do not claim all categorical tests used the same method. |
| [ ] | Methods, reproducibility paragraph | Identify the actual Python analysis and recorded versions; remove any claim that the rebuilt results were produced solely in SPSS. Original SPSS files are historical evidence. Add final code/data access wording once its destination is verified. |
| [ ] | Methods, geography | Identify **province of residence** for the main figure and **facility province** for the separate supplement. Counts are admissions, without provincial population denominators. |
| [ ] | p. 7, ethics | Preserve only statements supported by an actual institutional determination or applicable documented basis. Author must confirm ethics/exemption, consent requirements and any identifier. Do not retain “no potential risk” or an unverified CEISH-INSPI determination as established fact. |

The Methods must describe the executed reconstruction, even where this requires more change than elsewhere. Detailed source inventories, diagnostic tables and full sensitivity output can go in supplementary material to preserve a readable main text.

## 4. Results and tables — PDF pp. 7–16

Preserve the original descriptive → temporal rates → adjusted associations sequence. **Replace every numerical table in full**, including its title and footnotes, rather than patching selected cells. The rebuilt cohort changes denominators and comparisons throughout.

| Done | Original location/anchor | What to insert/change | Authoritative replacement |
|---|---|---|---|
| [ ] | p. 7, opening descriptive paragraph | 10,972 admissions, 10,009 live discharges, 963 deaths. Change patient/case counts to admission/discharge counts. Recalculate every percentage from the stated denominator. | [T06 report](t06_descriptive_tables.md), rebuilt Table 1 |
| [ ] | p. 7, rural/public-sector comparisons | Remove any interpretation of percentages within death/live columns as rural/urban fatality or hospital performance. Restrict rural/urban comparisons to verified 2018–2024. | Table 1 scope/denominator notes |
| [ ] | Table 1, p. 8 onward | Replace all counts, percentages, tests and legends. In particular 2023 = **1,095 admissions/101 deaths/994 live**; 2024 = **1,019/87/932**. | `outputs/tables/table1_rebuilt.md` |
| [ ] | Table 2, anatomical descriptive block | Replace the entire table and its test footnote; preserve original descriptive purpose. C719 totals **4,668**; 2024 C719 remains **379**. | `outputs/tables/table2_rebuilt.md` |
| [ ] | pp. 11–12, Table 3/rate narrative | Replace all annual rates, means, ranges and extrema. Include uncertainty. Remove exclusion of “anomalous” 2017/2023 and the all-death-2023 explanation. | `outputs/tables/table3_rebuilt.md`; [T03 report](t03_rates_and_methods.md) |
| [ ] | pp. 11–12, temporal highlights | Total AAHR peaks in **2017: 7.582913**; lowest **2020: 5.540394**. Total in-hospital death rate peaks **2017: 0.758166**; lowest **2020: 0.453874**. 2024 total AAHR **5.783973**; unspecified **2.152234**. Supratentorial peak **2019: 3.469736**. All are per 100,000 residents. Round consistently in prose. | T03 primary resident/five-band outputs |
| [ ] | p. 13, mortality interpretation and Table 4 | Replace model narrative and table, not just reciprocal ORs. Age ≥80 versus 0–17: **2.631 (1.864–3.715)**, higher adjusted death odds. 2023 versus 2015: **1.034 (0.768–1.391)**. Remove invalid 0.001 estimate and incomplete interval. | `outputs/tables/table4_rebuilt.md`; [T04 report](t04_mortality_analysis.md) |
| [ ] | Table 4 title/notes | Remove repeated title, mixed-language labels and “schizophrenia classification” footnote. Use the complete rebuilt legend, references, sample size and sparse flags. | T06 Table 4 presentation |
| [ ] | Table 5 and corresponding anatomy paragraphs, following Table 4 | Replace with two panels, correctly labelled populations/events/references. For conditional anatomy, pediatric versus 18–44 aOR **1.141 (0.985–1.320)**; do not retain the old pediatric aRRR or its age reference. Report period sensitivity without selecting a preferred fit. | `outputs/tables/table5_rebuilt.md`; [T05 report](t05_anatomy_analysis.md) |
| [ ] | End of regression Results | Add a short sensitivity paragraph: resident-only results, time restrictions, verified residence subset, sparse profile intervals and coding/site sensitivities as relevant. Avoid exhaustive repetition of every coefficient. | T04/T05 sensitivity sections and CSVs |

Generated `outputs/tables/` files are intentionally ignored by Git. If absent on another workstation, regenerate using [README_REPRODUCTION.md](../README_REPRODUCTION.md); do not fill gaps from the old manuscript.

## 5. Figures and geographical Results — PDF pp. 12–18, anchored by Figure 1/2

- [ ] **Figure 1:** replace the entire old image with `outputs/figures/figure1_rates.pdf` (SVG/PNG alternatives available). Its values match rebuilt Table 3; do not manually modify the old curves. Replace its caption using [T09 Figure 1 legend](t09_figure_legends.md#figure-1).
- [ ] **Figure 2 and geographic text, pp. 17–18:** use the rebuilt residence-count heatmap `figure2_residence_counts.pdf`. Keep descriptive geographic organization, but update every province/year count and remove elevated disease-risk/access/complexity inferences. State 10,969 resident admissions and three foreign exclusions.
- [ ] **If retaining the original map presentation is important:** the rebuilt annual maps are available in `figureS1_residence_atlas.pdf`. They can be promoted to the main figure after agreeing space/layout; move or renumber the heatmap consistently. Reuse verified data and legends, not the original map artwork. The ten-page atlas will usually fit better as a supplement.
- [ ] **Supplementary facility comparison:** identify `figureS2_facility_counts.pdf` explicitly as treating-facility province, n=10,972; do not switch residence and facility assignment mid-paragraph.
- [ ] **All captions:** preserve admission-count wording, scale, exclusions and source attribution. For maps include fixed boundary source/year/licence and the different Galápagos inset scale. Inspect labels again at the chosen journal size.

## 6. Discussion — PDF pp. 19–20

Keep the original paragraph order and useful context. Apply sentence-level edits below; verified alternative paragraphs are in [T08 Discussion](t08_interpretation_sections.md).

| Done | Find this topic/claim | Keep | Change |
|---|---|---|---|
| [ ] | Opening summary | A concise statement of the study question and principal findings | Replace all old totals/rates and describe reconstructed discharge records. Avoid restating every table. |
| [ ] | “Stable” burden or equal groups | Descriptive account of year-to-year variation | Remove stability/equivalence conclusions; no formal test established them. |
| [ ] | COVID, delayed imaging, deferred surgery, emergency prioritization | Observation that 2020 was the lowest rate year | Delete asserted mechanisms. Optional hypothesis: “These data cannot distinguish changes in presentation, admission practice, care availability or recording.” Do not state these occurred as demonstrated facts. |
| [ ] | 2017/2023 “capture disruptions”, “anomalies”, registry failure | A short acknowledgement of administrative-data limitations | Remove year-specific failure explanations; they were based on the historical extract and were not reproduced. |
| [ ] | Older age interpreted as protective | General discussion of age and admission case mix | Replace with the verified higher death-odds association; avoid causal attribution. |
| [ ] | Prolonged stay / acute early-stay mortality | Existing warning about outcome-dependent stay duration and reverse causation | Remove protective/harmful causal inference and unsupported early-stay mechanism. Final LOS is only a descriptive sensitivity. |
| [ ] | Public sector / tertiary complexity / access barriers | Cautious discussion that care populations may differ | Report the adjusted association without equating it with quality, access or severity; these were not adequately measured. |
| [ ] | Coding “precision”, “accuracy”, “elimination” or structural improvement | Concern about documentation and unspecified codes | State **4,668 unspecified records (42.54%)**, including 379 in 2024. Coding detail is not clinical accuracy. |
| [ ] | Pediatric site preference / ethnicity propensity | Properly bounded comparison with supported literature | Replace the old multinomial finding with the conditional binary estimate and period sensitivity; make the selected-population limitation explicit. |
| [ ] | International rate comparisons, including 3.5–6 or 7–11.5 ranges | General context if its citation supports the sentence | Remove numerical comparisons between hospital-event rates and cancer incidence/all-cancer mortality. A comparator can stay only after endpoint, code range and standard population are verified as comparable. |
| [ ] | “First”/unique national study | The contribution of a reproducible decade-long description | Remove unsupported priority claim. |

## 7. Limitations and conclusion — PDF pp. 20–21

Keep the existing repeat-admission and reverse-causation limitations. Expand them only where needed:

- [ ] Add inability to identify patient/facility clustering; reported intervals condition on independent records and may understate uncertainty.
- [ ] Add no histology/grade/clinical validation, incomplete severity/treatment/comorbidity adjustment, admission selection and no postdischarge follow-up.
- [ ] State early rural/urban labels remain unverified and are excluded from all-year adjustment; do not imply province coding has the same unresolved mapping.
- [ ] State model comparisons are exploratory, sparse categories have wide intervals, and conditional-site analysis excludes unspecified/overlapping codes without correcting selection.
- [ ] Explain that rate uncertainty conditions on fixed population denominators and standard weights; it does not capture underregistration or miscoding.
- [ ] **Conclusion:** preserve its short structure and corrected rejection of a diagnostic/surgical 1–3-day window. Replace incompatible findings and remove coding elimination, causal care claims and incidence framing. Suggested core: “C71-coded admissions in Ecuador during 2015–2024 describe hospital service activity and deaths during admission. Older age was associated with higher adjusted death odds, while frequent unspecified coding and period-sensitive anatomical associations limit interpretation. These data do not estimate cancer incidence or overall cancer mortality.”

## 8. Citations, declarations and final editorial pass — PDF pp. 21–22 and throughout

- [ ] **Keep original references where you retain their supported claims.** “Not retained in T08” means unused in that replacement, not demonstrated false. For each restored sentence, verify that the cited source supports the exact claim; otherwise narrow or remove the sentence.
- [ ] Merge duplicate original references **5 and 13** into one CBTRUS identity if still cited, then renumber all citations.
- [ ] Use original reference **14** for WHO classification only; remove it from COVID-disruption claims. Original reference **15** does not establish Ecuador emergency prioritization. Reference **16** is not automatically a hospitalization benchmark. Reference **20** does not establish Ecuador registry failure.
- [ ] Cite the exact IARC fact sheet, annual INEC sources, denominator/census sources and statistical methods actually used. Source IDs R01–R22 in working files must become the final journal citation format; do not leave internal R-codes unresolved.
- [ ] Obtain factual funding, conflicts, contributions, ethics/consent and availability declarations. Keep verified author information; do not infer “none” from silence.
- [ ] Replace “patients/cases” with “admissions/discharges” where the numerical unit is a record. Do not globally replace legitimate background references to patients.
- [ ] Use adjusted odds ratios consistently; do not call them relative risks, causal risk factors or survival probabilities.
- [ ] Use full precision for calculations and consistent display rounding. Report `<0.001` only when the actual p-value warrants it; use the rebuilt tables’ formatting.
- [ ] Match every figure/table number and caption to its in-text callout after any main/supplement swaps.

## When redaction can be considered closed

- [ ] All mandatory numerical/method/interpretation edits above are applied to one manuscript copy.
- [ ] Abstract, Results, Discussion and Conclusion use the same populations, endpoints and values; every number is traceable to T02–T09 evidence.
- [ ] All five old tables and both old figures have been replaced or explicitly removed with corresponding text changes.
- [ ] Every retained background/comparison claim has an appropriate citation; unused references and duplicates are removed.
- [ ] A coauthor has reviewed the revised estimands, sensitivity results and limitations.
- [ ] Author declarations and affiliations are factually confirmed; unresolved author items are clearly marked until resolved.
- [ ] One full read-through checks grammar, repetition, abbreviations, numbering and final rendered table/figure readability.
- [ ] The reporting crosswalk is updated to the **integrated manuscript’s** sections/pages, rather than the old T07 pagination.

Completing these edits closes the writing/integration work. Clean-workstation reproduction and the remaining T10 journal/submission checks are separate release requirements, tracked in [the prewriting audit](prewriting_repository_audit.md). Passing tests alone does not close manuscript editing.
