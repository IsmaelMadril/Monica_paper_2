# T08 claim and reference evidence ledger

Prepared 12 November 2026. This ledger covers the replacement Introduction, Discussion and Conclusion in `t08_interpretation_sections.md`, not a retroactive validation of the reviewed PDF. Exact numeric values and row locators are in `../provenance/t08/numeric_traceability.json`; the full machine-readable claim and reference dispositions are also tracked there.

## Claim decisions

The anchor identifies a paragraph or removed historical assertion. External findings, local results, analytical interpretations and untested explanations are distinguished. No unsupported factual mechanism is retained. Source IDs R01–R20 resolve in `reconstruction_rationale.md` and `../references/reconstruction.bib`.

| ID | Paragraph or historical claim | Evidence type | Support and decision | Limits |
|---|---|---|---|---|
| I01 | Malignant brain neoplasm discharge codes | supported external context | R02; R19. Distinguish site-coded administrative diagnoses from integrated tumour classification. | No claim of histological verification of study records. |
| I02 | For Ecuador, the archived GLOBOCAN | supported external estimate | R18; provenance/t08/globocan_snapshot.json. 561 cases/463 deaths retained as 2024 estimates v1.0; exact PDF, page and hash archived. | Modelled estimates, not recorded hospital events; historical July access not reconstructed. |
| I03 | Regional work has described | supported external methods | R20. Only registry-incidence/WHO mortality/world-standardization methods stated in authors abstract are retained. | Abstract-only access; no numerical hospital comparison or Ecuador-specific finding inferred. |
| I04 | We analyzed annual INEC | study objective and contribution | R01; provenance/t02/selection_flow.csv; provenance/t04/analysis_specification.md; provenance/t05/analysis_specification.md. Describe auditability and service-event question. | No first/unique claim or complete population cancer coverage. |
| D01 | The reconstructed analysis included | supported local result | provenance/t03/period_summary_rates.csv; provenance/t03/admission_fatality.csv; provenance/t07/numeric_traceability.json. All-admission fatality and resident-population rate summaries use different explicit denominators. | Gamma/Wilson intervals omit systematic error and dependence. |
| D02 | These service-event estimates should | analytical interpretation | R18; R20; Writeable/t03_rates_and_methods.md. Explain noncomparability of admissions, cancer incidence and disease mortality. | Do not divide the two mortality measures to infer a hospital capture fraction. |
| D03 | The resident hospitalization rate was | local observation plus untested hypotheses | provenance/t03/annual_standardized_rates.csv. Report 2019/2020 rates and intervals; temporal coincidence only. | No causal COVID estimate. Potential admission/case-mix/recording explanations explicitly unmeasured; no external source offered as proof. |
| D04 | The reconstructed official releases contained | supported local correction | provenance/t02/selection_flow.csv; provenance/t02/annual_counts.csv. Retain reconstructed 2017 and 2023; historical low counts not reproduced. | No identified historical loss mechanism; official completeness not proven. |
| D05 | Rates are described with model-based | executed analysis policy | provenance/t03/run_metadata.json; provenance/t06/analysis_specification.md. Descriptive temporal series; no trend, stability or COVID intervention claim. | Non-significance is not equivalence or temporal stability. |
| D06 | In the primary death model | supported local result | provenance/t04/all_model_coefficients.csv; provenance/t04/legacy_encoding.json; provenance/t04/legacy_model_evidence.md. Age80+ odds direction corrected; original event was live discharge and original fit failed. | No prognostic prediction, causal age effect or reciprocal repair of failed model. |
| D07 | Public versus private sector had | local result plus bias interpretation | provenance/t04/all_model_coefficients.csv; provenance/t04/analysis_specification.md. Report adjusted odds with uncertainty; do not infer performance/tertiary complexity or access. | Unmeasured severity/referral and selection remain possible; final LOS is postadmission. |
| D08 | Unspecified C71.9 coding remained | supported local result | provenance/t05/anatomy_descriptive.csv; provenance/t03/annual_standardized_rates.csv; provenance/t05/all_model_coefficients.csv. Retain C719 counts and nonzero 2024 rate; coding-detail association is not accuracy. | No external chart/pathology validation. |
| D09 | The site comparison excluded | supported local result | provenance/t05/model_flow.csv; provenance/t05/all_model_coefficients.csv. Primary and later-period pediatric contrasts have different periods and must both be described honestly. | No formal interaction test; later-year fit not selected to replace primary. |
| D10 | The conditional-site analysis describes | conditional-estimand interpretation | R02; provenance/t05/analysis_specification.md. State selected coded outcome population and operational C715 grouping. | No new biological pattern, ethnicity propensity or demonstrated selection correction. |
| L01 | The observation is a discharge record. | documented limitation | provenance/t02/duplicate_projection_audit.csv; Writeable/t04_mortality_analysis.md. Repeated records cannot be resolved as people; independent-record precision is conditional. | Direction/magnitude of clustering uncertainty not identified. |
| L02 | The administrative diagnosis was not | documented limitation | R19; provenance/t02/derived_variable_dictionary.csv; provenance/t06/missingness.csv; provenance/t06/table_scopes.csv. Identify unavailable clinical validation/severity and restricted residence labels. | No imputed known ethnicity; no all-decade rural comparison. |
| L03 | Selection into inpatient care limits | documented limitation | R08; provenance/t02/audit_summary.json; Writeable/t03_rates_and_methods.md. Limit applicability to recorded inpatient events; no external follow-up linkage. | Coverage changes possible, not established mechanisms. |
| L04 | Direct standardization improves | conditional statistical interpretation | R03; R04; R05; R06; R07; Writeable/t03_rates_and_methods.md. Standardization and narrower bands address stated age distributions, not all bias. | Fixed denominator/weight assumption; no cumulative risk interpretation. |
| L05 | The death and coding/site models were | local diagnostics plus limitation | provenance/t04/model_diagnostics.json; provenance/t05/model_diagnostics.json. Finite converged models do not prove clinical/causal validity; sparse and multiple exploratory contrasts remain limited. | No significance-selected subgroup conclusion or missing-site correction. |
| L06 | The study provides reproducible | documented contribution and research implication | R08; R09; README_REPRODUCTION.md; provenance/t02/selection_flow.csv. Offer auditability and service-event description; future validation/linkage are research proposals. | No assertion of firstness or specific clinical resource-allocation benefit. |
| C01 | C71-coded admissions in Ecuador during 2015–2024 | summary of supported local results | provenance/t08/numeric_traceability.json; D01; D06; D08; D09. Conclusion restates defined counts/rates/associations and limits. | Template anchor is expanded by the builder; no independent causal or novelty claim. |
| X01 | first decade-long nationwide study | removed | No retained support required. Removed; limited contextual search is not exhaustive and priority is not needed to state the contribution. | Removed from replacement text |
| X02 | coding accuracy improved or unspecified coding eliminated | removed | No retained support required. Removed; C719 persists and clinical accuracy was not validated. | Removed from replacement text |
| X03 | pandemic caused delayed imaging postponed surgery or emergency prioritization | removed | No retained support required. Removed as factual mechanism; timing retained and alternatives explicitly untested. | Removed from replacement text |
| X04 | 2017/2023 national registry failure | removed | No retained support required. Removed; reconstructed official counts contradict the historical deficit premise, without proving completeness. | Removed from replacement text |
| X05 | hospital rates align with 3.5–6 or 7–11.5 cancer incidence ranges | removed | No retained support required. Removed; endpoints/code definitions/standards are not matched. | Removed from replacement text |
| X06 | public tertiary hospitals handle complex tumours and prove access disparities | removed | No retained support required. Removed; facility complexity, severity and access were not established. | Removed from replacement text |
| X07 | prolonged stay protects or establishes surgical diagnostic window | removed | No retained support required. Removed; final stay is not a baseline causal exposure and old outcome/fit were invalid. | Removed from replacement text |
| X08 | stable burden or equal groups because confidence interval contains one | removed | No retained support required. Removed; descriptive rate series and non-significant tests do not establish equivalence or stability. | Removed from replacement text |

