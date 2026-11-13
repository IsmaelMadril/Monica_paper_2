# Malignant brain neoplasm hospitalizations in Ecuador

Scientific and computational changes are documented in the
[bibliographic rationale](Writeable/reconstruction_rationale.md), with a
[decision/evidence register](provenance/reconstruction_decisions.csv) and
[BibTeX library](references/reconstruction.bib). Each subsequent substantive
revision must include its justification, exact source, local verification and
unresolved assumptions.

Research workspace for the 2015–2024 nationwide hospital-discharge manuscript.
The unit of analysis is an admission/discharge record. T02 reconstructed **10,972
admissions and 963 in-hospital deaths** from official INEC releases. Early-year
residence-area labels remain provisional. T03 has rebuilt resident-population rates;
T04 mortality modelling and T05 replacement analyses are complete for their documented
specifications. T06 descriptive tables and model legends are complete; T07 replacement sections/crosswalk and T08 narrative/evidence are prepared; full-paper integration remains open.

Start with the [independent review](Writeable/current_state_review.md),
[revision task plan](Writeable/revision_task_plan.md),
[T02 audit](Writeable/t02_data_audit.md), [T03 rates and methods](Writeable/t03_rates_and_methods.md),
and [provenance notes](provenance/README.md).

## Complete reproduction guide and missing CSV recovery

Use [README_REPRODUCTION.md](README_REPRODUCTION.md) for the complete macOS/Windows
workflow from a fresh checkout, required inputs and expected results.
`data/processed/admissions_c71_audited.csv` is ignored by Git and is created by
`audit_admissions.py`, after `extract_inec.py`. Cloning alone does not create it.
The guide also documents `scripts/restore_analysis_inputs.py`, which restores official
inputs from recorded URLs without replacing the source manifests.

## Original analysis files and validation sources

Author clarification, 6 November 2026: the supplied `BASE DATOS TESIS.sav`,
`RESULTADOS.spv`, and both XLSX workbooks are the complete set of data/output
files used for the original analysis. **No additional original SAV file is missing.**
The annual INEC files downloaded during T02 are additional validation sources;
they were not part of the supplied original analysis package. The 8,249-record
supplied cohort and 10,972-record reconstruction must be distinguished when
reporting or investigating their differences. Those differences concern dataset
contents and processing, not evidence of an absent SAV file.

## Requirements and moving between machines

Use Python **3.14** on both machines to match the environment used for the audit
(recorded version: 3.14.7). Dependencies are pinned in `requirements.txt`.
Windows commands below use **PowerShell** and the Python launcher `py`.

Create `.venv` separately on each machine. Virtual environments contain local
paths and platform-specific packages; do not copy or synchronize `.venv` between
macOS and Windows. Transfer code through Git and restore ignored research files
from a separate backup, preserving the folder layout and exact file bytes.

The scripts resolve project paths relative to their own location. Commands below
are run from the project root; replace example paths with your checkout location.
Use `python -X utf8` for project scripts and tests on both systems. Explicit UTF-8
mode keeps Spanish labels and text files consistent, including in Windows shells
whose default text encoding differs. UTF-8 mode does not itself change line endings.

## First setup on macOS

```sh
cd "/path/to/Monica_paper_2"
python3.14 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install -r requirements.txt
```

If your Python 3.14 installation exposes `python3` instead of `python3.14`, check
`python3 --version` and use `python3 -m venv .venv` to create the environment.

## First setup on Windows PowerShell

```powershell
Set-Location "C:\path\to\Monica_paper_2"
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install -r requirements.txt
```

If `py` is unavailable, use the installed Python 3.14 executable to run
`-m venv .venv`. If PowerShell blocks `Activate.ps1`, activation is optional;
run the environment's interpreter directly without changing execution policy:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

For any later command beginning with `python`, substitute
`.\.venv\Scripts\python.exe` when working without activation. On macOS the
equivalent direct interpreter is `./.venv/bin/python`.

## Returning to an existing environment

After opening a new terminal, change to the project root and activate the local
environment again:

macOS:

