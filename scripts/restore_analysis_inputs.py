"""Verify or download official analysis inputs using the committed manifests.

Never changes manifests or overwrites existing files. Original supplied research
files and baseline snapshots must be restored separately from your backup.
"""
import argparse
import csv
import hashlib
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFESTS = ['provenance/inec_download_manifest.csv', 'provenance/t03/population_manifest.csv']


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read_entries(root, manifests):
    entries = {}
    for relative in manifests:
        with (root / relative).open(encoding='utf-8-sig', newline='') as stream:
            for row in csv.DictReader(stream):
                path = root / row['path']
                if not path.resolve().is_relative_to((root / 'data/raw').resolve()):
                    raise ValueError(f'Input path outside data/raw: {row["path"]}')
                if row['path'] in entries and entries[row['path']]['sha256'] != row['sha256']:
                    raise ValueError(f'Conflicting manifest checksums: {row["path"]}')
                entries[row['path']] = row
    return list(entries.values())


def ensure_file(root, row, download=False):
    path = root / row['path']
    if path.exists():
        if sha256(path) != row['sha256']:
            raise ValueError(f'CHECKSUM MISMATCH: {row["path"]}; existing file preserved')
        return 'verified'
    if not download:
        return 'missing'
    # Delay third-party import so checking existing files works with Python alone.
    import requests
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with requests.get(row['url'], stream=True, timeout=(30, 180)) as response:
            response.raise_for_status()
            digest = hashlib.sha256()
            with tempfile.NamedTemporaryFile(dir=path.parent, prefix='download_', suffix='.part', delete=False) as stream:
                temporary = Path(stream.name)
                for chunk in response.iter_content(chunk_size=1024*1024):
                    if chunk:
                        digest.update(chunk)
                        stream.write(chunk)
        if digest.hexdigest() != row['sha256']:
            raise ValueError(f'DOWNLOAD CHECKSUM MISMATCH: {row["path"]}; downloaded bytes not accepted')
        # Exclusive destination creation prevents accidental replacement of another input.
        with path.open('xb') as target, temporary.open('rb') as source:
            import shutil
            shutil.copyfileobj(source, target)
        return 'downloaded and verified'
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--download', action='store_true', help='Download absent files; existing files are only verified')
    parser.add_argument('--manifest', action='append', help='Repository-relative manifest path; repeatable. Defaults: T02 releases + T03 population')
    args = parser.parse_args()
    entries = read_entries(ROOT, args.manifest or DEFAULT_MANIFESTS)
    failures = []
    for row in entries:
        try:
            status = ensure_file(ROOT, row, args.download)
            print(f'{status}: {row["path"]}', flush=True)
            if status == 'missing':
                failures.append(row['path'])
        except Exception as error:
            print(f'ERROR: {error}', flush=True)
            failures.append(row['path'])
    if failures:
        raise SystemExit(f'{len(failures)} required input(s) unavailable or invalid. Restore exact archives from backup or use --download for absent files. Manifests were not changed.')
    print(f'All {len(entries)} official inputs verified; manifests unchanged.')


if __name__ == '__main__':
    main()