## Original reference audit

All 24 original entries were extracted from the reviewed PDF pages 21–22 and preserved in `../provenance/t08/legacy_references_extracted.json`. All are dispositioned below. This is not a claim that every discarded paper was read in full. Only retained references support new text, at the access level stated. DOI cleanup for unused entries is syntactic only unless independently verified. Missing DOIs are not invented.

| Old reference | Disposition | Canonical DOI when known | Verification boundary |
|---|---|---|---|
| 1 | Not retained in T08 active citations | 10.3322/caac.21693 | No full-text support claim; no T08 statement relies on this source |
| 2 | Not retained in T08 active citations | 10.3389/fneur.2025.1664458 | No full-text support claim; no T08 statement relies on this source |
| 3 | Not retained in T08 active citations | 10.3390/genes15040501 | No full-text support claim; no T08 statement relies on this source |
| 4 | Not retained in T08 active citations | 10.1007/s11060-025-05164-0 | No full-text support claim; no T08 statement relies on this source |
| 5 | One canonical identity for duplicate original entries 5 and 13; not cited in replacement | 10.1093/neuonc/noae145 | No full-text support claim; no T08 statement relies on this source |
| 6 | Not retained in T08 active citations | 10.1158/2767-9764.crc-25-0564 | No full-text support claim; no T08 statement relies on this source |
| 7 | Not retained in T08 active citations | 10.1093/oso/9780190238667.003.0008 | No full-text support claim; no T08 statement relies on this source |
| 8 | Replace general homepage citation with R18 exact archived fact sheet | Not verified / not applicable | 2024 estimates v1.0 verified in downloaded PDF; new access date; old July citation cannot authenticate September release |
| 9 | Not retained in T08 active citations | 10.47464/metrociencia/vol33/suplemento-1/2025/s56-s69 | No full-text support claim; no T08 statement relies on this source |
| 10 | Not retained in T08 active citations | Not verified / not applicable | No full-text support claim; no T08 statement relies on this source |
| 11 | Not retained in T08 active citations | Not verified / not applicable | No full-text support claim; no T08 statement relies on this source |
| 12 | Not retained in T08 active citations | Not verified / not applicable | No full-text support claim; no T08 statement relies on this source |
| 13 | Duplicate of original 5; excluded from replacement bibliography | 10.1093/neuonc/noae145 | No full-text support claim; no T08 statement relies on this source |
| 14 | Retain as R19 for classification only; remove from COVID attribution | 10.1093/neuonc/noab106 | Full-text classification taxonomy inspected; not evidence for Ecuador imaging delays or COVID care disruption |
| 15 | Not retained in T08 active citations | Not verified / not applicable | Childhood survival review not used as evidence of prioritization of emergency neuro-oncology care in Ecuador; old mechanism claim removed |
| 16 | Not retained in T08 active citations | Not verified / not applicable | Original GLOBOCAN incidence/disease-mortality title is not a hospital-admission benchmark; the claimed international hospitalization ranges are removed, not numerically patched |
| 17 | Not retained in T08 active citations | Not verified / not applicable | No full-text support claim; no T08 statement relies on this source |
| 18 | Not retained in T08 active citations | Not verified / not applicable | No full-text support claim; no T08 statement relies on this source |
| 19 | Not retained in T08 active citations | Not verified / not applicable | No full-text support claim; no T08 statement relies on this source |
| 20 | Not retained in T08 active citations | Not verified / not applicable | European patient-survival study not used to establish Ecuador registry disruptions; historical 2017/2023 loss mechanism remains unknown |
| 21 | Not retained in T08 active citations | 10.3322/caac.21834 | GLOBOCAN 2022 metadata identified; removed as support for WHO molecular classification; R19 used for that narrower claim |
| 22 | Not retained in T08 active citations | Not verified / not applicable | No full-text support claim; no T08 statement relies on this source |
| 23 | Retain as R20 only for endpoints stated in author abstract | 10.1016/j.canep.2016.04.007 | Abstract Methods verified; publisher full text unavailable; no Ecuador-specific or hospital-rate numerical claim retained |
| 24 | Not retained in T08 active citations | Not verified / not applicable | No full-text support claim; no T08 statement relies on this source |

