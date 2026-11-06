# Research provenance and reproducibility

This directory documents the preserved T01 baseline and T02 source reconstruction.
It is shared through Git; large inputs and generated admission files are restored
separately on each machine. See the [main README](../README.md) for macOS and Windows
PowerShell setup and [the T02 audit](../Writeable/t02_data_audit.md) for findings.

## Baseline and source records

Baseline date: 23 October 2026. Six supplied research inputs have local snapshots
and SHA-256 hashes. Filesystem modification times are metadata, not proof of a
national source release date.

| File | Purpose |
|---|---|
| `input_manifest.csv` | Original/snapshot relative paths, sizes, hashes, timestamps and version uncertainty |
| `artifact_lineage.csv` | Baseline provenance for all five manuscript tables and both figures; unknown routes remain explicit |
| `workbook_inventory.json` | Baseline workbook sheet inventory; names alone do not establish production history |
| `legacy_spss_log.txt` | Extracted legacy SPSS XML log text with the old machine path redacted; not runnable syntax |
| `variable_dictionary.csv` | Provisional baseline variable definitions from the manuscript and logs |
| `issue_resolution_log.csv` | Original issues, new findings, task decisions and validation status |
| `environment.json`, `environment_freeze.txt` | Historical T01 environment and bootstrap packages |
| `inec_download_manifest.csv` | Official annual SPSS/dictionary download URLs, dates, sizes and hashes |
| `inec_syntax_manifest.csv` | Early-year official syntax archive URLs and hashes |
| `t02/` | Annual schemas, selection flow, reconciliation, missingness, recoding definitions, validation and T02 environment records |

T02 downloaded the ten official annual INEC releases and available separate
2018–2024 dictionaries. Early-year SAV metadata and official syntax were also
inspected. These acquisitions supersede the T01 statement that all national source
files were absent. They do not establish how the old 8,249-record extract was made.

## Using the records on macOS and Windows

Manifest paths are relative to the repository root and use `/`. Python `pathlib`
resolves them on either operating system; do not replace them with your machine's
absolute paths or change path separators inside the manifests.

Create a local virtual environment and install the shared `requirements.txt` on
each machine. Do not copy `.venv` or assume macOS binaries run on Windows.
The environment records describe past runs; they are not platform-independent
Python installations. Use explicit UTF-8 mode for project commands so Spanish
labels and text files have the same encoding on both machines.

After changing to the project root and activating the local environment, run these
same commands in either shell:

```sh
python -X utf8 scripts/freeze_inputs.py --verify
python -X utf8 scripts/extract_inec.py
python -X utf8 scripts/audit_admissions.py
python -X utf8 -m unittest discover -s tests -v
```

If PowerShell activation is blocked, replace `python` with
`.\.venv\Scripts\python.exe`. Without activation on macOS, replace it with
`./.venv/bin/python`. No execution-policy change is required to invoke Python
directly. Restore baseline and official input files before running the audit.

Keep the version-controlled manifests and their archived inputs together. Do not
rerun acquisition merely to verify a restored archive: the acquisition scripts can
update manifests. The audit verifies official archive hashes, and the extraction
script checks cached C71 extract hashes. Baseline verification checks both original
and snapshot content. Different filesystem timestamps on a second machine do not
invalidate content hashes; altered text line endings do.

## Remaining provenance gaps

1. The original extraction/cleaning script is unavailable for now; the author may
   supply it later. Historical year losses and category transformations cannot be
   fully traced from the final legacy files alone.
2. The editable DOCX/LaTeX manuscript source is absent in the documented workflow.
3. Workbook creators, transformations and generation history remain unverified.
4. Population denominators and the actual 2022 standard weights remain to be obtained.
5. Plotting/mapping scripts and geographic boundary files remain unavailable.
6. The legacy SPV contains model warnings and does not establish valid final fits.
7. The 2015–2017 residence-area labels remain provisional; confirm them before
   modelling rural/urban associations. Raw source codes are preserved.

The rebuilt cohort and explicit selection rules support subsequent work; these
remaining gaps must stay visible in decisions and reporting.

## Preservation and updates

Keep original inputs and baseline snapshots unchanged. Put new national files in
versioned `data/raw/` directories with their own manifest; derived datasets belong
in `data/processed/`, and generated tables/figures/reports in `outputs/`.

Investigate verification failures instead of overwriting expected hashes. Distinguish
review findings, data-stage corrections and manuscript edits in the issue log.
Record software/platform versions for subsequent scientific analysis runs without
replacing historical T01/T02 environment evidence.
