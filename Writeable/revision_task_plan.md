# Manuscript revision task plan

Prepared 23 October 2026. Companion evidence: `current_state_review.md`. Preserve `review_issues.md` as the original review record. This plan covers all original issues 1–22 and new findings N01–N15. It specifies future work; no data corrections or model refits have yet been completed.

**Recommended order: establish trustworthy data → rebuild rates and models → rewrite findings → prepare submission.** Do not retain a result because it supports the present narrative. If data or models cannot be validated, narrow the paper to defensible descriptive analyses and revise its scope accordingly.

Priorities: P0 = blocks reliable results; P1 = major scientific/reporting revision; P2 = presentation/submission. Owners are suggested roles, not assignments to specific people. Effort estimates are working days and exclude waiting for external files, ethics determinations or coauthor responses.

## T01 — Freeze inputs and build a reproducibility workspace

- [x] **Workspace completed 23 October 2026; provenance gaps explicitly recorded.** See `../provenance/README.md`, `../provenance/input_manifest.csv` and `../provenance/artifact_lineage.csv`. Six input snapshots verified; editable manuscript and original derivation history are unavailable.
- **P0 · analyst + lead author · 0.5–1 day · no dependencies.**
- Preserve the reviewed PDF, original review, SAV, both workbooks and SPV output with version/date and checksums. Identify which workbook is analytic versus plotting data and how each was produced. Obtain the editable manuscript source if available.
- Create an input manifest, a variable dictionary and an issue-resolution log with columns: issue ID, evidence, decision, changed files, validation, owner, status.
- Keep original national files immutable; use scripts or saved SPSS syntax for transformations and output generation. Record software versions.
- **Deliverable:** input manifest and reproducible project skeleton.
- **Done when:** every manuscript table/figure has an identified data source and generation route; unknown provenance is explicitly listed.
- **Covers:** N09; enables every original issue.

## T02 — Reconstruct and audit the analytic admissions

- [ ] **P0 · data analyst + INEC/data custodian as needed · 2–4 days · after T01.**
- Obtain original annual INEC discharge files and year-specific dictionaries for 2015–2024. Record file dates/releases, coverage and annual source row counts.
- Implement documented primary-discharge C71.0–C71.9 selection, accounting for punctuation, labels, whitespace and year-specific coding. Inspect filters, joins, dropped records and missing discharge outcomes. Distinguish exact duplicated records from legitimate repeat admissions; never infer patient identity from demographic similarities.
- Produce a per-year selection flow: source records → diagnosis-eligible → exclusions by reason → final admissions; tabulate death/live/unknown outcome by year and C71 category.
- **Audit 2017 and 2023 first:** identify why only 31 and 83 admissions appear, and why all 83 in 2023 are deaths. Compare the supplied analytic files to national source records. Do not label anomalies administrative until there is evidence of the mechanism.
- **Audit 2024:** reconcile Table 1’s 980 admissions with Table 2’s 1,007 and verify its 379 unspecified admissions. Investigate the zero C71.9 hospitalization rate as a separate rate/plot pipeline issue.
- Recode age explicitly, checking age units and unknown codes. Recode LOS using mutually exclusive bounds grounded in the actual data; resolve day 30, same-day stays, negative values and missing values. Replace unsafe ELSE catch-all logic with explicit valid ranges and unknown categories.
- Tabulate missingness and invalid values by variable and year; decide transparent exclusion/imputation/unknown-category rules appropriate to each variable. Do not indiscriminately impute structural missingness or unknown outcomes.
- Define province (residence/facility), sector, ethnicity and geography coding. Verify changes over time and whether institution identifiers exist.
- **Deliverables:** clean admission-level extract, dictionary, flow table, year-quality audit and decision log.
- **Done when:** annual totals reconcile across outcomes and anatomy; all discrepancies have a documented cause; categories are mutually exclusive; unknowns and exclusions are counted.
- **Covers:** original 5, 6, 9, 11, 17, 18, 20; N03, N05, N06, N09, N11.
- **Decision rule:** correct extraction/coding errors first. If a year remains unverifiably incomplete, document a justified primary-analysis inclusion policy and report sensitivity results. Do not silently delete 2017/2023 or treat their observed counts as complete population capture.

## T03 — Rebuild every rate and uncertainty estimate

