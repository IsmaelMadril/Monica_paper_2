"""Extract C71.0–C71.9 discharge records, preserving source row identity and coding."""
from pathlib import Path
import io,json,zipfile,hashlib
import pandas as pd
import pyreadstat
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/raw/inec_2026-10-23'
OUT=ROOT/'data/processed/inec_c71'
OUT.mkdir(parents=True,exist_ok=True)
PROV=ROOT/'provenance/t02';PROV.mkdir(exist_ok=True)
FIELDS=['prov_ubi','area_ubi','sector','sexo','cod_edad','edad','etnia','prov_res','area_res','anio_ingr','mes_ingr','dia_ingr','anio_egr','mes_egr','dia_egr','dia_estad','con_egrpa','cau_cie10','entidad','tipo','clase']

def find_sav(data,trail=''):
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  for n in z.namelist():
   if n.lower().endswith('.sav') and ('egre' in n.lower() or 'eeh' in n.lower()):return z.read(n),trail+n
  for n in z.namelist():
   if n.lower().endswith('.zip') and ('egre' in n.lower() or 'eeh' in n.lower()):
    result=find_sav(z.read(n),trail+n+'!')
    if result:return result
 return None

flows=[]
for year in range(2015,2025):
 out=OUT/f'{year}.csv'
 if out.exists():
  flow=json.loads((PROV/f'{year}_flow.json').read_text())
  with out.open('rb') as stream: current=hashlib.file_digest(stream,'sha256').hexdigest()
  if flow.get('extract_sha256')==current:
   flows.append(flow);print(year,'verified cache',flush=True);continue
 paths=[p for p in (RAW/str(year)).glob('*.zip') if 'dic' not in p.name.lower() and 'sintaxis' not in p.name.lower()]
 if not paths:print(year,'missing release',flush=True);continue
 found=find_sav(paths[0].read_bytes())
 if not found:print(year,'missing SAV member',flush=True);continue
 data,member=found
 sav=RAW/str(year)/'extracted_egresos.sav'
 if not sav.exists():sav.write_bytes(data)
 del data
 _,m=pyreadstat.read_sav(str(sav),metadataonly=True)
 names={c.lower():c for c in m.column_names}
 fields=[names[c] for c in FIELDS if c in names]
 m.variable_value_labels['cau_cie10']={k:v for k,v in m.variable_value_labels.get('cau_cie10',{}).items() if str(k).replace('.','').startswith('C71')}
 (PROV/f'{year}_schema.json').write_text(json.dumps({'source_archive':paths[0].relative_to(ROOT).as_posix(),'archive_member':member,'number_rows':m.number_rows,'columns':m.column_names_to_labels,'value_labels':{c:m.variable_value_labels.get(names[c],{}) for c in FIELDS if c in names}},ensure_ascii=False,indent=2)+'\n')
 parts=[];offset=0;prefix=0;unknown=0
 for chunk,_ in pyreadstat.read_file_in_chunks(pyreadstat.read_sav,str(sav),chunksize=100000,usecols=fields,disable_datetime_conversion=True):
  chunk.columns=[c.lower() for c in chunk]
  codes=chunk.cau_cie10.astype('string').str.strip().str.upper().str.replace('.','',regex=False)
  mask=codes.str.fullmatch(r'C71[0-9]',na=False)
  prefix+=int(codes.str.startswith('C71',na=False).sum())
  unknown+=int(codes.isna().sum()+codes.eq('').sum())
  selected=chunk.loc[mask].copy()
  selected['source_row']=range(offset+1,offset+len(chunk)+1) if mask.all() else (mask.to_numpy().nonzero()[0]+offset+1)
  selected['icd10']=codes.loc[mask]
  selected['source_year']=year
  parts.append(selected);offset+=len(chunk)
 selected=pd.concat(parts,ignore_index=True)
 selected.to_csv(out,index=False)
 flow={'year':year,'source_records':offset,'c71_prefix_records':prefix,'eligible_c710_c719':len(selected),'other_or_unknown_diagnosis':offset-len(selected),'missing_diagnosis':unknown,'excluded_after_c71_selection':0,'extract_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
 (PROV/f'{year}_flow.json').write_text(json.dumps(flow,indent=2)+'\n');flows.append(flow)
 print(year,offset,'records;',len(selected),'eligible',flush=True)
pd.DataFrame(flows).to_csv(PROV/'selection_flow.csv',index=False)
