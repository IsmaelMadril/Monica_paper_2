# Malignant brain neoplasm hospitalizations in Ecuador

Research workspace for the 2015–2024 nationwide hospital-discharge manuscript.
The unit of analysis is an admission/discharge record. The project is currently
at **T02: official-source admission reconstruction implemented**. The rebuilt cohort
contains 10,972 admissions and 963 deaths. Early-year residence-area labels remain
provisional; rates and models require recalculation. See the [T02 audit](Writeable/t02_data_audit.md).

Start with the [independent review](Writeable/current_state_review.md),
[revision task plan](Writeable/revision_task_plan.md) and
[baseline provenance notes](provenance/README.md).

## Local setup

The environment uses Python 3.14.7. `requirements.txt` now pins the installed T02
reading/analysis dependencies; T01 preservation tooling still uses only the standard library.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/freeze_inputs.py --verify
```

The `.venv` already exists in the current workspace. For a new checkout, create
it using the commands above and restore the source inputs and snapshots from
separate storage before verification. Python 3.11 or newer is required for the
checksum script. Environment records are in `provenance/environment.json` and
`provenance/environment_freeze.txt`; activation ends with `deactivate`.

## Project layout

| Path | Purpose |
|---|---|
| `Writeable/` | Manuscript PDF, original review, independent review and revision plan |
| `Data_base/` | Supplied legacy SAV and workbooks; preserve unchanged |
| `Results/` | Supplied legacy SPSS viewer output |
| `data/raw/baseline_2026-10-23/` | Verified local snapshots of six supplied inputs |
| `data/processed/` | Future derived datasets |
| `provenance/` | Input hashes, variable dictionary, lineage, issue log and environment records |
| `scripts/` | Reproducible processing and verification tools |
| `outputs/tables/`, `outputs/figures/`, `outputs/reports/` | Future generated analysis products |

## Verify the preserved inputs

```sh
.venv/bin/python scripts/freeze_inputs.py --verify
```

This checks SHA-256 hashes for both original paths and local snapshots. The initial
freeze has already been performed; running the script without `--verify` refuses
to overwrite an existing manifest. The manifest records filesystem dates and a
capture timestamp; national source release dates remain unknown.

Dataset files, SPV output, local snapshots, derived data, generated analysis
products and the virtual environment are excluded from Git. Metadata, scripts,
review documents and the manuscript PDF remain eligible for version control.
Use separate storage/backups for ignored inputs; Git alone is insufficient to
restore this project. No files have been committed as part of this setup.

## Current provenance limits and next work

Observed SPSS commands identify candidate routes for Tables 1, 2, 4 and 5.
Table 3 and Figures 1–2 lack verified generation routes. Workbook purposes are
filename-based candidates; their production history is unknown. The editable
manuscript, original annual INEC files/codebooks, population files, and plotting
code are not present. See the lineage and provenance notes for the full record.

T02 downloaded and reconstructed all ten national releases. The audit documents
year discrepancies, corrected anatomical groups and explicit age/stay/outcome coding.
The original extraction script is unavailable for now; early-year residence-area
labels still require confirmation before association modelling. Next is T03 rate
recalculation, followed by model repair in T04/T05.

Reproduce the audit from downloaded sources:

```sh
.venv/bin/python scripts/extract_inec.py
.venv/bin/python scripts/audit_admissions.py
.venv/bin/python -m unittest discover -s tests -v
```

For new source acquisition, run `scripts/acquire_inec.py` and optionally
`scripts/acquire_early_dictionaries.py` first; these require internet access.
Individual admission outputs remain ignored; aggregate audit evidence is tracked
in `provenance/t02/`. T01 environment records describe the historical baseline;
current versions are recorded separately in `provenance/t02/environment_freeze.txt`.