- [ ] **P0 · epidemiologist/statistician · 1–2 days · after T02.**
- Archive annual Ecuador population denominators by age, their source/revision and the 2022 standard weights. Verify common age categories and weights summing to one.
- Compute annual age-specific admission and death rates, then standardize both using the same weights. Separate annual population denominators from the fixed standard population. Assess whether narrower age groups are feasible.
- Recalculate each anatomical component, annual total and 10-year summary from full-precision values. Define arithmetic mean of annual standardized rates versus any pooled summary; label whichever is used.
- Compute admission-based fatality separately. Add suitable confidence intervals to key rates and proportions, with their method and assumptions, including limitations from repeat admissions.
- Recalculate the share of mortality attributed to anatomical groups and all maxima/minima; remove stale 87% and peak claims unless reproduced.
- **Deliverables:** machine-readable annual rate table, denominator/weight appendix, uncertainty method and generated Table 3.
- **Done when:** total standardized rates equal summed anatomical components before rounding; each death component is no greater than its admission component under the same denominators; all published means reproduce; rounding differences are bounded. No ad hoc decimal corrections.
- **Covers:** original 7, 8, 18, 19, 20, 21; N04, N05, N09, N15.

## T04 — Repair and validate the mortality analysis

- [ ] **P0 · statistician + clinical coauthor · 2–3 days · after T02; agree analysis specification before refitting.**
- Open/export the SPSS dependent-variable encoding, warning and model-summary tables. Reconcile those outputs to the manuscript version.
- Create and validate an explicit numeric event `death=1`, `alive=0`, with unknown outcomes excluded or otherwise handled transparently. Cross-tabulate against original labels and compute simple crude odds ratios to verify event/reference directions.
- Specify the objective as association with death during an included admission. Distinguish causal explanation, association and prediction; the current study does not establish a clinical prediction tool.
- For the primary association model, use justified admission-time covariates. Remove final LOS as a purported baseline risk factor. If retained in a secondary model, label it descriptive and explain its outcome-dependent timing. Do not add survival analysis without valid dates and an explicit treatment of discharge alive as a competing event.
- Check separation, convergence, sparse levels, coefficient stability, model sample size/events and plausible coding. Reconsider tiny reference groups rather than retaining them automatically. Address facility clustering if supported; acknowledge inability to cluster repeated admissions by person when identifiers are absent.
- Fit an appropriate valid model. If separation persists in verified records, consider bias-reduced/Firth binary logistic regression with suitable intervals; document software and fit diagnostics. Neither penalization nor more iterations repairs a biased sample.
- Compare corrected all-year results with justified year-exclusion sensitivity analyses and models without LOS. Report what changes and why. Reassess age effects after outcome direction and selection are resolved.
- **Deliverables:** analysis specification, converged model output, diagnostics, sensitivity table and regenerated Table 4.
- **Done when:** death event and references are proven; no unresolved convergence/separation warning is concealed; estimates are reproducible with valid uncertainty; conclusions follow the corrected event direction. If stable estimation is impossible, remove the regression claims and state the limitation.
- **Covers:** original 12, 13, 14, 15, 16; N01, N02, N06, N09, N10.

## T05 — Decide whether the multinomial analysis answers a defensible question

- [ ] **P0/P1 · statistician + clinical coauthor · 1–2 days · after T02.**
- Clarify whether the scientific question concerns recorded coding specificity, anatomical distribution among specified diagnoses, or their mixture. State the population and reference outcome.
- Review the saved Hessian warning, sparse ethnic groups and zero overlapping-lesion cells. Count observations in every outcome/predictor combination and report model sample size.
- Choose among: a simpler clinically justified model; a suitable penalized multinomial approach; separate specified/unspecified and specified-site analyses; or descriptive presentation if inference is unsupported. Do not merge ethnic groups solely to obtain significance, or apply a binary Firth procedure directly to an unchanged multinomial outcome.
- Verify all predictor and outcome reference levels, including pediatric versus ≥80 years. Reconsider LOS as an explanatory variable for anatomy, which predates the observed stay.
- Explain aRRRs as ratios comparing outcome-category probabilities against a reference among included admissions, not population cancer risks. Report non-estimable cells without misleading p-values.
- **Deliverables:** documented model decision, valid output/diagnostics or descriptive alternative, revised Table 5.
- **Done when:** the scientific interpretation matches the model, instability is addressed, and every estimate/absence is explained. A footnote alone does not cure an invalid fit.
- **Covers:** original 22; N02, N08, N09, N10.

## T06 — Regenerate descriptive tables and statistical footnotes

