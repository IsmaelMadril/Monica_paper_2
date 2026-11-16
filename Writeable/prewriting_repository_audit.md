# Repository and results audit before manuscript integration

Audit date: 13 November 2026. Repository at start: clean, commit `e1d461c`.

## Readiness decision

**Ready to begin a bounded manuscript draft using the reconstructed results; not ready for submission or a claim that every original issue is closed.** No numerical blocker was found in the checks executed here. The scientific scope must remain admission-level C71-coded hospital activity and in-hospital outcomes. Journal acceptance or Q1 suitability cannot be established by passing computational checks.

This audit reviews the current local repository, code, recorded evidence and documentation. It reruns all tests and the three primary models without overwriting their historical outputs. It does not repeat downloads/extraction of every raw release, independently replicate the statistical implementation, revalidate diagnoses, conduct a new literature search, re-render Word documents or execute on a clean Windows machine. Earlier visual reviews remain historical evidence.

## Checks executed and results

| Check | Result | Interpretation |
|---|---|---|
| Full unit/integration suite | 72 tests passed, no skips; 1.083 seconds | Current local data and saved outputs pass implemented controls |
| Installed dependency consistency | `pip check`: no broken requirements | Does not prove installation from a clean environment |
| T03–T09 input fingerprints available under `inputs_sha256`/`input_sha256` maps | 76 entries: 71 exact, four exact LF/CRLF equivalents, one bibliography change | This is a scoped metadata audit, not verification of every raw-file manifest |
| Mortality primary refit | 26 contrasts: maximum absolute beta/SE difference 0 | Current cohort and implementation reproduce stored coefficients and standard errors |
| Coding-detail primary refit | 15 contrasts: difference 0 | Same result |
| Conditional anatomical primary refit | 15 contrasts: difference 0 | Same result |
| Fresh primary model diagnostics | All converged, no detected separation | Numerical validity under the fitted specification; not causal validity |
| Table/rate/geography tests | Passed | Includes rate additivity/means, cohort totals, table cells and 480 geography cells |

Evidence: [fingerprint audit](../provenance/prewriting_audit/input_fingerprint_audit.json), [fresh refits](../provenance/prewriting_audit/primary_refits.json). Refit comparisons cover coefficients and standard errors, not a fresh recalculation of every sensitivity/profile interval.

The T08 bibliography mismatch is explained: removing the appended T09 entries R21/R22 and restoring the terminal newline reproduces the earlier SHA-256. Preserve that historical hash; record the expanded bibliography at manuscript integration. The four line-ending equivalents are the already documented T03 inputs, not substantive data differences.

## Results suitable for the new draft

| Quantity | Audited result | Reporting constraint |
|---|---:|---|
| Admissions, 2015–2024 | 10,972 | Records, not unique people or incident cancers |
| Deaths during admission | 963 | Not all deaths from brain cancer in Ecuador |
| Live discharges | 10,009 | Do not describe as long-term survival |
| Overall admission fatality | 8.7769% | Admission denominator; distinguish from population rates |
| Resident admissions for national rates/maps | 10,969 | Three foreign-resident live discharges excluded |
| Mean annual standardized hospitalization rate | 6.611238 per 100,000 | Five age bands, fixed observed 2022 census weights |
| Mean annual standardized in-hospital death rate | 0.598464 per 100,000 | Annual resident denominators; not a cumulative risk |
| 2024 unspecified admissions | 379 | Unspecified coding was not eliminated |
| Coding-detail panel | 10,972 admissions; 6,304 non-C719 events | Coding detail is not validated accuracy |
| Anatomical panel | 6,192 admissions; 1,523 infratentorial/midline events | Conditional selected population; excludes C718/C719 |

Annual admissions/deaths independently tabulated from the current cohort:

| Year | Admissions | Deaths |
|---|---:|---:|
| 2015 | 1,073 | 97 |
| 2016 | 1,057 | 95 |
| 2017 | 1,221 | 113 |
| 2018 | 1,148 | 104 |
| 2019 | 1,239 | 103 |
| 2020 | 942 | 75 |
| 2021 | 1,080 | 87 |
| 2022 | 1,098 | 101 |
| 2023 | 1,095 | 101 |
| 2024 | 1,019 | 87 |

