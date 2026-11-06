# Preserved research inputs

These instructions apply to macOS and Windows. Run commands from the project root
with that machine's own virtual environment active; see the
[main setup instructions](../../README.md).

## Folder contents

| Directory | Contents |
|---|---|
| `baseline_2026-10-23/` | Byte-for-byte snapshots of the six supplied research inputs |
| `inec_2026-10-23/` | Official annual INEC archives, dictionaries, syntax and extracted SAV files |
| `inec_discovery_2026-10-23/` | Archived release pages and discovered source links |

The dated directories identify the acquisition/baseline batch. Actual download
timestamps and source versions are documented in manifests. The supplied legacy
SAV/workbooks are distinct from the official annual INEC downloads.

## Restore on another machine

Copy the ignored raw-data directories from your research backup into `data/raw/`,
keeping all relative subdirectories and filenames, including spaces and accents.
Also restore original files under `Data_base/` and `Results/` as listed in the
[input manifest](../../provenance/input_manifest.csv). The original PDF and review
must match their baseline snapshots too.

Do not copy `.venv`; create it locally. Git does not contain these datasets or
snapshots, so cloning alone cannot restore the analysis. Keep files byte-identical:
opening and resaving a workbook, converting text line endings or recoding an input
can invalidate its checksum.

With the local environment active, verify the baseline on either operating system:

```sh
python -X utf8 scripts/freeze_inputs.py --verify
```

Without activation, use one of these alternatives from the project root:

macOS:

```sh
./.venv/bin/python -X utf8 scripts/freeze_inputs.py --verify
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts/freeze_inputs.py --verify
```

## Obtain official files if the archived downloads are unavailable

With the environment active, both systems use:

```sh
python -X utf8 scripts/acquire_inec.py
python -X utf8 scripts/acquire_early_dictionaries.py
```

Internet access and several GB of disk space are needed. Record and compare source
hashes: a newly served file may differ from the release originally audited. Preserve
the existing manifests before a new acquisition run. Baseline snapshots cannot be
recovered by these download scripts; restore those from your research backup.

## Preservation policy

Treat baseline snapshots and downloaded original archives as immutable. Do not
clean, recode or overwrite them. Put derived datasets in `data/processed/`.
The extraction script may create an extracted SAV beside its source archive;
that SAV is a local extraction product, not a replacement for the preserved ZIP.

Baseline hashes are recorded in `provenance/input_manifest.csv`; official-source
hashes are in `provenance/inec_download_manifest.csv` and
`provenance/inec_syntax_manifest.csv`. Investigate a mismatch instead of replacing
the expected hash. The preservation policy relies on checksums and careful handling,
not operating-system write protection.
