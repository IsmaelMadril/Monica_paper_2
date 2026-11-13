# T07 replacement sections and integration notes

Prepared 10 November 2026. The revised title, abstract, framing/objective and
Methods are ready in [editable Word](t07_manuscript_sections.docx) and
[version-controlled text](t07_manuscript_sections.md). The text is generated from
[t07_sections_template.md](t07_sections_template.md), with numerical results
inserted from validated aggregate evidence rather than typed into multiple drafts.
The [STROBE and RECORD crosswalk](t07_reporting_crosswalk.md) identifies verified
page references and outstanding items. This is a replacement-section document,
not an integrated submission manuscript.

## What changed

The title and opening now identify a nationwide discharge-record analysis rather
than a cancer-incidence or patient-follow-up study. C71 as the primary discharge
diagnosis is distinct from a verified first primary tumour. The aim describes
recorded hospitalization burden, deaths during admission and exploratory
associations, without determinants, causal effects or validated risk prediction.

The abstract uses 10,972 reconstructed admissions and 963 deaths, with all-admission
fatality 8.78% (95% Wilson interval 8.26–9.32). National rates use the separate
10,969-record resident population and the equal-year means 6.611 and 0.598 per
100,000, with their weighted-count intervals. It reports the corrected direction
of the death model, identifies the changed conditional-site comparison and
acknowledges its period sensitivity. It does not reuse the old 8,249-record cohort,
failed multinomial aRRRs, false elimination of unspecified codes, survival-window
claims or an untested stability claim.

Methods now document source versions and access, exact diagnosis selection,
source/eligible counts, distinct analysis populations, age units, nonoverlapping
stay groups, unknown ethnicity, provisional early residence codes, population
sources, annual denominators versus fixed standard weights, rate/fatality formulas,
interval methods, covariates and references for all primary models, diagnostic and
sensitivity procedures, sparse-cell tests, p precision, dependence and coding limits.
No patient deduplication, clinical validation, ethics exemption or unverified
institutional completeness is invented.

## Numerical and artifact evidence

[provenance/t07/numeric_traceability.json](../provenance/t07/numeric_traceability.json)
contains 32 numeric entries with source path, source-row filters/aggregation,
raw field value and displayed rounding. Every abstract result is traceable.
`run_metadata.json` records source/code/template hashes and generated-text/Word
fingerprints. Cross-stage cohort checks require exact byte identity for T04–T06;
T03's recorded Windows hashes match exact LF/CRLF transformations for the cohort
and aggregate input files. This is narrowly verified line-ending equivalence,
not general whitespace normalization or a waiver of content mismatches.

At T07 inspection a Word manuscript was present at
`data/raw/baseline_2026-10-23/Writeable/tumores encefalo Monica art completo.docx`.
It is not one of the six entries in the frozen T01 manifest. Its hash is recorded
as an additional observed artifact; its creation date, version and equivalence to
the reviewed PDF are unverified. Earlier statements that editable source was
unavailable describe the earlier workflow; they must not be silently converted
into a claim that this file was a verified original T01 input. It was inspected
for wording and section structure, preserved unchanged and not required to rebuild
the replacement text. The six-input T01 manifest remains unchanged.

The Word document was rendered using bundled LibreOffice and every one of its
seven page images was visually checked, with page locators verified against the
rendered text. Layout uses readable type and fixed section page breaks; no title
border or clipped long DOI remains. `render_verification.json` ties pagination and
review to the exact Word/PDF hashes. Rendered images/PDF are QA files; the Word
file is the editable deliverable. Page numbers may change in another Word engine;
retain section labels and recheck the final journal layout.

## Original issue coverage and pending manuscript integration

| Issues | Replacement text and evidence | Remaining work |
|---|---|---|
| 1–4 scope and framing | Title, abstract, p. 2 objective/design and p. 3 coded-diagnosis definition | Replace matching wording throughout the original Introduction, Discussion and conclusion. Literature/context review is T08. |
| 5 record unit | pp. 2–3 records, repeat admissions and no person linkage/deduplication | Use admissions consistently in Results, tables and figures. |
| 6 statistical comparisons | pp. 5–6 models, references and sparse-table testing | Insert generated Tables 1–2/4–5 and align the full Results narrative. |
| 7–8 rate methods | p. 4 annual denominators, observed standard, formulas and distinct mortality denominators | Insert rebuilt Table 3, remove old means/extrema everywhere and regenerate Figure 1 in T09. |
| 9, 14–15 interpretation | pp. 1, 4–6 conditional uncertainty, coding and association limits | Rewrite old causal, coding-accuracy, diagnostic-window and stability claims in T08. |
| N04, N09, N14 | Numeric source ledger, reproducibility wording and explicit checklist coverage | Full-paper consistency check and final journal checklist/page numbers after integration. |

T07's requested **replacement-section deliverables are prepared**. Its stricter
full-paper completion criterion remains open: the original manuscript is not
consistent until Results, Discussion, conclusion and figures are updated and the
new sections are integrated. The tracker therefore records draft completion
without checking off full T07. No statistical results were refitted in this task.

T02 early residence labels remain unresolved; T07 does not use them in all-year
comparisons. T10 must verify ethics/exemption basis, consent, funding, conflicts,
contributions and access statements. Neither this draft nor its reporting
crosswalk authorizes a claim of ethics approval or complete STROBE/RECORD compliance.

## Reproduction

After T02–T06 outputs exist for the same cohort, run on macOS or Windows with the
project environment active:

```sh
python -X utf8 scripts/prepare_t07_sections.py
```

This regenerates the Markdown and numeric ledger using only the Python standard
library; no acquisition or model fitting occurs. It stops on cohort/content
mismatches. The optional baseline Word file is fingerprinted when present and is
not a runtime requirement. Do not rerun earlier acquisition to overwrite historical
manifests just to satisfy a text-generation check.

Optional Word export requires `python-docx==1.2.0`, separate from analysis dependencies:

```sh
python -m pip install -r requirements-documents.txt
python -X utf8 scripts/prepare_t07_sections.py --docx
```

The delivered Word export and render were executed with the bundled document
runtime on macOS. New Windows generation/rendering has not been verified.
Editing the template and rebuilding requires renewed numeric/editorial review;
Word edits alone do not update the authoritative text or source ledger. Re-render
and recheck page references after layout changes. The analysis pipeline remains
independent of the optional document-export dependency.
