"""Create the reviewed-input baseline once, or verify its SHA-256 checksums.

Uses only the standard library. Existing snapshots/manifests are never overwritten.
"""
import argparse
import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'provenance/input_manifest.csv'
SOURCES = [
    ('Writeable/tumores encefalo Monica art completo.docx.pdf', 'reviewed_manuscript'),
    ('Writeable/review_issues.md', 'original_reviewer_comments'),
    ('Data_base/BASE DATOS TESIS.sav', 'supplied_spss_analytic_candidate'),
    ('Data_base/base monica encefalo.xlsx', 'supplied_workbook_role_unverified'),
    ('Data_base/base monica encefalo base para graficos.xlsx', 'plotting_workbook_candidate_unverified'),
    ('Results/RESULTADOS.spv', 'legacy_spss_output'),
]

def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def verify():
    with MANIFEST.open(newline='', encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    failures = []
    for row in rows:
        for key in ('source_path', 'snapshot_path'):
            path = ROOT / row[key]
            if not path.is_file() or digest(path) != row['sha256']:
                failures.append(row[key])
    if failures:
        raise SystemExit('Missing/changed inputs: ' + ', '.join(failures))
    print(f'Verified {len(rows)} original inputs and {len(rows)} snapshots.')


def freeze():
    if MANIFEST.exists():
        raise SystemExit('Baseline already exists. Use --verify; do not overwrite it.')
    # Fail before copying if any source is absent or a target already exists.
    snapshot_root = ROOT / 'data/raw/baseline_2026-10-23'
    for relative, _ in SOURCES:
        if not (ROOT / relative).is_file():
            raise SystemExit(f'Missing source: {relative}')
        if (snapshot_root / relative).exists():
            raise SystemExit(f'Snapshot already exists: {relative}')
    captured = datetime.now(timezone.utc).isoformat()
    rows = []
    for relative, role in SOURCES:
        source = ROOT / relative
        target = snapshot_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        checksum = digest(source)
        if digest(target) != checksum:
            raise SystemExit(f'Copy verification failed: {relative}')
        rows.append(dict(source_path=relative, snapshot_path=target.relative_to(ROOT).as_posix(),
                         role=role, size_bytes=source.stat().st_size, sha256=checksum,
                         source_modified_utc=datetime.fromtimestamp(source.stat().st_mtime, timezone.utc).isoformat(),
                         captured_utc=captured, source_release='unknown; supplied local version'))
    MANIFEST.parent.mkdir(exist_ok=True)
    with MANIFEST.open('x', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    verify()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    verify() if args.verify else freeze()
