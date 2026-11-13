# T07 STROBE and RECORD reporting crosswalk

Prepared 10 November 2026. Page references identify the **seven-page T07
replacement-section document**, not the original reviewed PDF or a completed
submission manuscript. They were checked against its latest rendered pagination;
Word repagination on another system must be checked again. Section headings give
a second locator. The Word file and its section-text hash are recorded in
`provenance/t07/run_metadata.json`; the render/page map is recorded separately.

Sources: the [STROBE explanation](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0040297)
and [RECORD statement and checklist](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1001885).
This is a coverage audit, not a certification of compliance or methodological validity.
Items are paraphrased below; consult the original checklists for their full wording.
The design is repeated cross-sectional discharge-record analysis, not longitudinal
patient follow-up. T07 does not claim that the legacy Discussion, tables or figures
have been integrated into the replacement document.

## STROBE coverage

| Item | Topic | T07 page and section or evidence | Status and remaining action |
|---|---|---|---|
| 1a | Identify design | p. 1 Abstract; p. 2 Study design and data sources | Covered in replacement sections. |
| 1b | Balanced abstract | p. 1 Abstract | Counts, matched rate population, uncertainty and limitations included; numeric source ledger supplied. |
| 2 | Scientific context | p. 2 Study framing and objective | Partial. This defines service-event scope; literature-based Introduction awaits T08. |
| 3 | Study objectives | pp. 1–2 Abstract and Study framing | Covered; descriptive and exploratory objectives, no causal hypothesis. |
| 4 | Design explained early | p. 2 Study design and data sources | Covered. |
| 5 | Setting and dates | p. 2 Study design and data sources | National releases and discharge years specified; institutional completeness is not asserted. |
| 6a | Eligibility and selection | p. 2 Record selection and analysis populations | Covered for discharge records; exact codes and flow supplied. |
| 6b | Matching or follow-up provisions | p. 2 Record selection | Not applicable to this unmatched cross-sectional design; no patient follow-up. |
| 7 | Variable definitions | p. 3 Outcome definitions and Covariate construction; p. 5 Primary regression models | Covered; primary diagnosis does not establish primary tumour origin. |
| 8 | Measurement sources | pp. 2–4 Sources, Covariates, Population denominators | Codebooks and recorded-data limitations described; clinical validation unavailable. |
| 9 | Bias | p. 6 Bias and reproducibility | Covered in Methods; fuller interpretation remains T08. |
| 10 | Study size | p. 2 Record selection | All released eligible records retained; no power-based sampling or sample-size target. |
| 11 | Quantitative-variable handling | pp. 3–4 Covariates and Standardization | Explicit age/stay bands, boundaries, standard population and narrower-band sensitivity. |
| 12a | Statistical procedures | pp. 4–6 Rates, Regression and Descriptive comparisons | Included covariates and limited adjustment rationale; not complete confounding control. |
| 12b | Subgroups and interactions | pp. 4–6 Alternative rates and Sensitivity analyses | Anatomical strata and restricted periods declared; no interaction search. |
| 12c | Missing data | p. 3 Covariate construction and data checks | Source unknown ethnicity retained; no imputation; no primary model null exclusion. |
| 12d | Design-specific analytic handling | pp. 2, 6 Record selection and Bias | No survey weights, patient matching or follow-up; complete eligible release records, with capture/dependence limitations. |
| 12e | Sensitivity analyses | pp. 4, 6 Alternative rate specifications and Sensitivity analyses | Executed alternatives described, with no preferred-result substitution. |
| 13a | Record flow | p. 2 Record selection | Aggregate source/selection/model populations reported; annual supplementary flow in provenance/t02/selection_flow.csv. |
| 13b | Exclusion reasons | pp. 2, 5 Selection and Primary regression models | Diagnosis rule, foreign-resident rate exclusion, restricted residence period and site-panel exclusions explicit. |
| 13c | Flow visualization | p. 2 Record selection | Counts and machine-readable annual flow supplied; diagram optional and not created in T07. |
| 14a | Descriptive characteristics | p. 3 definitions; T06 Tables 1–2 | Available as separate generated tables, not inserted in this section-only document. |
| 14b | Missing-value counts | p. 3 data checks; provenance/t06/missingness.csv | Nulls distinguished from 1,290 unknown-ethnicity records. |
| 14c | Follow-up summary | p. 3 endpoint definition | Not applicable; observation ends at recorded discharge, without person follow-up. |
| 15 | Outcome counts | p. 1 Abstract; pp. 2–3 populations/outcome | Overall counts included; annual and category counts available in separate T06 tables. |
| 16a | Estimates and precision | p. 1 Abstract; T03–T06 tables | Selected adjusted estimates/intervals in abstract; full crude/adjusted Results integration pending. |
| 16b | Category boundaries | pp. 3, 5 Covariates and Models | Explicit age/stay bounds and model references. |
| 16c | Absolute measures where useful | p. 1 Abstract; p. 4 rates/fatality definitions | Admission fatality and population rates shown alongside odds ratios; no OR-to-risk conversion. |
| 17 | Other analyses | p. 6 methods; T03–T05 sensitivity outputs | Methods covered; full sensitivity Results narrative remains to integrate. |
| 18 | Main findings in relation to aims | p. 1 Abstract | Abstract covered; Discussion remains T08. |
| 19 | Study limitations | pp. 4–6 uncertainty and bias | Main assumptions stated; full direction/magnitude discussion of bias remains T08. |
| 20 | Overall interpretation | p. 1 Conclusions | Restrained abstract conclusion; full manuscript interpretation pending T08. |
| 21 | Applicability | pp. 2, 6 national source and bias | Limited to recorded admissions; fuller external-validity discussion pending T08. |
| 22 | Funding and funder role | No verified statement supplied | Open author confirmation in T10; do not infer no funding. |