2017 and 2023 are ordinary complete selected cohorts in this reconstruction; the legacy reductions cannot justify excluding those years. The primary mortality model estimates death=1. Age 80+ versus 0–17 has adjusted OR 2.631 (95% Wald interval 1.864–3.715). The public/private association is 1.201 (1.035–1.394), but cannot be interpreted as a hospital-quality effect. The original failed survival-coded model and mixed-outcome multinomial estimates must not enter the new Results.

## Findings and required actions

| Priority | Finding | Action and completion criterion |
|---|---|---|
| High, before final narrative | T07 and T08 are replacement sections, not an integrated article. Legacy manuscript results remain incompatible. | Assemble one new manuscript from T03–T09; write Results from rebuilt tables; check every abstract/body/table/figure value against a source ledger. Preserve original files. |
| High, scientific interpretation | Patient and facility dependence cannot be estimated with established identifiers. HC0 does not solve clustering. | Explicitly state conditional independence assumptions for intervals/models; avoid patient-level risk, causal and precision claims. Coauthors accept this limitation before submission. |
| High, restricted variable | Rural/urban labels for 2015–2017 remain provisional. | Either obtain independent labels or keep the implemented exclusion from all-year adjustment and restrict residence comparisons to verified 2018–2024. This does not block national rates or province-count figures. Do not mark unrestricted T02/G1 complete. |
| High, scope approval | Primary anatomy analysis changes the estimand; C715–C717 is an operational group; C719/C718 selection may be nonrandom. | Retain the two distinct questions, C715 sensitivity and selection limitation. Obtain scientific coauthor agreement on the specification before final manuscript approval. |
| High, submission | T10 ethics/declarations, author contributions, funding/conflicts and journal requirements remain unverified. | Obtain factual author/institution statements and select the target journal; never infer exemption or invent approval identifiers. These are submission requirements, not reasons to delay a bounded draft. |
| Medium, reproducibility | Local tests pass with existing ignored inputs/outputs. A fresh clone and full modern Windows pipeline have not been demonstrated in this audit. | Reproduce from manifests on a clean environment, install core/document/figure requirements, regenerate outputs and run the full suite with no unintended skips. Record Python/platform versions and log. Earlier Windows T03 validation does not validate T04–T09. |
| Medium, provenance | T08 references fingerprint predates the T09 bibliography additions. | Preserve the historical record and add a new integration manifest with the final bibliography and all adopted artifacts. Earlier content is verified unchanged. |
| Medium, issue tracking | Several log rows combine obsolete “pending” or “no correction verified” text with later completion evidence; T03 report still says figures await T09, T04 report says T07 next. | Reconcile current status in the master log, explicitly date historical statements, and link this audit. Avoid rewriting old execution evidence as if rerun. |
| Medium, historical lineage | Original extraction/cleaning script remains unavailable; supplied SAV/SPV/XLSX are the complete provided package. | Describe the analysis as reconstructed from archived official releases. No additional missing SAV is alleged. Explain that exact historical losses/recodes remain unknown. |
| Medium, scientific restraint | Sparse ethnicity contrasts, many comparisons, descriptive year changes and count maps invite overinterpretation. | Keep exploratory labels/profile intervals, avoid selective significant-result emphasis, and make no trend/stability/pandemic-causality claim without a separately defined analysis. Province counts are not population risk. |

## Recommended writing sequence

1. Agree the scope and primary estimands already implemented: admission outcomes, resident population rates, coding detail and conditional anatomy. Retain the five-band primary standard with the narrower-band sensitivity unless a documented scientific decision changes it.
2. Build the Results section from rebuilt Tables 1–5 and T09 figures, then integrate the existing T07/T08 sections. Use the new source ledger as the numerical authority.
3. Review all limitations and sensitivity results with clinical/statistical coauthors; resolve or explicitly bound early residence labels and historical provenance.
4. Complete the clean-workstation reproduction and reconcile the issue tracker. Freeze the adopted inputs, code, tables, figures, bibliography and manuscript in a dated integration manifest.
5. Complete T10 author/institution/journal checks and final reporting/formatting review before submission.

No model, dataset, historical metadata or article section was changed by this audit. Only this report and the audit evidence were added.
