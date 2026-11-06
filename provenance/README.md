# Research provenance and reproducibility

This directory documents the preserved T01 baseline, T02 source reconstruction, T03 rates and T04 mortality models.
It is shared through Git; large inputs and generated admission files are restored
separately on each machine. See the [main README](../README.md) for macOS and Windows
PowerShell setup and [the T02 audit](../Writeable/t02_data_audit.md) for findings.

## Confirmed original analysis package

On 6 November 2026, the author confirmed that only the supplied SAV, SPV and two
XLSX files were used for the original analysis. That package is complete; no other
original SAV is expected. The INEC annual files acquired in T02 are independent
validation inputs, not recovered missing original-analysis files. Uncertainty about
how the supplied data were prepared must not be described as a missing SAV.

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
| `t03/` | Population-source hashes, annual denominators, observed census weights, rates, intervals, sensitivity analyses and run metadata |

T02 downloaded the ten official annual INEC releases and available separate
2018–2024 dictionaries. Early-year SAV metadata and official syntax were also
inspected. These acquisitions supersede the T01 statement that all national source
files had not yet been acquired for validation. They were not additional files
reported as used in the original analysis. They do not establish how the supplied
8,249-record extract was prepared.

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
python -X utf8 scripts/extract_inec.py
python -X utf8 scripts/audit_admissions.py
python -X utf8 -m unittest discover -s tests -v
```

If PowerShell activation is blocked, replace `python` with
`.\.venv\Scripts\python.exe`. Without activation on macOS, replace it with
`./.venv/bin/python`. No execution-policy change is required to invoke Python
directly. Restore official INEC input files before running the default audit.
Thesis originals and baseline snapshots are required only for the optional
`python -X utf8 scripts/audit_admissions.py --compare-legacy` command, which
verifies them before comparing the cohorts.

Default runs write `t02/annual_counts.csv` and record
`legacy_comparison_status: "not_run"` with null legacy metrics in the audit
summary. Existing legacy reconciliation reports are preserved as historical
evidence; they are regenerated only by a successful `--compare-legacy` run.

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
4. T03 has obtained annual population denominators and actual 2022 census standard counts; their full provenance is in `t03/`. The original manuscript calculation history remains unverified.
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

## T03 rate evidence

See [the methods appendix](../Writeable/t03_rates_and_methods.md).
`population_manifest.csv` inside `t03/` fixes the two workbook versions by SHA-256.
Annual estimates and the observed census standard are separate sources; they are
not interchangeable. `annual_standardized_rates.csv` includes both residence
policies and age schemes. `run_metadata.json` records input fingerprints.
T03 environment versions are in `t03/environment_freeze.txt`. The generated Table 3
is under `outputs/tables/` and can be regenerated using the main README commands.

## T04 mortality-model evidence

`provenance/t04/` records the pre-fit specification, explicit outcome cross-tabulation,
legacy SPV encoding, primary crude/adjusted ORs, sensitivity fits, rank/separation/
convergence checks, sparse-level profile intervals and environment versions.
The supplied SPV confirms its old internal event 1 was live discharge; the rebuilt
model explicitly uses death=1. Final LOS is secondary only, and unverified early
rural/urban labels are excluded from the primary fit. See the
[T04 report](../Writeable/t04_mortality_analysis.md) for interpretation and limitations.
Legacy evidence can be re-examined when the supplied SPV is restored; primary
model reproduction requires the audited cohort, not the original SPV.
