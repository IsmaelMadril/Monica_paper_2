# T08 interpretation and evidence audit

Completed 12 November 2026 for the replacement Introduction, Discussion and
Conclusion. Read the [editable Word sections](t08_interpretation_sections.docx),
[version-controlled text](t08_interpretation_sections.md) and
[claim/reference evidence ledger](t08_evidence_ledger.md). The five-page Word
export was rendered and all pages were inspected. These sections replace the
corresponding historical narrative; the old manuscript/PDF is preserved.

## Main decisions

The narrative now describes recorded C71 admissions and deaths during admission,
with their distinct admission and resident-population denominators. The corrected
age association replaces the old protective-age interpretation. Sector and
anatomical estimates retain their outcome populations, uncertainty and unmeasured
case-mix limitations. The later-year pediatric anatomical estimate is not used to
replace the all-year result. Unspecified coding remains common and nonzero in 2024.

Unsupported claims of coding accuracy, elimination of unspecified records,
protected emergency services, imaging/surgery delay as an established COVID
mechanism, national 2017/2023 registration disruptions, tertiary complexity and
causal care/access disparities are removed. The first/unique claim is removed
without pretending that a contextual search was exhaustive. The study's stated
contribution is an auditable service-event analysis alongside cancer-registration
estimates, not a new biological pattern or an incidence measure.

Temporal results remain **descriptive with intervals**. No trend, equivalence,
interrupted-time-series or COVID causal model was fitted. Alternative explanations
for 2020 timing are explicitly untested, rather than externally cited as if they
were mechanisms established by this cohort. The original 3.5–6.0 versus 7.0–11.5
international rate comparison is omitted because its cancer incidence/disease
mortality endpoints do not match C71 hospital event rates or age standards. This
audit did not establish a matched hospitalization comparator; it does not prove
that no such study exists.

## GLOBOCAN verification resolves an earlier uncertainty

The original Ecuador figures **561 new brain/CNS cases and 463 deaths** are
confirmed in the archived IARC PDF: **GLOBOCAN 2024 estimates, version 1.0**,
release label **September 2026**, both sexes and all ages, page 2 Brain CNS row.
They are retained as **estimated**, not recorded, events. The fact sheet's source
methods also describe model-based incidence estimation and projected national
mortality rates. It cannot benchmark observed hospital admissions or deaths
restricted to admission. The exact PDF and extracted text are tracked under
`provenance/t08/sources/`; its SHA-256 and selected fields are in
[globocan_snapshot.json](../provenance/t08/globocan_snapshot.json).

The old reference's access date is 20 July 2026. A newly retrieved PDF labelled
September does not authenticate the endpoint's July contents. The revision uses
12 November 2026 access and the frozen bytes; no previous endpoint state is
invented. The earlier review's uncertainty is preserved as historical review
material rather than silently rewritten. This check supports the exact edition
and numbers in the replacement text, not the old access-date provenance.

## Reference and claim audit boundaries

All **24 original reference entries** were extracted from reviewed PDF pages
21–22, fingerprinted and dispositioned. The original CBTRUS entries 5 and 13
identify the same report and collapse to one canonical DOI identity; neither is
needed in the new text. Old DOI paths with /XML, /METRICS or article-page suffixes
are normalized in the audit. A syntactically cleaned DOI for an unused reference
is not claimed to be independently resolved or full-text validated. Unverified
missing DOI fields remain empty rather than guessed.

The active new bibliography adds R18 (IARC snapshot), R19 (classification authors'
WHO summary) and R20 (regional registry study). Existing primary-source and
statistical identities R01–R09 remain available. R19 is cited for classification,
not COVID effects. R20 is used only for the incidence-registry, WHO mortality and
world-standardization methods explicitly stated in the authors' PubMed abstract;
the publisher full-text request returned 403. No body-only result, Ecuador-specific
subgroup finding or numerical hospital-rate benchmark is inferred. The discarded
references are not described as false simply because they are no longer needed.

The machine-readable ledger has **29 dispositions**: 21 retained narrative
paragraphs classified by evidence type and eight removed historical claims. Local
results cite executed evidence, rather than external papers as proof of this
study's findings. Limitations and analytical interpretations are identified as
such. Every quantitative placeholder used in these sections is linked to one of
**44 numeric entries** with source path, row filter and displayed rounding.

The source audit used targeted primary-source/context searches on 11–12 November
2026, not a systematic review. Search scope and access limitations are disclosed
in the evidence ledger. Clinical coauthors should review the framing and
interpretation before manuscript adoption; no independent clinical case validation
was performed.

## What remains

T08's replacement narrative and evidence-audit deliverables are complete for the
executed specifications. Whole-paper integration still requires replacing the
old Results, assembling the T07/T08 sections and rebuilt tables, and auditing
consistency. **T07 therefore remains open** under its manuscript-wide criterion.
T09 must rebuild figures and geographic reporting. T10 covers ethics/exemption
basis, consent, author declarations, journal requirements and final submission
review. The early T02 residence-label question remains explicit and unresolved.
No statistical results were refitted for T08.

## Reproduction on macOS and Windows

After T02–T07 evidence exists for the same cohort, activate the local environment
and use the same command in either shell:

```sh
python -X utf8 scripts/prepare_t08_sections.py
```

The builder uses the Python standard library and the existing T07 formatting
helper; it reads the tracked IARC snapshot without network requests. It verifies
T07 input fingerprints and the archived PDF hash, then rebuilds Markdown, the
numeric ledger and run metadata. The authoritative text is
`t08_sections_template.md`. Read the claim/reference ledger alongside edits;
changing the prose alone does not establish new source support.

Optional Word export uses the separate document dependencies already introduced
in T07:

```sh
python -m pip install -r requirements-documents.txt
python -X utf8 scripts/prepare_t08_sections.py --docx
```

No analysis dependency changes. Export/render were verified on macOS with the
bundled document runtime; new Windows execution remains unverified. Re-render
after text/layout changes. The SHA-256/page map in
`provenance/t08/render_verification.json` identifies the reviewed Word output.
A new acquisition is not required to reproduce this version; if the IARC endpoint
changes, preserve the existing snapshot and record the new version separately.