- [ ] **P1 · analyst · 0.5–1 day · after T02; coordinate with T04/T05.**
- Generate Tables 1–2 directly from the validated extract. Specify row versus column percentages; report actual within-group fatality if mortality comparisons are discussed.
- Verify counts across every characteristic, denominators for missing values, and year totals. Repair the 2024 alive percentage through regeneration.
- Recalculate tests and identify which comparisons use chi-square versus exact/Monte Carlo methods where appropriate. Record actual p-value precision; never replace all small values by exactly 0.001.
- For Tables 4–5, state event/outcome, all included covariates, model N/events, reference categories, model type and interval method. Remove the schizophrenia footnote and unsupported significance highlighting.
- **Deliverables:** generated tables with self-contained legends.
- **Done when:** a reader can recover each percentage denominator and understand each model without guessing; table text matches executed code.
- **Covers:** original 6, 16, 22; N03, N07, N14.

## T07 — Rewrite Methods, abstract and study framing from validated results

- [ ] **P1 · lead author + epidemiologist · 1–2 days · after T02–T06 for result-dependent text.**
- Suggested working title: **Hospitalizations and In-Hospital Deaths Associated With Malignant Brain Neoplasms in Ecuador, 2015–2024: A Nationwide Analysis of Discharge Records.** Retain “primary” only with a clearly explained coded-diagnosis scope; avoid suggesting histological verification.
- Retain the improved hospitalization/in-hospital mortality objective and explicit admission-level unit. Explain limitations in national capture and repeat admissions.
- Make terminology consistent: malignant brain neoplasms coded C71; admissions/discharges as observations; case-fatality proportion with an admission denominator; population-denominator in-hospital death rate distinct from overall cancer mortality.
- Report complete data provenance, flow, coding, missingness, population denominators, standardization and model decisions. Complete STROBE and relevant RECORD items with page references rather than an unsupported blanket compliance statement.
- Rewrite abstract once: design, verified admission/death totals, key estimates with uncertainty, defensible interpretation and limitations. Remove duplicate phrases and causal/survival claims not established by the analysis.
- Keep original corrections that are already sound; do not restore patient-level deduplication claims or diagnostic/surgical-window language.
- **Deliverables:** revised title, abstract, Methods and checklist crosswalk.
- **Done when:** original issues 1–8 are consistently addressed across the entire paper and every abstract number is traceable to a validated output.
- **Covers:** original 1–8, 9, 14, 15; N04, N09, N14.

## T08 — Rebuild interpretation, limitations and evidence base

- [ ] **P1 · lead author + clinical coauthor · 1–2 days · literature audit can start after T01; conclusions wait for T03–T05.**
- Create a claim-to-source ledger. Verify every reference supports the attached statement, remove duplicate references, clean DOI fields, and archive the exact GLOBOCAN edition and estimates.
- Compare hospitalization rates only with genuinely comparable hospitalization measures, cancer definitions and age standards. Clearly distinguish incidence, disease mortality and discharge outcomes.
- Remove unvalidated improvement in coding accuracy, emergency-care prioritization, diagnostic/surgical timing and institutional complexity claims. A change in unspecified coding is not proof of diagnostic accuracy.
- Describe COVID timing as an observation; present mechanisms as hypotheses with appropriate sources. Give neutral descriptions of suspect years unless the audit identifies their cause.
- Address selection into admission, repeated admissions, out-of-hospital deaths, missing clinical severity, classification error, coding changes, temporal completeness and residual confounding.
- Decide whether rates are merely described or formally tested for trends; report uncertainty and avoid an unsupported assertion of stability. No causal COVID claim from a single before/after contrast.
- Verify the “first” claim through a documented literature search or remove it. State what this analysis adds beyond existing Ecuador and regional studies without overselling anatomical patterns already well known.
- **Deliverables:** evidence ledger and rewritten Introduction/Discussion/Conclusion.
- **Done when:** every major claim is either supported by the corrected analysis, supported by an appropriate source, clearly marked as a hypothesis, or removed.
- **Covers:** original 4, 9–15; N07, N10, N12, N15.

## T09 — Rebuild figures and geographic reporting