```sh
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

The remaining commands are identical in both shells once the environment is
active. Run `deactivate` to leave it. After pulling dependency changes, run
`python -m pip install -r requirements.txt` again in that machine's environment.

## Optional: restore thesis inputs for legacy comparison

The default INEC reconstruction does not require thesis originals or baseline
snapshots. Restore them only for the optional `--compare-legacy` audit.
A Git checkout does not contain these ignored thesis inputs.
Restore these folders from your research backup, at the same relative paths:

- `Data_base/`: the supplied SAV and both workbooks.
- `Results/`: the supplied `RESULTADOS.spv`.
- `data/raw/baseline_2026-10-23/`: six preserved baseline snapshots.

Keep the original manuscript PDF and `Writeable/review_issues.md` byte-identical
to the baseline as well. Git/editor line-ending conversion of a text input can
cause a checksum mismatch even when the visible text looks unchanged. Consult
[the input manifest](provenance/input_manifest.csv) for the exact files and hashes.
Do not regenerate the baseline to bypass a mismatch.

Verify the restored originals and snapshots:

```sh
python -X utf8 scripts/freeze_inputs.py --verify
```

This checks content hashes, not machine paths or file modification times. The
baseline already exists; running the script without `--verify` refuses to replace
its manifest. See [raw-data instructions](data/raw/README.md) for preservation.

## Download official sources when needed

These commands work in either shell with the local environment active and require
internet access. Allow several GB of disk space for ZIP archives and extracted SAV
files. The scripts use the existing dated acquisition directory; that date identifies
the project batch, while manifests record actual access timestamps.

```sh
python -X utf8 scripts/restore_analysis_inputs.py --download
```

This restores the official discharge/dictionary archives and population workbooks
from the committed manifest URLs, verifies hashes and preserves the manifests.
Optional early-year syntax restoration is covered in the complete reproduction guide.
Restoring archived downloads is preferable when reproducing the original audit;
files served by the website may change. Preserve existing manifests and compare
checksums before treating fresh downloads as the same source version.

## Reproduce the admission audit

After acquiring/restoring the official INEC sources (no `Data_base/` required):

```sh
python -X utf8 scripts/extract_inec.py
python -X utf8 scripts/audit_admissions.py
python -X utf8 -m unittest discover -s tests -v
```

The audited cohort is written to `data/processed/admissions_c71_audited.csv`.
Aggregate evidence and dictionaries are written to `provenance/t02/`, including
INEC-only `annual_counts.csv`. The summary records that the legacy comparison was
not run; previous legacy reports remain historical evidence. To regenerate them
after restoring the complete thesis baseline, run:

```sh
python -X utf8 scripts/audit_admissions.py --compare-legacy
```

Run extraction and auditing before the tests: cohort-integrity tests are skipped
if the generated cohort is absent, so a test run alone does not prove reconstruction.

The historical audit was executed on macOS. The INEC-only audit and all 26 tests
also passed on Windows with the existing local Python 3.13.7 environment on
6 November 2026. The optional comparison with actual legacy files was not rerun
on Windows because those originals were unavailable.

## Project layout

| Path | Purpose |
|---|---|
| `Writeable/` | Manuscript PDF, reviews, revision plan and T02 audit |
| `Data_base/` | Preserved legacy SAV and workbooks; ignored by Git |
| `Results/` | Legacy SPSS viewer output; SPV files ignored by Git |
| `data/raw/` | Preserved baseline, downloaded national releases and release pages |
| `data/processed/` | Generated admission extracts; ignored by Git |
| `provenance/` | Hashes, dictionaries, lineage, issue log and audit evidence |
| `scripts/` | Acquisition, extraction, auditing and preservation scripts |
| `tests/` | Recoding boundaries and cohort-integrity checks |
| `outputs/` | Generated tables, figures and reports; products ignored by Git |

## Current limits and next work

The official annual files and available dictionaries have been acquired in T02.
The original data preparation steps, editable manuscript source and plotting/mapping
code remain incompletely documented or unavailable. T03 population inputs have been
acquired and can be restored as described in the reproduction guide.
The original workbook generation history is unverified. Confirm 2015–2017
residence-area labels before rural/urban association modelling.

T03 rates, T04 mortality modelling and T05 replacement analyses are complete for their
documented specifications. T06 descriptive tables and legends are complete; T07 replacement sections are drafted; full-paper integration remains open. T02 early residence-area labels still require confirmation. T01 environment
records describe the historical baseline; T02 versions are recorded separately in
`provenance/t02/environment_freeze.txt`. Those records are provenance, not a virtual
environment to copy between machines.

## Reproduce T03 rates

With the local environment active on macOS or Windows PowerShell, and the T02
audited cohort already generated:

```sh
python -m pip install -r requirements.txt
python -X utf8 scripts/acquire_population.py
python -X utf8 scripts/prepare_population.py
python -X utf8 scripts/calculate_rates.py
python -X utf8 -m unittest discover -s tests -v
```

Population acquisition requires internet access only for absent files; existing
source hashes are verified. Restore `data/raw/population_2026-11-06/` from backup
to reproduce the exact acquired versions. Source hashes and derived rate evidence
are under `provenance/t03/`; the primary table is generated as
`outputs/tables/table3_rebuilt.md` and `.csv`. T03 uses 10,969 resident discharges
(three foreign-resident live discharges excluded) and keeps an all-discharge
sensitivity analysis. These national rates do not depend on rural/urban labels.

## Reproduce T04 mortality associations

After generating the audited cohort, with the local environment active:

```sh
python -m pip install -r requirements.txt
python -X utf8 scripts/fit_mortality.py
python -X utf8 scripts/profile_sparse_mortality.py
python -X utf8 -m unittest discover -s tests -v
```

To re-examine the original SPV when restored, run
`python -X utf8 scripts/inspect_legacy_mortality.py`. This optional examination is
separate from the rebuilt model. See [the T04 report](Writeable/t04_mortality_analysis.md)
and `provenance/t04/analysis_specification.md`. Generated Table 4 is in
`outputs/tables/table4_rebuilt.md` and `.csv`. The primary event is death=1; final
LOS and unverified early residence-area labels are excluded from the primary fit.
T04 includes sensitivities and sparse-level profile intervals. The new T04 stage
has been executed on macOS; it has not yet been verified on Windows.

## Reproduce T05 coding and anatomical-group analyses

With the audited cohort available and the local environment active:

```sh
python -m pip install -r requirements.txt
python -X utf8 scripts/fit_anatomy.py
python -X utf8 -m unittest discover -s tests -v
```

The two primary binary models separate non-C719 coding from the conditional
infratentorial/midline-versus-supratentorial comparison; they replace the old
multinomial Table 5 and report aORs, not aRRRs. Overlapping/unspecified records
remain descriptive, with exact exclusions in the conditional-site model. See the
[T05 report](Writeable/t05_anatomy_analysis.md), pre-fit specification and evidence
in `provenance/t05/`. Primary references include age18–44, male, private and year2015.
The script runs the sensitivities and sparse profile intervals, then generates
`outputs/tables/table5_rebuilt.md` and `.csv`. No new package is required beyond
the pinned environment. T05 was tested on macOS; Windows execution of this new
stage remains to be verified.

## Reproduce T06 descriptive tables and model legends

After creating the audited cohort and executing T04 and T05, run the same commands
on macOS or Windows PowerShell with the local virtual environment active:

```sh
python -X utf8 scripts/generate_descriptive_tables.py
python -X utf8 -m unittest discover -s tests -v
```

This produces Tables 1–2 and refreshes Tables 4–5 presentation without refitting
models. Read the [T06 report](Writeable/t06_descriptive_tables.md) for denominators,
restricted residence comparisons, sparse-cell testing and validation. Readable
review copies and evidence are tracked in `provenance/t06/`; regenerated products
are in `outputs/tables/`. This stage was executed on macOS; Windows is untested.

## T07 manuscript replacement sections

Read the [T07 revision notes](Writeable/t07_revision_notes.md),
[editable Word sections](Writeable/t07_manuscript_sections.docx),
[version-controlled section text](Writeable/t07_manuscript_sections.md) and
[STROBE/RECORD crosswalk](Writeable/t07_reporting_crosswalk.md). These replace
the title, abstract, framing and Methods; they are not an integrated full paper.
T08–T09 must update the remaining narrative/figures before T07 can close its
whole-paper consistency criterion. Ethics and author declarations remain T10.

After T02–T06, regenerate text and the numeric ledger on either system with:

```sh
python -X utf8 scripts/prepare_t07_sections.py
```

Optional Word export uses `requirements-documents.txt` and `--docx`; see the
[reproduction guide](README_REPRODUCTION.md). No analysis dependency changed.

## T08 interpretation and evidence audit

The [T08 replacement Introduction Discussion and Conclusion](Writeable/t08_interpretation_sections.docx)
and [evidence ledger](Writeable/t08_evidence_ledger.md) align interpretation with
executed results and verified source claims. See [revision notes](Writeable/t08_revision_notes.md)
for source-access limits, the exact GLOBOCAN edition and remaining integration.
The new narrative is complete for its stated scope; T07 whole-paper integration,
T09 figures and T10 author/submission verification remain open.

```sh
python -X utf8 scripts/prepare_t08_sections.py
```

This works from tracked aggregate evidence after T02–T07 and requires no network
or model refits. `--docx` uses optional `requirements-documents.txt`. The archived
IARC fact sheet is preserved with its hash rather than fetched on every run.

## T09 publication figures and geographic reporting

Read [T09 figure methods](Writeable/t09_figures_and_geography.md) and
[figure legends](Writeable/t09_figure_legends.md). Figure 1 reproduces Table 3 rates;
Figure 2 shows residence-province counts with full labels. Supplement S1 contains
ten yearly maps, and S2 distinguishes treating-facility province counts. All are
exported as PDF/SVG; main PNGs are 600 dpi at 180 mm width.

After T02/T03 with the local environment active on macOS or Windows:

```sh
python -m pip install -r requirements-figures.txt
python -X utf8 scripts/generate_figures.py
python -X utf8 -m unittest discover -s tests -v
```

Fixed boundaries/metadata are tracked under `provenance/t09/`, so ordinary figure
generation is offline. Plotting dependencies are optional and separate from core
analysis. Full exports are in `outputs/figures/`; tracked review previews and
reconciled data are in `provenance/t09/`. T09 is complete; T07 whole-paper
integration and T10 author/submission checks remain open.
