"""Archive the exact geoBoundaries layer selected for T09; never overwrite expected hashes."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import requests

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'provenance/t09'
API='https://www.geoboundaries.org/api/current/gbOpen/ECU/ADM1/'
URL='https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/9469f09592ced973a3448cf66b6100b741b64c0d/releaseData/gbOpen/ECU/ADM1/geoBoundaries-ECU-ADM1_simplified.geojson'

def digest(content):
    return hashlib.sha256(content).hexdigest()

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest=OUT/'boundary_manifest.json'
    if manifest.exists():
        saved=json.loads(manifest.read_text())
        for item in saved['files']:
            path=ROOT/item['path']
            if not path.exists():
                response=requests.get(item['url'],timeout=60);response.raise_for_status()
                if digest(response.content)!=item['sha256']:raise ValueError('Boundary restoration hash mismatch')
                path.write_bytes(response.content)
            if digest(path.read_bytes())!=item['sha256']:raise ValueError('Boundary artifact changed; preserve manifest and inspect')
        print('Existing boundary sources verified; manifest unchanged.')
        return
    metadata=requests.get(API,timeout=60);metadata.raise_for_status();meta=metadata.json()
    response=requests.get(URL,timeout=60);response.raise_for_status()
    if digest(response.content)!='ddab55b98606edc09fe603eaf88e6205533fffd496d85c2dee03e345aed33c95':raise ValueError('Content does not match pinned Git LFS object hash')
    geo=response.json()
    if geo.get('type')!='FeatureCollection' or len(geo['features'])!=24:raise ValueError('Expected 24 province features')
    if meta['boundaryID']!='ECU-ADM1-780006' or meta['boundaryYearRepresented']!='2011':raise ValueError('Current API changed; inspect before selecting a source')
    items=[]
    for name,url,content in [('boundary_metadata.json',API,metadata.content),('ecuador_adm1.geojson',URL,response.content)]:
        path=OUT/name;path.write_bytes(content)
        items.append(dict(path=path.relative_to(ROOT).as_posix(),url=url,sha256=digest(content),bytes=len(content)))
    result=dict(accessed_date='2026-11-13',recorded_utc=datetime.now(timezone.utc).isoformat(),
                files=items,boundary_id=meta['boundaryID'],represented_year='2011',
                source=meta['boundarySource'],source_license=meta['boundaryLicense'],
                repository_commit='9469f09592ced973a3448cf66b6100b741b64c0d',crs='GeoJSON longitude latitude WGS84',
                use='Fixed cartographic context for all ten years, not validated annual historical boundaries',
                attribution='geoBoundaries / William & Mary geoLab; source metadata credits Wikimedia Commons')
    manifest.write_text(json.dumps(result,indent=2)+'\n')
    print('Archived 24-province fixed boundary layer and exact source metadata.')

if __name__=='__main__':main()
