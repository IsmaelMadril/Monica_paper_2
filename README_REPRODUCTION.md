# Reproduce the analysis on macOS or Windows

The [bibliographic rationale](Writeable/reconstruction_rationale.md) explains
the scientific choices behind these commands; the
[decision register](provenance/reconstruction_decisions.csv) links each change
to its sources and validation. Preserved inputs, scripted transformations and
software records follow the reproducibility principles discussed by
[Sandve et al. (2013)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285).
SHA-256 checks detect changed bytes under the
[NIST Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final);
they do not establish scientific validity. Making legacy comparisons optional
is a project implementation choice, not a requirement of either reference.

This guide reproduces the implemented **T01–T06 workflow**: input verification,
C71 admission reconstruction, data audit, age-adjusted rates, mortality modelling,
separate coding/anatomical-group analyses and descriptive tables. T07 replacement sections are drafted and T08 replacement narrative/evidence is complete; T09 figures are complete; whole-paper integration and T10 remain pending. Run commands from the
repository root and stop when a command reports an error.

## Immediate fix: `admissions_c71_audited.csv` is missing

`data/processed/admissions_c71_audited.csv` is a **generated file**, excluded by
`.gitignore`. A fresh Git checkout normally does not contain it. Its absence on
your second workstation does not mean an original SAV is missing.

With your local environment active and the official INEC inputs restored as
explained below, run (the thesis `Data_base/` folder is not required):

```sh
python -X utf8 scripts/extract_inec.py
python -X utf8 scripts/audit_admissions.py
```

**`audit_admissions.py` creates the missing CSV.** `extract_inec.py` creates its ten
annual inputs under `data/processed/inec_c71/`; extraction alone does not create
the final CSV. Do not start `calculate_rates.py` before these commands succeed.

If official archives are missing, follow steps 1, 3, 4 and 5 below.
Step 2 is optional and applies only to legacy comparisons.
If all ten verified annual extracts and the official archives are already restored,
rerunning only `audit_admissions.py` is sufficient to recreate the final CSV.

## 1. Get the code and create a local Python environment

Clone/pull the same repository revision on both machines. Open a terminal in the
folder containing `requirements.txt` and `scripts/`. The example paths below are
placeholders; replace them with your checkout location.

Use Python **3.14** to match the recorded environment (3.14.7). Build `.venv` locally
on each machine; never copy it from macOS to Windows or vice versa. Install the
pinned packages with `requirements.txt`.

### macOS Terminal

```sh
cd "/path/to/Monica_paper_2"
python3.14 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install -r requirements.txt
python -m pip check
```

If the installed Python 3.14 is named `python3`, check `python3 --version` and use
`python3 -m venv .venv`. For an existing local environment, activate it instead of
creating it again.

### Windows PowerShell

```powershell
Set-Location "C:\path\to\Monica_paper_2"
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python --version
python -m pip install -r requirements.txt
python -m pip check
```

If `py` is unavailable, use your installed Python 3.14 executable to create the
environment. If PowerShell blocks activation, invoke Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

For every later command starting with `python`, use
`.\.venv\Scripts\python.exe` when working without activation. The macOS equivalent
is `./.venv/bin/python`. No execution-policy change is needed to invoke Python.

All subsequent `python` commands below work in either shell with the environment
active. `-X utf8` ensures consistent handling of Spanish labels. Quote paths that
contain spaces. Do not run the analysis with `python -O`: its validation uses
assertions, which optimized Python would disable.

## 2. Optional: restore originals for legacy comparison

Skip this step for INEC reconstruction and T03 rates. It is required only for
`audit_admissions.py --compare-legacy`, which verifies the complete thesis baseline.

The original analysis package consists of the supplied SAV, SPV and two XLSX
files. **No additional original SAV is expected.** The PDF and reviewer comments
are also part of the six-file preserved baseline.

| Original path required by baseline verification | Role |
|---|---|
| `Data_base/BASE DATOS TESIS.sav` | Supplied 8,249-record legacy dataset |
| `Data_base/base monica encefalo.xlsx` | Supplied analysis workbook |
| `Data_base/base monica encefalo base para graficos.xlsx` | Supplied plotting workbook |
| `Results/RESULTADOS.spv` | Supplied SPSS output |
| `Writeable/tumores encefalo Monica art completo.docx.pdf` | Reviewed manuscript |
| `Writeable/review_issues.md` | Original reviewer comments |

