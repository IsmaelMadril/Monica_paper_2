"""Build T08 interpretation sections from audited evidence without network or model refits."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

from prepare_t07_sections import export_docx, select

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'provenance/t08'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--docx',action='store_true')
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    inputs={}
    t07=json.loads((ROOT/'provenance/t07/run_metadata.json').read_text())
    for name,expected in t07['inputs_sha256'].items():
        p=ROOT/name
        if not p.exists() and name.startswith('data/raw/baseline_'):
            continue  # The historical Word source is optional for reanalysis text.
        if digest(p)!=expected:
            raise ValueError('T07 evidence bytes changed; rebuild/review that stage: '+name)
        inputs[name]=digest(p)
    ledger=json.loads((ROOT/'provenance/t07/numeric_traceability.json').read_text())
    inputs['provenance/t07/numeric_traceability.json']=digest(ROOT/'provenance/t07/numeric_traceability.json')
    # Reuse the audited numeric sources, not an independently typed abstract value.
    def source(name):
        inputs[name]=digest(ROOT/name)
        with (ROOT/name).open(encoding='utf-8',newline='') as f:
            return list(csv.DictReader(f))
    def value(key,raw,name,locator,precision=3,count=False):
        ledger[key]=dict(source=name,locator=locator,raw_value=raw,
                         displayed=f'{int(raw):,}' if count else f'{float(raw):.{precision}f}')
    snapshot_path=ROOT/'provenance/t08/globocan_snapshot.json'
    snapshot=json.loads(snapshot_path.read_text())
    pdf=ROOT/snapshot['archived_path']
    if digest(pdf)!=snapshot['sha256']:
        raise ValueError('Archived IARC artifact hash mismatch')
    inputs[snapshot_path.relative_to(ROOT).as_posix()]=digest(snapshot_path)
    inputs[pdf.relative_to(ROOT).as_posix()]=digest(pdf)
    for key,field in [('iarc_cases','new_cases'),('iarc_deaths','deaths')]:
        value(key,snapshot[field],snapshot['archived_path'],
              f'GLOBOCAN {snapshot["estimate_year"]} version {snapshot["version"]}; page2 Brain CNS; '+field,count=True)
    name='provenance/t03/annual_standardized_rates.csv'
    rates=source(name)
    for year,anatomy,prefix in [(2019,'Total','rate_2019'),(2020,'Total','rate_2020'),(2024,'Unspecified','unspecified_rate_2024')]:
        row=select(rates,policy='resident',scheme='five_groups',year=year,anatomy=anatomy,measure='admissions')
        for suffix,field in [('', 'rate_per_100k'),('_lo','lower_95'),('_hi','upper_95')]:
            value(prefix+suffix,row[field],name,f'resident/five_groups/{year}/{anatomy}/admissions/{field}')
        if year==2024:
            value('unspecified_2024',row['events'],name,'resident/five_groups/2024/Unspecified/admissions/events',count=True)
    name='provenance/t02/selection_flow.csv'
    for year in [2017,2023]:
        row=select(source(name),year=year)
        value('count_'+str(year),row['eligible_c710_c719'],name,f'{year}/eligible_c710_c719',count=True)
    for name,filters,prefix in [
        ('provenance/t04/all_model_coefficients.csv',dict(model='primary',variable='sector_binary',level='Public'),'sector'),
        ('provenance/t05/all_model_coefficients.csv',dict(panel='coding',model='primary',variable='year',level='2024'),'coding_year'),
        ('provenance/t05/all_model_coefficients.csv',dict(panel='site',model='verified_years_core',variable='age_group',level='0-17'),'site_later')]:
        row=select(source(name),**filters)
        for suffix,field in [('_or','aor'),('_lo','lower_95'),('_hi','upper_95')]:
            value(prefix+suffix,row[field],name,str(filters)+'/'+field)
    template=ROOT/'Writeable/t08_sections_template.md'
    text=template.read_text(encoding='utf-8')
    used=set(re.findall(r'\{\{(\w+)\}\}',text))
    if used-set(ledger):
        raise ValueError('Unrecognized numeric placeholders: '+str(used-set(ledger)))
    for key in used:
        text=text.replace('{{'+key+'}}',ledger[key]['displayed'])
    path=ROOT/'Writeable/t08_interpretation_sections.md'
    path.write_text(text,encoding='utf-8')
    (OUT/'numeric_traceability.json').write_text(json.dumps({k:ledger[k] for k in sorted(used)},indent=2)+'\n')
    claims=json.loads((OUT/'claim_source_ledger.json').read_text())
    for row in claims:
        if row['status']!='removed' and row['anchor'] not in text:
            raise ValueError('Unlocated active claim '+row['claim_id'])
    for name in ['Writeable/t08_sections_template.md','scripts/prepare_t08_sections.py',
                 'scripts/prepare_t07_sections.py','provenance/t08/claim_source_ledger.json',
                 'provenance/t08/reference_audit.json','references/reconstruction.bib']:
        inputs[name]=digest(ROOT/name)
    result=dict(prepared_date='2026-11-12',recorded_utc=datetime.now(timezone.utc).isoformat(),
                inputs_sha256=inputs,numeric_entries=len(used),claims=len(claims),
                text_sha256=digest(path),model_refits=False,network_required=False,
                scope='Replacement Introduction Discussion Conclusion; whole-paper integration/figures/author declarations remain pending')
    if args.docx:
        word=ROOT/'Writeable/t08_interpretation_sections.docx'
        export_docx(text.replace('\n### ','\n## '),word)
        result['docx_sha256']=digest(word)
    (OUT/'run_metadata.json').write_text(json.dumps(result,indent=2)+'\n')
    print(f'Prepared {len(used)} numeric entries and {len(claims)} claim dispositions; '+
          f'{len(text.split("<!-- PAGE -->"))} planned pages.')


if __name__=='__main__':
    main()
