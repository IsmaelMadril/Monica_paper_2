"""Download official SPSS releases and dictionaries linked by archived release pages."""
import csv, hashlib, json, re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, unquote
import requests
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/raw/inec_2026-10-23'
RAW.mkdir(exist_ok=True)
DISC=ROOT/'data/raw/inec_discovery_2026-10-23'
DISC.mkdir(exist_ok=True)
for year in range(2015,2024):
    page=f'https://www.ecuadorencifras.gob.ec/camas-y-egresos-hospitalarios-{year}/'
    target=DISC/f'{year}_links.json'
    if not target.exists():
        response=requests.get(page,timeout=40);response.raise_for_status()
        (DISC/f'{year}.html').write_text(response.text)
        from html.parser import HTMLParser
        class Links(HTMLParser):
            def __init__(self):super().__init__();self.links=[]
            def handle_starttag(self,tag,attrs):
                for k,v in attrs:
                    if k in ('href','src') and v:self.links.append(v)
        parser=Links();parser.feed(response.text)
        target.write_text(json.dumps(sorted(set(parser.links)),indent=2))
# The current operation page hosts the 2024 release.
u='https://www.ecuadorencifras.gob.ec/camas-y-egresos-hospitalarios/'
r=requests.get(u,timeout=40);r.raise_for_status()
(DISC/'2024.html').write_text(r.text)
links=sorted(set(re.findall(r'''(?:href|src)=["']([^"']+)["']''',r.text)))
(DISC/'2024_links.json').write_text(json.dumps([x for x in links if '/2024/' in x],indent=2))
records=[]
for year in range(2015,2025):
 links=json.loads((DISC/f'{year}_links.json').read_text())
 candidates=[x for x in links if x.lower().endswith('.zip') and ('spss' in x.lower() or 'bdd_' in x.lower()) and not any(k in x.lower() for k in ['csv','_r.zip','camas_hosp'])]
 if not candidates:
  print(year,'NO DATA LINK',flush=True);continue
 selected=[('data',candidates[0])]+[('dictionary',x) for x in links if x.lower().endswith('.zip') and ('diccionario' in x.lower() or 'dicionario' in x.lower())]
 for kind,url in selected:
  path=RAW/str(year)/unquote(Path(urlsplit(url).path).name)
  path.parent.mkdir(exist_ok=True)
  try:
   if not path.exists():
    response=requests.get(url,timeout=(25,180));response.raise_for_status()
    if not response.content.startswith(b'PK'):raise ValueError('Not a ZIP archive')
    path.write_bytes(response.content)
   records.append(dict(year=year,kind=kind,url=url,path=path.relative_to(ROOT).as_posix(),size_bytes=path.stat().st_size,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),accessed_utc=datetime.now(timezone.utc).isoformat()))
   print(year,kind,path.stat().st_size,flush=True)
  except Exception as exc: print(year,kind,'FAILED',str(exc),flush=True)
 with (ROOT/'provenance/inec_download_manifest.csv').open('w',newline='') as stream:
  writer=csv.DictWriter(stream,lineterminator='\n',fieldnames=['year','kind','url','path','size_bytes','sha256','accessed_utc']);writer.writeheader();writer.writerows(records)
