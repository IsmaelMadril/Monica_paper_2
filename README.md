# Malignant brain neoplasm hospitalizations in Ecuador

Research workspace for the 2015–2024 nationwide hospital-discharge manuscript.
The unit of analysis is an admission/discharge record. T02 reconstructed **10,972
admissions and 963 in-hospital deaths** from official INEC releases. Early-year
residence-area labels remain provisional; rates and models require recalculation.

Start with the [independent review](Writeable/current_state_review.md),
[revision task plan](Writeable/revision_task_plan.md),
[T02 audit](Writeable/t02_data_audit.md), and [provenance notes](provenance/README.md).

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
python -X utf8 scripts/freeze_inputs.py --verify
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
python -X utf8 scripts/freeze_inputs.py --verify
```

If `py` is unavailable, use the installed Python 3.14 executable to run
`-m venv .venv`. If PowerShell blocks `Activate.ps1`, activation is optional;
run the environment's interpreter directly without changing execution policy:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -X utf8 scripts/freeze_inputs.py --verify
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

## Restore the research inputs

A Git checkout does not contain the ignored inputs needed to reproduce the audit.
Restore these folders from your research backup, at the same relative paths:

- `Data_base/`: the supplied SAV and both workbooks.
- `Results/`: the supplied `RESULTADOS.spv`.
- `data/raw/baseline_2026-10-23/`: six preserved baseline snapshots.
- `data/raw/inec_2026-10-23/` and `data/raw/inec_discovery_2026-10-23/`:
  official downloads and archived release pages, if already available.

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
python -X utf8 scripts/acquire_inec.py
python -X utf8 scripts/acquire_early_dictionaries.py
```

The first command obtains the 2015–2024 releases and linked dictionaries. The
second obtains early-year syntax archives used to investigate missing labels.
Restoring archived downloads is preferable when reproducing the original audit;
files served by the website may change. Preserve existing manifests and compare
checksums before treating fresh downloads as the same source version.

## Reproduce the admission audit

After restoring the baseline inputs and acquiring/restoring the official sources:

```sh
python -X utf8 scripts/extract_inec.py
python -X utf8 scripts/audit_admissions.py
python -X utf8 -m unittest discover -s tests -v
```

The audited cohort is written to `data/processed/admissions_c71_audited.csv`.
Aggregate evidence and dictionaries are written to `provenance/t02/`.
Run extraction and auditing before the tests: cohort-integrity tests are skipped
if the generated cohort is absent, so a test run alone does not prove reconstruction.

The documented audit was executed on macOS. Windows instructions have been checked
against the scripts' path handling; execution on a Windows machine remains to be
verified. The test suite and checksum verification provide the checks to run there.

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
The original legacy extraction script, editable manuscript source, population
files and plotting/mapping code remain unavailable in the documented workflow.
The original workbook generation history is unverified. Confirm 2015–2017
residence-area labels before rural/urban association modelling.

Next is T03 rate recalculation, followed by model repair in T04/T05. T01 environment
records describe the historical baseline; T02 versions are recorded separately in
`provenance/t02/environment_freeze.txt`. Those records are provenance, not a virtual
environment to copy between machines.
