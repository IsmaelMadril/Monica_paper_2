# New article editing record

16 November 2026. Applied the original-draft checklist to `../data/raw/baseline_2026-10-23/Writeable/New_article.docx`, the supplied file matching the user's request. The working source was untracked at the start. The prior manuscript PDF and the other original Word manuscript were not changed.

Backup: `../outputs/reports/article_edit/New_article_before_edit.docx` (local, ignored by Git). Paragraph-level before/after evidence: `../provenance/article_edit/paragraph_changes.json`. Validation: `../provenance/article_edit/validation.json`. The editing script rebuilds from this backup, not from later manual author edits; do not rerun it over subsequent author revisions without preserving them.

Preserved the author block, affiliations supplied by the author, corresponding-author details, main section sequence, eligible diagnosis/unit-of-analysis statement, anatomical list structure, direct-standardization explanation, two native equations, distinction between mortality denominators and core limitations. Invalid numerical and interpretive passages required replacement. Removed duplicated background and unsupported mechanisms rather than retaining them as established claims. Rebuilt Tables 1–5 use 23 editable table blocks with repeated headers; Figures 1–2 are embedded at publication resolution. References are renumbered by first citation, using previously verified sources. No new literature verification was claimed for omitted original assertions.

All 23 table blocks match the source Markdown cells, with only two Table 4 header labels shortened for layout. Every decimal/scientific numeric token from the table bodies is present in the rendered text. Both figures and both native equations remain present. All 19 rendered pages were reviewed, with unchanged pages confirmed against the previously inspected render. A lost Table 5 panel in an intermediate render was detected and corrected by an explicit panel page break. No statistical inputs or fitted estimates were changed.

## Integrated manuscript reporting locations

Page numbers refer to the 19-page bundled-renderer output of the final Word file, not the historical PDF. Word may repaginate elsewhere.

| Checklist coverage | Final location | Remaining boundary |
|---|---|---|
| Title and abstract; design and balanced results | p. 1 | Journal word limit/style not selected |
| Context and objectives | p. 2 Introduction | No first/unique claim |
| Source setting and eligibility, RECORD codes and selection | pp. 2–3 Methods | Annual flows/manifests remain external reproducibility materials |
| Variables, missingness and group handling | pp. 3–4 Methods | Early rural/urban labels remain provisional and bounded |
| Rates, model specification, uncertainty, sensitivity and bias | pp. 4–5 Methods | Conditional independence and absent clinical covariates remain limitations |
| Record characteristics and explicit denominators | pp. 5–10 Tables 1–2 | Residence blocks cover 2018–2024 only |
| Rate results and uncertainty | pp. 10–13 Table 3 and Figure 1 | No formal trend or pandemic causal analysis |
| Adjusted findings and sensitivity narrative | pp. 13–16 Tables 4–5 | Exploratory associations; no clinical validation |
| Geographic assignment and count interpretation | pp. 16–17 Figure 2 | Figure S1 atlas and S2 facility comparison remain separate T09 outputs |
| Interpretation, limitations, applicability and conclusion | pp. 18–19 | Coauthor scientific review still required |
| Ethics, funding and availability | p. 5 ethics comment | Author confirmation required; submission not closed |

## Author-only items still open

Two Word comments flag affiliation 6 and the unverified declarations. The ethics paragraph now states only established data-access facts. No approval/exemption, consent waiver, absence of funding/conflicts or author contributions were invented. Supply these statements before submission. Final public repository/access terms, supplement packaging, target-journal requirements, independent workstation reproduction and coauthor approval remain open. The new document is an integrated revision for author review, not a declaration that T10 is complete.

Supplementary files referenced in the text are existing repository deliverables: T02 selection and source manifests; T03 age weights, denominators and sensitivities; T04/T05 diagnostics and sensitivity/profile outputs; T06 test/missingness records; T09 annual atlas and facility heatmap with captions in `t09_figure_legends.md`. Include these in the eventual submission package with journal-specific numbering.
