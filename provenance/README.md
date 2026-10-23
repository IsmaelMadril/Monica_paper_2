# T01 baseline and provenance

Baseline date: 23 October 2026. All six supplied research inputs have verified
local snapshots and SHA-256 hashes. `input_manifest.csv` records source paths,
snapshot paths, sizes, modification times, capture time and version uncertainty.
Modification times are filesystem metadata, not proof of a source release date.

Files:

- `input_manifest.csv`: preserved manuscript, original review, SAV, two workbooks
  and SPV output. The independent review and plan remain working documents.
- `artifact_lineage.csv`: provenance for all five tables and both figures,
  distinguishing observed SPSS commands from candidate or unknown routes.
- `workbook_inventory.json`: workbook sheet names; roles are not established by
  names alone. The workbook without “graficos” is an analytic candidate and the
  “base para graficos” workbook is a plotting candidate. Neither derivation is known.
- `legacy_spss_log.txt`: embedded XML log text from the supplied SPV, with the
  legacy absolute machine path redacted. This is evidence, not runnable syntax.
- `variable_dictionary.csv`: provisional definitions from the manuscript/logs;
  observed mappings do not establish valid data or annual coding consistency.
- `issue_resolution_log.csv`: all 22 original issues and 15 additional findings,
  plus T01 status. Review statuses are carried forward, not treated as verified fixes.
- `environment.json` and `environment_freeze.txt`: environment metadata and
  installed bootstrap package versions. T01 requires no third-party libraries.

## Known gaps for T02 and source recovery

1. Original annual INEC downloads, release versions and codebooks are absent.
2. Editable DOCX/LaTeX manuscript source is absent; only the supplied PDF is present.
3. Workbook creators, original formulas/transforms and generation history are unknown.
4. Population-denominator files and actual 2022 standard weights are absent.
5. Plotting/mapping scripts and map boundary files are absent.
6. The SPV records legacy commands but does not prove which dataset version was
   used for the manuscript or that its model fits were valid.

These gaps are explicitly recorded rather than inferred as established provenance.
The T01 workspace is ready; complete scientific reproducibility depends on resolving
these gaps during the subsequent work.

## Preservation policy

Keep original inputs and baseline snapshots unchanged. Do not run transformations
in place. Put newly acquired national files in a separate versioned `data/raw/`
subdirectory and maintain a separate manifest for them. Put derived datasets in
`data/processed/` and generated tables/figures/reports in `outputs/`.

Run `.venv/bin/python scripts/freeze_inputs.py --verify` before analysis. Any
mismatch stops verification; investigate it rather than overwriting the baseline.
The snapshot is protected by policy and checksum verification, not OS write protection.
