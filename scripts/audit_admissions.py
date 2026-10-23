"""Build and audit the C71 admission cohort from preserved official annual extracts.

Never deletes repeated/identical projected records. No modelling or rates.
"""
import csv, hashlib, json
from pathlib import Path
import pandas as pd
import pyreadstat
ROOT=Path(__file__).resolve().parents[1]
PROV=ROOT/'provenance/t02'
OUT=ROOT/'data/processed'

def anatomy(code):
    if code in [f'C71{i}' for i in range(5)]:return 'Supratentorial'
    if code in ['C715','C716','C717']:return 'Infratentorial/midline'
    if code=='C718':return 'Overlapping'
    if code=='C719':return 'Unspecified'
    return pd.NA

def age_group(value,unit):
    if pd.isna(value) or pd.isna(unit):return pd.NA
    if unit in [1,2,3]:
        upper={1:23,2:28,3:11}[unit]
        return '0-17' if value==int(value) and 1<=value<=upper else pd.NA
    if unit!=4 or value!=int(value) or not 1<=value<=115:return pd.NA
    return '0-17' if value<=17 else '18-44' if value<=44 else '45-64' if value<=64 else '65-79' if value<=79 else '80+'

def los_group(value):
    if pd.isna(value) or value<0 or value!=int(value):return pd.NA
    return '0 days' if value==0 else '1-3' if value<=3 else '4-14' if value<=14 else '15-30' if value<=30 else '31+'

def labels(series,mapping):
    # JSON keys retain original string codes or numeric codes encoded as strings.
    def lookup(v):
        if pd.isna(v):return pd.NA
        for key in [str(v),str(float(v)) if str(v).replace('.','',1).isdigit() else str(v),str(int(float(v))).zfill(2) if str(v).replace('.','',1).isdigit() else str(v)]:
            if key in mapping:return mapping[key]
        return pd.NA
    return series.map(lookup)