Each also needs its byte-identical snapshot at:

```text
data/raw/baseline_2026-10-23/<the same original relative path>
```

For example, the SAV snapshot is:

```text
data/raw/baseline_2026-10-23/Data_base/BASE DATOS TESIS.sav
```

Restore the original files and matching snapshot tree from your research backup,
using Finder or File Explorer if preferred. Preserve exact filenames, accents,
folder names and file bytes. Some baseline PDF/review/SPV files are tracked in
this repository revision; the SAV and workbook copies are not. Check actual files
on the second machine rather than assuming the whole baseline came with Git.

The authoritative list is [provenance/input_manifest.csv](provenance/input_manifest.csv).
Once restored, run:

```sh
python -X utf8 scripts/freeze_inputs.py --verify
```

Expected message:

```text
Verified 6 original inputs and 6 snapshots.
```

Do not run `freeze_inputs.py` without `--verify` to fix this problem: the baseline
is already established. A checksum failure requires restoring the matching bytes,
not replacing the expected hash. Windows Git/editor line-ending conversion can
change `review_issues.md` even when its visible text appears identical. Restore
that file from the byte-identical backup if this occurs.

## 3. Restore the official T02 and T03 sources

These files were acquired for validation/reanalysis. They are separate from the
complete supplied original analysis package and are excluded from Git.

| Folder | Required content |
|---|---|
| `data/raw/inec_2026-10-23/<year>/` | Official 2015–2024 discharge ZIPs and linked dictionary ZIPs listed in the T02 manifest |
| `data/raw/population_2026-11-06/` | Two population/census XLSX files listed in the T03 manifest |

**Preferred:** copy the archived files from the working workstation or research
backup, preserving the directory structure. ZIPs are enough for extraction; the
large `extracted_egresos.sav` files can be regenerated. Allow several GB of free
disk space for extracted national files and intermediate data.

Verify the exact 19 official input files without downloading or changing manifests:

```sh
python -X utf8 scripts/restore_analysis_inputs.py
```

If some official files are absent and internet access is available:

```sh
python -X utf8 scripts/restore_analysis_inputs.py --download
```

This helper uses the URLs already recorded in:

- `provenance/inec_download_manifest.csv` — 17 discharge/dictionary archives.
- `provenance/t03/population_manifest.csv` — 2 population/census workbooks.

It downloads only absent files, verifies SHA-256, refuses mismatched existing
files, and leaves manifests unchanged. If an official server now supplies different
bytes or a URL fails, restore the exact archived version from backup. A downloaded
file with a different hash is not accepted as the original source version.

The older `acquire_inec.py` discovers releases from web pages and rewrites its
manifest. It is an acquisition tool, **not the preferred way to reproduce the fixed
source versions**. Use the manifest-based helper above for another workstation.
Archived discovery HTML/JSON is not required by the extraction and audit scripts.

### Optional: restore early-year syntax evidence

These archives document the T02 label investigation; they are not required to
create the admission CSV or calculate national T03 rates:

```sh
python -X utf8 scripts/restore_analysis_inputs.py --download --manifest provenance/inec_syntax_manifest.csv
```

## 4. Extract the ten annual C71 datasets

```sh
python -X utf8 scripts/extract_inec.py
```

Required inputs: the ten annual discharge ZIPs from step 3. The script reads
nested ZIPs where needed and writes these annual C71 datasets:

```text
data/processed/inec_c71/2015.csv
...
data/processed/inec_c71/2024.csv
```

It also regenerates annual schemas, selection-flow records and extract checksums
under `provenance/t02/`. If a valid cached annual CSV exists, it is verified and
reused. If it is absent, it is reconstructed from its annual source archive.

Every year 2015–2024 must be present. Do not continue if the log contains
`missing release` or `missing SAV member`: the current extractor can finish after
reporting an absent year, but a partial extraction is not a successful reconstruction.

## 5. Build the missing audited admission CSV

```sh
python -X utf8 scripts/audit_admissions.py
```

This checks the official archive and annual-extract hashes, applies the explicit
recodes and writes the INEC cohort independently of the supplied thesis files:

```text
data/processed/admissions_c71_audited.csv
provenance/t02/audit_summary.json
provenance/t02/annual_counts.csv
```

The summary records `legacy_comparison_status: "not_run"` and null legacy metrics
unless a comparison was requested. Existing legacy reports remain historical
evidence and are not regenerated by the default run.