## GLOBOCAN edition and historical access

The exact IARC Ecuador PDF was downloaded and archived on 12 November 2026. It identifies GLOBOCAN 2024 estimates, version 1.0, and its release label is September 2026. Page 2 Brain CNS gives 561 new cases and 463 deaths, both sexes and all ages. The original figures are therefore retained as **estimated** events with a precise current citation. They must not be described as observed admissions or recorded disease events.

The old reference gives 20 July 2026 as its access date. The newly archived September-labelled artifact cannot establish what the dynamic endpoint showed in July. We use a new access date and a byte-level snapshot; no historical webpage state or exact download time is invented. The PDF hash and methods label are in `../provenance/t08/globocan_snapshot.json`. Earlier doubts about the edition/numbers are resolved for this archived revision artifact, without rewriting the historical review record.

## Literature scope and comparison policy

The WHO classification source was inspected in full text via PMC. The Piñeros regional paper was accessible as its authors' abstract through PubMed, while the publisher full-text request returned 403. Its use is limited to the registry/WHO mortality/world-standardization methods explicitly stated in that abstract. No Ecuador-specific subgroup, clinical interpretation or body-only claim is drawn from it. The active bibliography has one entry per identity and canonical DOI fields, with no /XML, /METRICS or article-page suffix appended to a DOI.

The original CBTRUS references 5 and 13 describe the same 2017–2021 report and map to one canonical DOI, 10.1093/neuonc/noae145. Neither is cited in the new sections because no US rate or anatomical benchmark is required. Other historical sources are omitted where no verified new claim needs them; omission is not a judgement that the source is false.

Contextual searches on 11–12 November 2026 included IARC Ecuador GLOBOCAN, the WHO classification, the regional brain/CNS study, the duplicate CBTRUS identifier, and Ecuador brain-hospitalization/INEC terms. This was not a systematic review or exhaustive novelty search. The first/unique claim is removed. No matched international C71 hospitalization benchmark was established in this targeted audit, so no numerical international rate comparison is retained. Absence of a comparator here is not evidence that none exists.

## Local results and hypotheses

All local estimates come from T02–T06 aggregate evidence. No outside citation is offered as proof of this study's own count, rate, adjusted odds ratio, convergence or historical event coding. The 2020 timing is descriptive; admission decisions, presentation, availability, case mix and recording are named only as untested alternative explanations. No hypothesis is stated as a mechanism established in Ecuador by these data.

The series remains descriptive with intervals. No trend, stability, equivalence, interrupted-time-series or causal COVID analysis was added. Sector and anatomical results retain their conditional outcome populations and missing-severity/selection limits. Figures and geographic interpretation remain T09, and author declarations remain T10.