- [ ] **P1/P2 · analyst + figure author · 0.5–1 day · after T02/T03.**
- Regenerate Figure 1 from the exact rate table used for Table 3. Check 2017 mortality and 2024 total/unspecified series explicitly; include uncertainty if readable or provide it in a companion table.
- Define residence versus treating-facility province. Use “admission counts” for count maps; do not imply incidence/risk. Add resident-population rates only if the geographic numerator/denominator match and the question warrants them.
- Regenerate Figure 2, clarify incomplete years and distinguish zero from missing. Retain a comparable scale across years; improve label sizes or move detailed maps to a supplement.
- State boundary source, geographic assignment and relevant exclusions. Export publication-quality/vector figures where possible and inspect at intended journal dimensions.
- **Deliverables:** verified Figures 1–2 and complete legends.
- **Done when:** every plotted number matches source outputs; geography is interpretable; labels are readable at publication size.
- **Covers:** original 6, 20, 21; N04, N11.

## T10 — Ethics, journal fit and final submission audit

- [ ] **P1/P2 · lead author + all coauthors · 1–2 days plus external waiting · after substantive revisions; ethics verification can begin immediately.**
- Confirm and accurately document the applicable ethics review/exemption basis, public-data provenance and consent status. Include an identifier only if one exists.
- Add funding, conflicts, author contributions and data/code availability. Explain access restrictions where applicable rather than promising unrestricted sharing of all records.
- Select a target journal based on scope, article type, methodological expectations and genuine contribution. Verify its current quartile using the chosen database, subject category and year; no journal has been assessed or promised Q1 status in this review.
- Check word/figure limits, required checklists and reporting format. Fix affiliation 6, repeated text, table title, mixed languages and terminology; perform professional scientific-language editing after the analysis is stable.
- Conduct a final consistency audit of abstract, Results, Discussion, tables, figures and supplement. Have a coauthor independently verify event coding, the 2023 decision, 2024 counts, rates and model diagnostics.
- **Deliverables:** submission-ready manuscript, supplementary methods/code, checklists and completed issue-resolution log.
- **Done when:** no P0 issue remains; every original and new issue has evidence of resolution or an explicitly justified change of scope; all authors approve the final interpretation.
- **Covers:** N13/N14 and final verification of all issues.

## Sequence and decision gates

| Gate | Required evidence | Work permitted next |
|---|---|---|
| G1: data accepted | T01–T02 complete; year/age/LOS/outcome discrepancies explained | Final rates and model refits |
| G2: results accepted | T03–T06 complete; consistent rates, correct event direction, valid models or justified descriptive alternative | Final abstract, Results and causal/clinical interpretation |
| G3: manuscript accepted | T07–T09 complete; claims and sources aligned | Journal formatting and submission preparation |
| G4: ready to submit | T10 complete; coauthor verification and complete issue log | Submission decision |

Indicative effort is approximately **11–20 person-days**, with overlapping literature, ethics and documentation work where appropriate. Data-source reconstruction or external determinations may lengthen elapsed time. Do not set a submission date before G1 establishes whether the current research scope is supportable.

## Full coverage check

| Original issue | Tasks | Original issue | Tasks |
|---|---|---|---|
| 1 | T07 | 12 | T04, T08 |
| 2 | T07 | 13 | T04, T08 |
| 3 | T02, T07 | 14 | T04, T07, T08 |
| 4 | T07, T08 | 15 | T04, T07, T08 |
| 5 | T02, T07 | 16 | T02, T04, T06 |
| 6 | T02, T06, T07, T09 | 17 | T02 |
| 7 | T03, T07 | 18 | T02, T03 |
| 8 | T03, T07 | 19 | T03 |
| 9 | T02, T07, T08 | 20 | T02, T03, T09 |
| 10 | T08 | 21 | T03, T09 |
| 11 | T02, T03, T08 | 22 | T05, T06 |

| New finding | Tasks |
|---|---|
| N01 outcome direction | T04 |
| N02 invalid model fits | T04, T05 |
| N03 counts/percentages | T02, T06 |
| N04 stale means/extrema | T03, T07, T09 |
| N05 death/admission rate contradiction | T02, T03 |
| N06 age/LOS recoding | T02, T04 |
| N07 denominator interpretation | T06, T08 |
| N08 anatomy versus coding model | T05 |
| N09 reproducibility/missingness | T01–T05, T07 |
| N10 dependence/confounding | T04, T05, T08 |
| N11 geography/figures | T02, T09 |
| N12 sources/novelty | T08 |
| N13 ethics/declarations | T10 |
| N14 editorial/reporting | T06, T07, T10 |
| N15 trends/uncertainty | T03, T08 |