To reproduce the legacy comparison after completing optional step 2:

```sh
python -X utf8 scripts/audit_admissions.py --compare-legacy
```

This first verifies the six thesis originals and their snapshots, then also writes
`annual_reconciliation.csv`, `legacy_anatomy_audit.csv` and
`workbook_reconciliation.json`. The summary records `"completed"` and legacy
metrics only when this comparison succeeds.

Expected full cohort:

- **10,972 admissions** with unique source-year/source-row keys.
- **963 deaths**, **10,009 live discharges**.
- All years 2015–2024; no patient-level deduplication.

The reconstructed cohort is distinct from the supplied 8,249-record SAV. Do not
rename the SAV or export a different CSV under the expected filename to bypass
this generation step.

Check that the file was generated (same command on both systems):

```sh
python -X utf8 -c "from pathlib import Path; p=Path('data/processed/admissions_c71_audited.csv'); print(p.resolve()); assert p.is_file(), 'Run audit_admissions.py first'"
```

## 6. Rebuild age-adjusted rates and Table 3

The two source population workbooks must have passed step 3.

```sh
python -X utf8 scripts/prepare_population.py
python -X utf8 scripts/calculate_rates.py
```

`prepare_population.py` produces annual population denominators and actual 2022
census weights. `calculate_rates.py` consumes those tables **and the audited CSV
created in step 5**. It does not create the admission cohort itself.

Primary rate outputs:

| Output | Contents |
|---|---|
| `outputs/tables/table3_rebuilt.md` | Readable rebuilt Table 3 |
| `outputs/tables/table3_rebuilt.csv` | Primary annual rate table |
| `provenance/t03/annual_standardized_rates.csv` | Both age schemes and residence policies, with confidence intervals |
| `provenance/t03/age_specific_rates.csv` | Age-specific numerators, denominators and rates |
| `provenance/t03/period_summary_rates.csv` | Mean annual and pooled population-year summaries |
| `provenance/t03/admission_fatality.csv` | Admission-level fatality percentages and intervals |
| `provenance/t03/run_metadata.json` | Input fingerprints and calculation choices |

Expected results for the preserved source versions:

| Control | Expected value |
|---|---:|
| Resident admissions used for primary population rates | 10,969 |
| Deaths in resident cohort | 963 |
| Foreign-resident live discharges excluded from primary rates | 3 |
| Observed 2022 census standard population | 16,938,986 |
| Mean annual hospitalization rate per 100,000 residents | 6.611238 |
| Mean annual in-hospital death rate per 100,000 residents | 0.598464 |
| Pooled resident admission fatality | 8.779287% |

Full methods, confidence-interval assumptions and sensitivities are in
[Writeable/t03_rates_and_methods.md](Writeable/t03_rates_and_methods.md).

## 7. Run validation after generating the data

```sh
python -X utf8 -m unittest discover -s tests -v
python -m pip check
```

Confirm that all tests run successfully **without skipped cohort/rate integration
tests**. A fresh checkout includes some aggregate rate evidence in Git, and the
tests skip certain checks if generated data are absent. Therefore a passing test
summary alone does not replace steps 4–6. Expected controls above must also match.

The missing-CSV recovery sequence was also tested in an isolated macOS workspace:
originals, official archives and the ten cached annual extracts were restored, while
`admissions_c71_audited.csv` was initially absent. Running steps 4–6 regenerated
the final CSV and both Table 3 files byte-for-byte identically to the working copy.
This checks cached-extract recovery; it does not claim a fresh website download or
an execution on Windows. The downloader's accepted/rejected checksum behavior is
covered by tests without accessing the network.

On 6 November 2026, the INEC-only audit and all 26 tests passed on Windows
using the existing local Python 3.13.7 environment and UTF-8 mode. Reconstruction
produced 10,972 admissions and 963 deaths without thesis originals or snapshots.
The optional comparison with actual legacy files was not rerun on Windows because
those originals were unavailable. The historical full workflow used Python 3.14.

## Short command sequence after environment setup

With the environment active, this sequence works in either shell. Run each command
only after the previous one succeeds:

```sh
python -X utf8 scripts/restore_analysis_inputs.py --download
python -X utf8 scripts/extract_inec.py
python -X utf8 scripts/audit_admissions.py
python -X utf8 scripts/prepare_population.py
python -X utf8 scripts/calculate_rates.py
python -X utf8 -m unittest discover -s tests -v
```

