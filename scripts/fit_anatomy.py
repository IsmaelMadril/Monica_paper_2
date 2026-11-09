"""T05: separate recorded code detail from conditional anatomical group associations."""
import hashlib
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import warnings
import zipfile

import numpy as np
import pandas as pd
from scipy.stats import norm
import statsmodels.api as sm

from audit_admissions import anatomy as expected_anatomy
from calculate_rates import wilson
from fit_mortality import separation_check, ETHNICITY
from inspect_legacy_mortality import readable_strings
from profile_sparse_mortality import profile_interval

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'provenance/t05'
TABLES = ROOT/'outputs/tables'
CORE = ['age_group', 'sex', 'sector_binary', 'year']
LEVELS = {
    'age_group': ['18-44', '0-17', '45-64', '65-79', '80+'],
    'sex': ['Hombre', 'Mujer'],
    'sector_binary': ['Private', 'Public'],
    'year': [str(y) for y in range(2015, 2025)],
    'ethnicity': ['6','1','2','3','4','5','7','8','9'],
    'residence_area': ['Urbana','Rural'],
}
GROUPS = ['Supratentorial','Infratentorial/midline','Overlapping','Unspecified']


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def build_design(data, variables):
    x = pd.DataFrame({'Intercept': np.ones(len(data))}, index=data.index)
    terms, references = [], {}
    for variable in variables:
        if data[variable].isna().any():raise ValueError('Missing required predictor: '+variable)
        observed = set(data[variable].astype(str))
        if observed-set(LEVELS[variable]):raise ValueError('Unrecognized predictor category: '+variable)
        levels = [level for level in LEVELS[variable] if level in observed]
        if len(levels)<2:raise ValueError('Predictor has fewer than two levels: '+variable)
        references[variable] = levels[0]
        for level in levels[1:]:
            term = f'{variable}[{level}]'
            x[term] = data[variable].astype(str).eq(level).astype(float)
            terms.append(dict(term=term,variable=variable,level=level,reference=levels[0]))
    return x,terms,references


def panel_data(data, panel):
    if panel=='coding':
        result=data.copy()
        result['event']=result.icd10.ne('C719').astype(int)
    elif panel=='site':
        result=data.loc[data.anatomy.isin(['Supratentorial','Infratentorial/midline'])].copy()
        result['event']=result.anatomy.eq('Infratentorial/midline').astype(int)
    else:raise ValueError('Unknown panel')
    return result


def fit_binary(data, panel, model, variables, covariance='nonrobust'):
    x,terms,references=build_design(data,variables)
    y=data.event.to_numpy(dtype=float)
    if not np.isfinite(y).all() or not np.isin(y,[0,1]).all() or len(np.unique(y))!=2:
        raise ValueError('Binary event must contain both recognized values0 and1')
    rank=int(np.linalg.matrix_rank(x))
    if rank!=x.shape[1]:raise RuntimeError(f'{panel}/{model}: design rank deficiency')
    separation=separation_check(x,y)
    if separation['separation_detected']:raise RuntimeError(f'{panel}/{model}: separation; do not report conventional estimates')
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter('always')
        fitted=sm.GLM(y,x,family=sm.families.Binomial()).fit(maxiter=100,tol=1e-10,cov_type=covariance)
    probabilities=fitted.predict()
    information=x.to_numpy().T@((probabilities*(1-probabilities))[:,None]*x.to_numpy())
    eigen=np.linalg.eigvalsh(information)
    score=float(np.abs(x.to_numpy().T@(y-probabilities)).max())
    messages=[str(w.message) for w in captured]
    if not fitted.converged or messages or not np.isfinite(fitted.params).all() or eigen.min()<=0 or score>1e-5:
        raise RuntimeError(f'{panel}/{model}: convergence/information/warning checks failed: {messages}')
    rows=[]
    for term in terms:
        name=term['term'];beta=float(fitted.params[name]);se=float(fitted.bse[name])
        values=data.loc[data[term['variable']].astype(str).eq(term['level']),'event']
        rows.append(dict(panel=panel,model=model,**term,beta=beta,se=se,aor=math.exp(beta),
                         lower_95=math.exp(beta-1.959963984540054*se),upper_95=math.exp(beta+1.959963984540054*se),
                         p_value=float(2*norm.sf(abs(beta/se))),admissions=len(values),events=int(values.sum()),
                         non_events=int(len(values)-values.sum()),sparse_level=min(int(values.sum()),int(len(values)-values.sum()))<10,
                         interval_method='Wald',covariance=covariance))
    diagnostic=dict(panel=panel,model=model,admissions=len(data),events=int(y.sum()),non_events=int(len(y)-y.sum()),
                    parameters=x.shape[1],rank=rank,converged=bool(fitted.converged),iterations=int(fitted.fit_history['iteration']),
                    score_max_abs=score,smallest_information_eigenvalue=float(eigen.min()),
                    information_condition_number=float(eigen.max()/eigen.min()),warnings=messages,references=references,
                    min_fitted_event_probability=float(probabilities.min()),max_fitted_event_probability=float(probabilities.max()),
                    log_likelihood=float(fitted.llf),**separation)
    return rows,diagnostic,fitted,x,terms


