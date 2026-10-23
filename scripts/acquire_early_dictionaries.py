"""Preserve official early-year syntax archives to recover omitted SAV value labels."""
import csv,hashlib,json
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlsplit,unquote
import requests
ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'provenance/inec_syntax_manifest.csv'
rows=[]
for y in [2015,2016,2017]:
 links=json.loads((ROOT/f'data/raw/inec_discovery_2026-10-23/{y}_links.json').read_text())
 urls=[u for u in links if u.lower().endswith('.zip') and 'sintaxis' in u.lower() and ('egre' in u.lower() or 'eeh' in u.lower() or y==2015)]
 for url in urls:
  p=ROOT/f'data/raw/inec_2026-10-23/{y}'/unquote(Path(urlsplit(url).path).name)
  if not p.exists():
   r=requests.get(url,timeout=60);r.raise_for_status();assert r.content.startswith(b'PK');p.write_bytes(r.content)
  rows.append({'year':y,'url':url,'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'accessed_utc':datetime.now(timezone.utc).isoformat()})
  print(y,p.name,flush=True)
with manifest.open('w',newline='') as f:
 w=csv.DictWriter(f,lineterminator='\n',fieldnames=rows[0]);w.writeheader();w.writerows(rows)