## RECORD extension coverage

| Item | Topic | T07 page and section or evidence | Status and remaining action |
|---|---|---|---|
| 1.1 | Routine data identified | p. 1 title subtitle and Abstract; p. 2 Sources | Hospital-discharge records and INEC identified. |
| 1.2 | Region and period | p. 1 title and Abstract | Ecuador, 2015–2024. |
| 1.3 | Linkage identified when used | pp. 2, 6 Selection and Bias | No person/institution-level linkage; annual records stacked and aggregate population cells matched only. |
| 6.1 | Record-selection codes | pp. 2–3 Selection and Outcome definitions | Exact normalized C710–C719 rule plus source scripts and annual flow. |
| 6.2 | Code validation | p. 3 Outcome definitions and data checks | No clinical/chart validation; coding/range checks are not represented as clinical validation. |
| 6.3 | Linked-population flow | pp. 2, 6 Selection and Bias | Not applicable to person-level linkage, which was not performed. |
| 7.1 | Codes for analyzed concepts | pp. 3, 5 Covariates and Models | Diagnosis, death and references stated; full variable dictionaries and source code lists in provenance/t02/. |
| 12.1 | Scope of data access | p. 2 Sources | Released annual SPSS records/dictionaries; no clinical records or identifiable patient database accessed. |
| 12.2 | Cleaning and preparation | pp. 2–3 Selection and data checks | Normalization, age units, stay boundaries, dates, unknowns and retained repeated projections described. |
| 12.3 | Database linkage methods | p. 6 Bias | No record linkage; year/age aggregate matching to denominators stated. |
| 13.1 | Population derivation | p. 2 Selection; p. 5 Models | All selection branches counted and source annual flow supplied. |
| 19.1 | Limits of routine data | pp. 3–6 validation, uncertainty and bias | Methods caveats included; full Discussion, selection and temporal eligibility appraisal remain T08. |
| 22.1 | Protocol data and code access | p. 6 Reproducibility; repository guides | Partial. Local scripts/specifications/manifests exist; final persistent URL, access terms and author availability statement remain T10. |

## Other declarations and closure conditions

Ethics review/exemption basis, any identifier, consent requirements, funding,
conflicts, contributions and final public-access terms require author verification
in T10. The historical ethics paragraph is not carried into this document as an
established exemption. No new legal/ethical determination was made.

T07 replacement sections and this crosswalk are ready for coauthor review. Full
T07 closure still requires integrating the sections with updated Results,
Introduction/Discussion and figures and auditing consistency throughout the paper.
The older PDF and newly located, unmanifested baseline Word file remain preserved.
Do not submit a mixture of the replacement sections and unrevised old results.
