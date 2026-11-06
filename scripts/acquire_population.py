"""Acquire the fixed official sources used for T03; never overwrite a preserved hash."""
import csv, hashlib
from datetime import datetime, timezone
from pathlib import Path
import requests
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw/population_2026-11-06'
MANIFEST = ROOT / 'provenance/t03/population_manifest.csv'
SOURCES = [
    ('annual_denominators', 'https://www.ecuadorencifras.gob.ec/documentos/web-inec/Poblacion_y_Demografia/Proyecciones_Poblacionales/censo_2022/revision_2024_areas/Tabulados_Estimacion_Proyeccion_v2.xlsx', 'INEC Estimaciones y Proyecciones Revision 2024; expanded area workbook v2; sheet 1.1; June 30'),
    ('census_standard', 'https://www.censoecuador.gob.ec/wp-content/uploads/2024/04/01_2022_CPV_Estructura_poblacional.xlsx', 'INEC CPV 2022 Estructura poblacional; sheet 3; observed census counts'),
]

def main():
    RAW.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    old = {}
    if MANIFEST.exists():
        with MANIFEST.open(encoding='utf-8', newline='') as stream:
            old = {r['role']: r for r in csv.DictReader(stream)}
    rows = []
    for role, url, version in SOURCES:
        path = RAW / url.rsplit('/', 1)[1]
        if not path.exists():
            response = requests.get(url, timeout=(30, 180))
            response.raise_for_status()
            if not response.content.startswith(b'PK'):
                raise ValueError(f'Not an XLSX/ZIP: {url}')
            path.write_bytes(response.content)
        with path.open('rb') as stream:
            checksum = hashlib.file_digest(stream, 'sha256').hexdigest()
        if role in old:
            if old[role]['sha256'] != checksum:
                raise ValueError(f'Source hash changed for {role}; preserve original manifest and investigate')
            rows.append(old[role])
        else:
            rows.append(dict(role=role, url=url, path=path.relative_to(ROOT).as_posix(),
                             version=version, size_bytes=path.stat().st_size, sha256=checksum,
                             recorded_utc=datetime.now(timezone.utc).isoformat()))
        print(role, checksum)
    if not MANIFEST.exists():
        with MANIFEST.open('x', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)

if __name__ == '__main__':
    main()