def main():
    from freeze_inputs import verify
    verify()
    manifest=pd.read_csv(ROOT/'provenance/inec_download_manifest.csv')
    for r in manifest.itertuples():
        with (ROOT/r.path).open('rb') as stream:
            assert hashlib.file_digest(stream,'sha256').hexdigest()==r.sha256, r.path
    cohort=[];schemas=[];quality=[]
    for y in range(2015,2025):
        extract=OUT/f'inec_c71/{y}.csv'
        flow=json.loads((PROV/f'{y}_flow.json').read_text())
        with extract.open('rb') as stream:
            assert hashlib.file_digest(stream,'sha256').hexdigest()==flow['extract_sha256'], extract
        x=pd.read_csv(extract,dtype={'prov_ubi':'string','prov_res':'string'})
        schema=json.loads((PROV/f'{y}_schema.json').read_text());m=schema['value_labels']
        x['admission_id']=x.source_year.astype(str)+':'+x.source_row.astype(str)
        x['death']=x.con_egrpa.map({1:0,2:1,3:1}).astype('Int64')
        x['anatomy']=x.icd10.map(anatomy)
        x['age_group']=[age_group(a,u) for a,u in zip(x.edad,x.cod_edad)]
        x['los_group']=x.dia_estad.map(los_group)
        x['age_years_completed']=x.edad.where(x.cod_edad.eq(4)).where(x.age_group.notna())
        x.loc[x.cod_edad.isin([1,2,3]) & x.age_group.notna(),'age_years_completed']=0
        for raw,new in [('prov_ubi','facility_province'),('prov_res','residence_province'),('sexo','sex'),('etnia','ethnicity_recorded'),('area_res','residence_area'),('area_ubi','facility_area')]:
            x[new]=labels(x[raw],m.get(raw,{}))
        x['sector_group']=x.sector.map({1:'Public',2:'Private for profit',3:'Private nonprofit'})
        x['sector_binary']=x.sector.map({1:'Public',2:'Private',3:'Private'})
        x['ethnicity_unknown']=x.etnia.eq(9) | x.ethnicity_recorded.isna()
        x['residence_foreign']=x.prov_res.str.zfill(2).eq('88')
        x['residence_province_unknown']=~x.prov_res.str.zfill(2).isin([str(i).zfill(2) for i in range(1,25)]+['88'])
        # Early SAV files omit labels. Keep their codes; mark the inferred labels provisional.
        if not m.get('area_res'):
            x['residence_area']=x.area_res.map({1:'Urbana',2:'Rural'})
        x['residence_area_mapping_verified']=y>=2018
        assert 'Vivo' in m['con_egrpa']['1.0']
        assert all('Fallecido' in m['con_egrpa'][k] for k in ['2.0','3.0'])
        for prefix in ['ingr','egr']:
            x[f'date_{prefix}']=pd.to_datetime(pd.DataFrame({'year':x[f'anio_{prefix}'],'month':x[f'mes_{prefix}'],'day':x[f'dia_{prefix}']}),errors='coerce')
        x['calendar_stay_days']=(x.date_egr-x.date_ingr).dt.days
        x['stay_date_difference']=x.dia_estad-x.calendar_stay_days
        x['discharge_year_mismatch']=x.anio_egr.ne(y)
        for c in x:
            quality.append({'year':y,'variable':c,'missing_or_blank':int((x[c].isna() | x[c].astype('string').str.strip().eq('')).sum()),'records':len(x)})
        schemas.append({'year':y,'age_unknown':int(x.age_group.isna().sum()),'outcome_unknown':int(x.death.isna().sum()),'los_unknown':int(x.los_group.isna().sum()),'ethnicity_unknown':int(x.ethnicity_unknown.sum()),'residence_province_unknown':int(x.residence_province_unknown.sum()),'residence_foreign':int(x.residence_foreign.sum()),'same_day_calendar':int(x.calendar_stay_days.eq(0).sum()),'negative_calendar_stay':int(x.calendar_stay_days.lt(0).sum()),'stay_date_mismatch':int(x.stay_date_difference.ne(0).sum()),'discharge_year_mismatch':int(x.discharge_year_mismatch.sum())})
        cohort.append(x)
    c=pd.concat(cohort,ignore_index=True)
    assert c.admission_id.is_unique and c.anatomy.notna().all()
    assert c.icd10.str.fullmatch('C71[0-9]').all()
    # No automatic exclusions for covariate missingness or suspected duplicate admissions.
    c.to_csv(OUT/'admissions_c71_audited.csv',index=False)
    pd.DataFrame(quality).to_csv(PROV/'missingness_by_year.csv',index=False)
    pd.DataFrame(schemas).to_csv(PROV/'quality_by_year.csv',index=False)
    annual=c.groupby('source_year').agg(admissions=('admission_id','size'),deaths=('death','sum'),known_outcomes=('death','count')).reset_index()
    annual['alive']=annual.known_outcomes-annual.deaths
    annual['unknown_outcomes']=annual.admissions-annual.known_outcomes
    legacy,lmeta=pyreadstat.read_sav(str(ROOT/'Data_base/BASE DATOS TESIS.sav'))
    legacy['icd10']=legacy.cau_cie10.str.extract(r'^(C71[0-9])')
    legacy['expected_anatomy']=legacy.icd10.map(anatomy)
    legacy_map={'Supratentorial (Hemisférico)':'Supratentorial','Infratentorial y Línea Media':'Infratentorial/midline','Lesiones Sobrepuestas':'Overlapping','No Especificado / Otros':'Unspecified'}
    legacy['recorded_anatomy']=legacy.CIE10.map(legacy_map)
    legacy.groupby(['icd10','recorded_anatomy','expected_anatomy']).size().rename('records').reset_index().to_csv(PROV/'legacy_anatomy_audit.csv',index=False)
    lg=legacy.groupby('Año').agg(legacy_admissions=('con_egrpa','size'),legacy_deaths=('con_egrpa',lambda s:s.eq('Fallecido').sum())).reset_index().rename(columns={'Año':'source_year'})
    annual=annual.merge(lg,on='source_year');annual['admissions_difference']=annual.admissions-annual.legacy_admissions;annual['deaths_difference']=annual.deaths-annual.legacy_deaths
    annual.to_csv(PROV/'annual_reconciliation.csv',index=False)
    c.groupby(['source_year','icd10','anatomy','death'],dropna=False).size().rename('records').reset_index().to_csv(PROV/'year_code_outcome.csv',index=False)
    for v in ['age_group','los_group','sex','ethnicity_recorded','sector_group','residence_area','facility_province','residence_province','con_egrpa','cod_edad']:
        c.groupby(['source_year',v],dropna=False).size().rename('records').reset_index().to_csv(PROV/f'counts_{v}.csv',index=False)
    # Identical observed attributes do not establish record duplication without an admission ID.
    rawfields=['source_year','prov_ubi','area_ubi','sector','sexo','cod_edad','edad','etnia','prov_res','area_res','anio_ingr','mes_ingr','dia_ingr','anio_egr','mes_egr','dia_egr','dia_estad','con_egrpa','cau_cie10']
    c['identical_projected_row']=c.duplicated(rawfields,keep=False)
    duplicates=c.groupby('source_year').agg(rows_in_identical_groups=('identical_projected_row','sum')).reset_index()
    duplicates.to_csv(PROV/'duplicate_projection_audit.csv',index=False)
    book=[]
    for path in sorted((ROOT/'Data_base').glob('*.xlsx')):
        x=pd.read_excel(path,sheet_name='Hoja3')
        shared=list(x)
        norm=lambda s:s.astype('string').str.replace(r'\.0$','',regex=True)
        equal=len(x)==len(legacy) and all(norm(x[k]).equals(norm(legacy[k])) for k in shared)
        book.append({'path':path.relative_to(ROOT).as_posix(),'sheet':'Hoja3','rows':len(x),'shared_fields':len(shared),'same_order_and_values_as_sav_after_numeric_format_normalization':equal})
    (PROV/'workbook_reconciliation.json').write_text(json.dumps(book,indent=2)+'\n')
    summary={'admissions':len(c),'deaths':int(c.death.sum()),'alive':int(c.death.eq(0).sum()),'unknown_outcome':int(c.death.isna().sum()),'legacy_misclassified_anatomy':int(legacy.recorded_anatomy.ne(legacy.expected_anatomy).sum()),'legacy_projected_duplicates_beyond_first':int(legacy[list(lmeta.column_names)].duplicated().sum()),'retention_policy':'All C710-C719 records retained; no covariate or deduplication exclusions; unknown covariates explicitly flagged','year_policy':'All 2015-2024 years retained from official source reconstruction; no anomaly-year exclusion'}
    (PROV/'audit_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(annual.to_string(index=False));print(summary)

if __name__=='__main__':main()