For offline reproduction, restore all official files first and omit `--download`
from the restoration command. The remainder requires no network access.

## Troubleshooting

| Error or observation | Cause and action |
|---|---|
| `FileNotFoundError: ... admissions_c71_audited.csv` | Run extraction, then `audit_admissions.py` before calculating rates. Follow steps 3–5 if official inputs are missing. |
| Missing `data/processed/inec_c71/<year>.csv` | Restore the corresponding official ZIP and run `extract_inec.py`; confirm all ten years succeed. |
| `Missing/changed inputs: ...` | Optional legacy comparison/baseline verification failed. Restore the exact thesis files; the default INEC audit does not require them. Do not create a new baseline. |
| Missing `Data_base/BASE DATOS TESIS.sav` | Only `--compare-legacy` needs it. Run the default INEC audit, or restore the original and snapshot for comparison. |
| Missing `annual_population_by_age.csv` or `standard_weights_2022.csv` | Restore/verify the population XLSX files, then run `prepare_population.py`. |
| `CHECKSUM MISMATCH` or `DOWNLOAD CHECKSUM MISMATCH` | Input bytes differ from the preserved version. Existing files/manifests are not overwritten. Investigate or restore the matching backup. |
| `ModuleNotFoundError` | Activate the correct local `.venv`; run `python -m pip install -r requirements.txt`. |
| Python installer/package installation fails | Check Python version and workstation platform against the recorded Python 3.14 environment; retain pinned versions rather than silently upgrading scientific dependencies. |
| PowerShell blocks `Activate.ps1` | Use `.\.venv\Scripts\python.exe` directly for each command. |
| `UnicodeDecodeError` or corrupted Spanish labels | Run with `python -X utf8`; restore any already-corrupted inputs from backup. |
| Tests show `skipped` | Generate the cohort and rate outputs before rerunning integration tests. |
| `provenance/` files change after a run | Many are regenerated analysis evidence; inspect `git diff`. Timestamp/platform records can change. Content hashes/recorded results should be investigated if scientific inputs are unchanged. |

## Moving work between machines

Transfer code and documentation with Git. Transfer ignored originals, exact raw
archives and optional caches using your research backup. Derived CSVs and tables
can be regenerated; copying them is optional and does not replace verifying their
inputs. Keep `.venv` local to each machine. Preserve the committed manifests and
avoid automatic line-ending conversion of hashed original text inputs.

## T04: reproduce mortality modelling

After step 5 has created `admissions_c71_audited.csv`, install updated requirements
and run (the same commands in an active macOS or Windows environment):

```sh
python -m pip install -r requirements.txt
python -X utf8 scripts/fit_mortality.py
python -X utf8 scripts/profile_sparse_mortality.py
python -X utf8 -m unittest discover -s tests -v
```

The modelling stage uses the T02 cohort directly; T03 population denominators are
not model inputs. `fit_mortality.py` produces the primary Table 4 and seven sensitivity
fits, with diagnostics in `provenance/t04/`. `profile_sparse_mortality.py` adds
profile-likelihood intervals for six sparse primary categories. The original SPV
is not required to run the rebuilt model.

Optional legacy encoding examination, with `Results/RESULTADOS.spv` restored:

```sh
python -X utf8 scripts/inspect_legacy_mortality.py
```

If the supplied SPV is absent, that command reports its absence and preserves
historical encoding evidence. Its absence does not change the rebuilt numeric
death outcome. Tests specifically reading the original SPV can be skipped on a
workstation without it; this is distinct from skipping the cohort/model integration
tests, which must run after generating the analysis outputs.

Expected primary model: 10,972 admissions, 963 deaths, 27 full-rank parameters,
finite estimates and no separation or fitting warning. The model excludes final
LOS and provisional early-year residence-area labels. Age 80+ vs 0–17 has aOR
2.631358; public vs private sector has aOR 1.201195. These are adjusted admission-level
associations. See [the complete T04 methods/report](Writeable/t04_mortality_analysis.md)
for references, uncertainty and dependence limitations. New T04 execution has been
verified on macOS only; the previously documented Windows validation of T02/T03
does not establish Windows validation of this newly added model stage.

## T05: reproduce replacement Table 5

After step 5 has created `data/processed/admissions_c71_audited.csv`, use these
commands on macOS or Windows PowerShell with the local environment active:

```sh
python -m pip install -r requirements.txt
python -X utf8 scripts/fit_anatomy.py
python -X utf8 -m unittest discover -s tests -v
```