def separation_certificates(data):
    """A zero outcome in a nonreference dummy level gives a multinomial recession direction.

    With the unspecified outcome as baseline, decrease only that level's coefficient
    in the overlapping logit. Every affected observation has another outcome, so
    its probability strictly increases. No finite MLE exists in that direction.
    """
    rows=[]
    for level in LEVELS['ethnicity'][1:]:
        subset=data.loc[data.ethnicity.eq(level)]
        overlap=int(subset.anatomy.eq('Overlapping').sum())
        if len(subset)>0 and overlap==0:
            rows.append(dict(predictor='ethnicity',level=level,outcome='Overlapping',outcome_count=0,
                             other_outcomes=len(subset),reference_predictor='6',reference_outcome='Unspecified',
                             direction='decrease overlapping-outcome ethnicity coefficient toward minus infinity',
                             conclusion='no finite unpenalized maximum in full four-outcome ethnicity model'))
    return rows


def legacy_warning():
    path=ROOT/'Results/RESULTADOS.spv'
    target=OUT/'legacy_nomreg_evidence.json'
    if not path.exists():
        print('Legacy SPV absent locally; historical NOMREG evidence preserved; rebuilt models do not require it.',flush=True)
        return
    member='00000000072_lightWarningData.bin'
    with zipfile.ZipFile(path) as archive:
        data=archive.read(member)
    strings=readable_strings(data)
    selected=list(dict.fromkeys(s.removesuffix('X') for s in strings if any(k in s for k in ['singularidades','validez','continúa','hessiana'])))
    if not selected:raise ValueError('Expected NOMREG warning not found; inspect supplied SPV')
    target.write_text(json.dumps(dict(source_path=path.relative_to(ROOT).as_posix(),source_sha256=digest(path),
        member=member,member_sha256=hashlib.sha256(data).hexdigest(),warning_text=selected,
        interpretation='Saved NOMREG reports Hessian singularities and uncertain validity; not a valid conventional Table5 fit'),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def main():
    OUT.mkdir(parents=True,exist_ok=True);TABLES.mkdir(parents=True,exist_ok=True)
    path=ROOT/'data/processed/admissions_c71_audited.csv'
    data=pd.read_csv(path)
    if not data.admission_id.is_unique or not data.icd10.str.fullmatch(r'C71[0-9]').all():raise ValueError('Invalid source cohort identifiers/codes')
    if not data.anatomy.eq(data.icd10.map(expected_anatomy)).all():raise ValueError('Anatomical labels do not match corrected ICD mapping')
    if not data.etnia.isin(range(1,10)).all() or not data.source_year.isin(range(2015,2025)).all():raise ValueError('Invalid ethnicity/year source codes')
    data['ethnicity']=data.etnia.astype(int).astype(str)
    data['year']=data.source_year.astype(int).astype(str)
    legacy_warning()
    certificate=separation_certificates(data)
    pd.DataFrame(certificate).to_csv(OUT/'four_outcome_separation_certificates.csv',index=False)
    cells=[]
    for variable in CORE+['ethnicity','residence_area']:
        levels=LEVELS[variable]
        for level in levels:
            subset=data.loc[data[variable].astype(str).eq(level)]
            for group in GROUPS:
                cells.append(dict(variable=variable,level=level,anatomy=group,admissions=int(subset.anatomy.eq(group).sum()),
                                  scope='all years; early residence labels provisional' if variable=='residence_area' else 'all years'))
    pd.DataFrame(cells).to_csv(OUT/'anatomy_predictor_cells.csv',index=False)
    descriptions=[]
    for group in GROUPS:
        count=int(data.anatomy.eq(group).sum());percent,lo,hi=wilson(count,len(data))
        descriptions.append(dict(anatomy=group,admissions=count,total_admissions=len(data),percent=percent,lower_95=lo,upper_95=hi))
    pd.DataFrame(descriptions).to_csv(OUT/'anatomy_descriptive.csv',index=False)
    all_rows,diagnostics,flow,profiles,crude,reference_checks=[],[],[],[],[],[]
    for panel in ['coding','site']:
        frame=panel_data(data,panel)
        flow.append(dict(panel=panel,source_admissions=len(data),excluded_c719=0 if panel=='coding' else int(data.icd10.eq('C719').sum()),
                         excluded_c718=0 if panel=='coding' else int(data.icd10.eq('C718').sum()),included_admissions=len(frame),events=int(frame.event.sum()),non_events=int(len(frame)-frame.event.sum())))
        verified=frame.loc[frame.residence_area_mapping_verified].copy()
        specifications=[('primary',frame,CORE,'nonrobust'),
                        ('resident_only',frame.loc[~frame.residence_foreign],CORE,'nonrobust'),
                        ('exclude_2017_2023',frame.loc[~frame.source_year.isin([2017,2023])],CORE,'nonrobust'),
                        ('verified_years_core',verified,CORE,'nonrobust'),
                        ('verified_years_residence',verified,CORE+['residence_area'],'nonrobust'),
                        ('record_HC0',frame,CORE,'HC0'),
                        ('ethnicity_extended',frame,CORE+['ethnicity'],'nonrobust')]
        if panel=='site':specifications.append(('exclude_ventricular',frame.loc[frame.icd10.ne('C715')],CORE,'nonrobust'))
        for name,subset,variables,covariance in specifications:
            rows,diagnostic,fitted,x,terms=fit_binary(subset.copy(),panel,name,variables,covariance)
            all_rows.extend(rows);diagnostics.append(diagnostic)
            print(panel,name,'n=',len(subset),'events=',int(subset.event.sum()),'converged=',fitted.converged,flush=True)
            if name=='primary':
                covariance_matrix=fitted.cov_params()
                covariance_matrix.to_csv(OUT/f'{panel}_primary_covariance.csv',index_label='term')
                child,old='age_group[0-17]','age_group[80+]'
                beta=float(fitted.params[child]-fitted.params[old])
                se=math.sqrt(float(covariance_matrix.loc[child,child]+covariance_matrix.loc[old,old]-2*covariance_matrix.loc[child,old]))
                reference_checks.append(dict(panel=panel,contrast='age0-17 versus80+',aor=math.exp(beta),
                    lower_95=math.exp(beta-1.959963984540054*se),upper_95=math.exp(beta+1.959963984540054*se),
                    interpretation='Reference re-expression only; outcome differs from the old unspecified-reference multinomial contrast'))
                for term in terms:
                    k=[]
                    for level in [term['level'],term['reference']]:
                        group=subset.loc[subset[term['variable']].astype(str).eq(level),'event']
                        k.append((int(group.sum()),int(len(group)-group.sum())))
                    (a,b),(c,d)=k
                    beta=math.log(a/b)-math.log(c/d);se=math.sqrt(1/a+1/b+1/c+1/d)
                    crude.append(dict(panel=panel,**term,events=a,non_events=b,reference_events=c,reference_non_events=d,
                                      crude_or=math.exp(beta),lower_95=math.exp(beta-1.959963984540054*se),upper_95=math.exp(beta+1.959963984540054*se)))
            if name=='ethnicity_extended':
                for row in rows:
                    if row['sparse_level']:
                        lo,hi=profile_interval(x,subset.event.to_numpy(),fitted,row['term'])
                        profiles.append(dict(panel=panel,model=name,term=row['term'],events=row['events'],non_events=row['non_events'],
                                             aor=row['aor'],wald_lower_95=row['lower_95'],wald_upper_95=row['upper_95'],profile_lower_95=lo,profile_upper_95=hi))
    coefficients=pd.DataFrame(all_rows)
    coefficients.to_csv(OUT/'all_model_coefficients.csv',index=False)
    pd.DataFrame(flow).to_csv(OUT/'model_flow.csv',index=False)
    pd.DataFrame(reference_checks).to_csv(OUT/'reference_contrasts.csv',index=False)
    pd.DataFrame(crude).to_csv(OUT/'crude_odds_ratios.csv',index=False)
    pd.DataFrame(profiles).to_csv(OUT/'sparse_profile_intervals.csv',index=False)
    (OUT/'model_diagnostics.json').write_text(json.dumps(diagnostics,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    pd.DataFrame(diagnostics).drop(columns=['references','warnings']).to_csv(OUT/'model_sample_sizes_and_fit.csv',index=False)
    primary=coefficients.loc[coefficients.model.eq('primary')]
    compare=coefficients.loc[coefficients.model.ne('primary')].merge(primary[['panel','term','reference','aor','beta']].rename(columns={'aor':'primary_aor','beta':'primary_beta'}),on=['panel','term','reference'],how='left',validate='many_to_one')
    compare['log_or_change']=compare.beta-compare.primary_beta
    compare['or_ratio_to_primary']=compare.aor/compare.primary_aor
    compare.to_csv(OUT/'sensitivity_comparison.csv',index=False)
    primary.to_csv(TABLES/'table5_rebuilt.csv',index=False)
    from table_reporting import render_models
    render_models(ROOT, table=5)
    metadata=dict(recorded_utc=datetime.now(timezone.utc).isoformat(),specification_date='2026-11-09',inputs_sha256={path.relative_to(ROOT).as_posix():digest(path),'provenance/t05/analysis_specification.md':digest(OUT/'analysis_specification.md')},
                  statsmodels=sm.__version__,primary_events={'coding':'non-C719=1;C719=0','site':'C715-C717=1;C710-C714=0;C718/C719 excluded'},
                  primary_references={d['panel']:d['references'] for d in diagnostics if d['model']=='primary'},
                  primary_covariance='Observed-information; independent admission records',four_outcome_decision='Not estimated: conceptual mixture plus demonstrated no-finite-MLE directions when source ethnicity included',
                  limitations=['Conditional coding/selection','Unknown patient/facility dependence','Missing severity/treatment','Exploratory comparisons'])
    (OUT/'run_metadata.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(primary.loc[primary.variable.isin(['age_group','sector_binary']),['panel','term','aor','lower_95','upper_95']].to_string(index=False))

if __name__=='__main__':main()