The script reads the audited cohort; T03 population files and T04 model outputs are
not runtime inputs. It reuses statistical helper functions from existing modules.
All T05 main and sensitivity fits plus sparse profile intervals run in one command.
If the optional supplied SPV is present, its NOMREG warning is exported; if absent,
historical evidence is preserved and fitting proceeds using the audited cohort.

Expected controls: coding panel10972 records/6304 non-C719 events; conditional-site
panel6192 records/1523 infratentorial-midline events; 16 parameters per primary
model; 15 converged finite fits overall; no binary separation; four certificates
explain why the full four-outcome ethnicity model has no finite maximum.
Primary pediatric-versus-age18-44 aORs are1.897457 (coding) and1.140529 (conditional
site). Do not label these as the original multinomial aRRRs. Temporal sensitivity
and selection limitations are material; consult the [T05 report](Writeable/t05_anatomy_analysis.md).

Generated outputs: `outputs/tables/table5_rebuilt.md` and `.csv`. Tracked evidence:
`provenance/t05/` including model flow, source cells, covariances, coefficients,
reference re-expressions, diagnostics and sensitivity/profile intervals. The new
T05 stage was executed on macOS; existing Windows validation of earlier stages
does not establish Windows validation of this stage.

## T06: reproduce Tables 1–2 and consistent model legends

Run the T02 audited-cohort build, T04 mortality fit and T05 anatomical analyses
first. T03 population/rate files are not T06 runtime inputs. These commands are
the same on macOS and Windows PowerShell after activating the local environment:

```sh
python -X utf8 scripts/fit_mortality.py
python -X utf8 scripts/profile_sparse_mortality.py
python -X utf8 scripts/fit_anatomy.py
python -X utf8 scripts/generate_descriptive_tables.py
python -X utf8 -m unittest discover -s tests -v
```

Skip the first three commands if their outputs already exist for exactly the
current audited cohort bytes. T06 checks those cohort hashes and saved diagnostics
and stops if they disagree; rerun the relevant model stage after recreating the
cohort on a different workstation. It refreshes presentation from saved
coefficients, without changing estimates or refitting. No original SAV/SPV/XLSX
is required for the rebuilt T06 stage.

Expected controls: 10,972 admissions, 963 deaths, 10,009 live discharges. All 17
characteristic blocks reconcile. Residence comparisons alone use 7,621 records
from verified 2018–2024 labels; 3,351 early records are excluded from those blocks.
2024: 1,019 admissions, 932 live, 87 deaths; live column share 9.31%, within-year
fatality 8.54%. Four sparse comparisons use 99,999 fixed-margin Monte Carlo draws;
13 use Pearson chi-square. Seeds, simulation resolution and uncertainty are saved.

Outputs: Markdown and numeric CSV for Tables 1, 2, 4 and 5 in `outputs/tables/`.
Tracked evidence: `provenance/t06/`, including readable copies of those four tables,
long-form numeric cells, denominator/missingness registers, independence tests,
reconciliation and code/input/environment metadata. The [T06 report](Writeable/t06_descriptive_tables.md)
explains conventions and remaining limits. Full local suite: 61 tests, no skips.
The new stage has been executed on macOS; Windows execution remains unverified.

## T07: reproduce revised title abstract and Methods

After T02–T06 outputs exist, with the project environment active on macOS or
Windows PowerShell:

```sh
python -X utf8 scripts/prepare_t07_sections.py
```

This uses the Python standard library to regenerate
`Writeable/t07_manuscript_sections.md`, `provenance/t07/numeric_traceability.json`
and `run_metadata.json`. The editable source is `Writeable/t07_sections_template.md`.
All 32 numeric entries retain exact source filters/aggregations and display rounding.
The generator checks cohort fingerprints against T04–T06 and exact LF/CRLF
equivalence against T03; it rejects content differences. No refits, downloads or
changes to historical manifests are performed. The locally found baseline Word
file is optional, separately fingerprinted when present, and never overwritten.

Optional Word export, on either operating system:

```sh
python -m pip install -r requirements-documents.txt
python -X utf8 scripts/prepare_t07_sections.py --docx
```

The Word output is `Writeable/t07_manuscript_sections.docx`. This optional document
dependency is separate from `requirements.txt`; it is not required for analysis
or Markdown generation. The distributed document was rendered and visually
checked on macOS with the bundled document runtime. New Windows text/Word
generation has not been executed. Word engines can change pagination, so verify
[the crosswalk](Writeable/t07_reporting_crosswalk.md) against the final layout.

See [T07 revision notes](Writeable/t07_revision_notes.md) for integration steps.
This is a seven-page replacement-section document, not a full manuscript; old
Results/Discussion/figures must be replaced in T08–T09, and author declarations
verified in T10. The T07 checkbox remains open until whole-paper consistency is checked.

## T08: reproduce interpretation sections

After T02–T07 evidence exists for the current cohort, use this command on macOS
or Windows PowerShell with the local environment active:

```sh
python -X utf8 scripts/prepare_t08_sections.py
```

Inputs include the T07 numeric ledger and fingerprints, T02–T06 aggregate results,
the tracked T08 claim/reference ledgers and the exact archived IARC Ecuador PDF.
No source acquisition, network request or statistical refit occurs. The original
baseline Word file is optional. The authoritative prose is
`Writeable/t08_sections_template.md`; output text is
`Writeable/t08_interpretation_sections.md`. Evidence and hashes are in `provenance/t08/`.

Optional Word export:

```sh
python -m pip install -r requirements-documents.txt
python -X utf8 scripts/prepare_t08_sections.py --docx
```

Expected: 44 numeric entries, 29 claim dispositions and a five-page Word section
document under the verified macOS renderer. All 24 original reference entries have
a recorded disposition. GLOBOCAN uses the frozen 2024 v1.0 Ecuador artifact labelled
September 2026, accessed 12 November 2026, not an unspecified current endpoint.

The [T08 notes](Writeable/t08_revision_notes.md) explain full-text versus abstract-only
access, removed claims and integration requirements. Word/Markdown content equality
and the five rendered page headings were checked; no new statistical tests or
refits were required for this prose task. The new stage was executed on macOS;
Windows execution and repagination remain unverified. T08 does not close T07's
whole-paper consistency criterion or supply the T09 figures/T10 declarations.

## T09: reproduce Figures 1–2 and supplementary geography

First build the audited cohort (T02) and Table 3/rates (T03). The T04–T08 models
and draft documents are not figure runtime inputs. From the repository root with
the local environment active, run the same commands on macOS and Windows PowerShell:

```sh
python -m pip install -r requirements.txt
python -m pip install -r requirements-figures.txt
python -X utf8 scripts/generate_figures.py
python -X utf8 -m unittest discover -s tests -v
```

Optional plotting packages are pinned separately; the core analysis requirements
are unchanged. The script uses a headless backend and a repository-local font
cache; no GUI is needed. Geometry, metadata and expected hashes are tracked.
Normal plotting performs no network requests. If a boundary artifact is absent,
restore from the recorded URL while keeping the manifest:

```sh
python -X utf8 scripts/acquire_figure_boundaries.py
```

Existing hashes are checked; the acquisition script never silently replaces an
established expected manifest. A Git LFS pointer file is not accepted as geometry.
Use the pinned source rather than a newly changed current API layer.

Expected controls: 100 primary rate/interval rows match Table 3; residence count
N=10,969 after three foreign-resident live exclusions; facility count N=10,972;
240 province-year cells per assignment; 24-to-24 boundary join; shared count scale
0–500. 2017 death rate=0.758166; 2024 total admission rate=5.783973 and unspecified
rate=2.152234 per 100,000 residents. Full suite: 72 tests, no skips after all
analysis/figure stages and dependencies are present. Figure tests explicitly skip
when optional plotting dependencies or prerequisite outputs are unavailable; that
is not equivalent to successful figure validation.

Exports in `outputs/figures/`: `figure1_rates`, `figure2_residence_counts` and
`figureS2_facility_counts` in PDF/SVG/600 dpi PNG; ten-page
`figureS1_residence_atlas.pdf` and individual annual SVG/300 dpi PNG previews.
Main figures are 180 mm wide. Tracked evidence/review previews are in
`provenance/t09/`; captions and limitations are in
[the figure legends](Writeable/t09_figure_legends.md). Read
[T09 methods](Writeable/t09_figures_and_geography.md) for residence/facility
meaning, code joins, boundary representation and uncertainty assumptions.

Verified on macOS; new Windows figure generation is untested. Reinspect labels at
the journal's final dimensions. T09 supplies figures, not an integrated submission
manuscript or verified author/ethics declarations.
