"""T06: denominator-explicit Tables 1–2 and consistent Tables 4–5 presentation."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import platform

import numpy as np
import pandas as pd
import scipy
from scipy.stats import beta, chi2_contingency, fisher_exact, random_table

from table_reporting import render_models, p_text, label

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'provenance/t06'
TABLES = ROOT/'outputs/tables'
GROUPS = ['Supratentorial', 'Infratentorial/midline', 'Overlapping', 'Unspecified']
VARIABLES = {
    'age_group': ['0-17','18-44','45-64','65-79','80+'],
    'sex': ['Hombre','Mujer'],
    'ethnicity': [str(i) for i in range(1,10)],
    'sector_binary': ['Public','Private'],
    'sector_group': ['Public','Private nonprofit','Private for profit'],
    'los_group': ['0','1-3','4-14','15-30','31+'],
    'year': [str(y) for y in range(2015,2025)],
    'residence_area': ['Urbana','Rural'],
}
REPLICATES = 99_999
SEED = 20261109


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def independence_test(observed, seed, replicates=REPLICATES):
    counts = np.asarray(observed)
    if counts.ndim != 2 or not np.isfinite(counts).all() or (counts < 0).any() or (counts != np.floor(counts)).any():
        raise ValueError('Contingency counts must be finite nonnegative integers in two dimensions')
    counts = counts.astype(np.int64)
    active = counts[counts.sum(axis=1)>0][:, counts.sum(axis=0)>0]
    result = dict(active_rows=active.shape[0], active_columns=active.shape[1],
                  admissions=int(active.sum()), seed=None, replicates=0, exceedances=None,
                  monte_carlo_se=None, tail_lower_95=None, tail_upper_95=None)
    if min(active.shape) < 2:
        return dict(result, method='Not testable: fewer than two active levels', statistic=None,
                    p_value=None, degrees_of_freedom=None, minimum_expected=None, cells_expected_below_5=None)
    pearson = chi2_contingency(active, correction=False)
    expected = pearson.expected_freq
    result.update(statistic=float(pearson.statistic), degrees_of_freedom=int(pearson.dof),
                  minimum_expected=float(expected.min()), cells_expected_below_5=int((expected<5).sum()))
    if active.min() >= 5 and expected.min() >= 5:
        return dict(result, method='Pearson chi-square (no continuity correction)', p_value=float(pearson.pvalue))
    if active.shape == (2,2):
        return dict(result, method='Fisher exact (two-sided)', p_value=float(fisher_exact(active,alternative='two-sided').pvalue))
    if replicates < 1:
        raise ValueError('Monte Carlo replicate count must be positive')
    rng = np.random.default_rng(seed)
    exceedances = 0
    for offset in range(0, replicates, 5000):
        simulated = random_table.rvs(active.sum(axis=1), active.sum(axis=0),
                                     size=min(5000,replicates-offset), method='patefield', random_state=rng)
        statistic = (((simulated-expected)**2)/expected).sum(axis=(1,2))
        exceedances += int((statistic >= pearson.statistic-1e-10*max(1,pearson.statistic)).sum())
    probability = (exceedances+1)/(replicates+1)
    result.update(method='Fixed-margin Monte Carlo Pearson', seed=seed, replicates=replicates,
                  exceedances=exceedances, p_value=probability,
                  monte_carlo_se=float(np.sqrt(probability*(1-probability)/replicates)),
                  tail_lower_95=0.0 if exceedances==0 else float(beta.ppf(.025,exceedances,replicates-exceedances+1)),
                  tail_upper_95=1.0 if exceedances==replicates else float(beta.ppf(.975,exceedances+1,replicates-exceedances)))
    return result


def summarize(frame, variable, levels, outcomes):
    """Long-form numeric cells; preserve unknowns and missing as distinct categories."""
    values = frame[variable].astype('string').fillna('Missing')
    unexpected = set(values)-set(levels)-{'Missing'}
    if unexpected:
        raise ValueError(f'Unrecognized {variable} levels: {unexpected}')
    ordered = list(levels)+(['Missing'] if values.eq('Missing').any() else [])
    rows, matrix = [], []
    for level in ordered:
        group = frame.loc[values.eq(level)]
        counts = [int(group[outcomes[0]].eq(outcome).sum()) for outcome in outcomes[1]]
        matrix.append(counts)
        for outcome, count in zip(outcomes[1], counts):
            denominator = int(frame[outcomes[0]].eq(outcome).sum())
            rows.append(dict(variable=variable, level=level, outcome=str(outcome), count=count,
                             column_denominator=denominator,
                             column_percent=100*count/denominator if denominator else np.nan,
                             group_admissions=len(group), scope_admissions=len(frame)))
    return rows, np.asarray(matrix)


def validate_saved_models(cohort_sha):
    inputs = {}
    for stage, expected in [('t04',8),('t05',15)]:
        folder = ROOT/'provenance'/stage
        metadata = json.loads((folder/'run_metadata.json').read_text(encoding='utf-8'))
        hashes = metadata['inputs_sha256']
        if hashes['data/processed/admissions_c71_audited.csv'] != cohort_sha:
            raise ValueError(f'{stage} used different cohort bytes; rerun that stage before T06')
        diagnostics = json.loads((folder/'model_diagnostics.json').read_text(encoding='utf-8'))
        if len(diagnostics)!=expected or any(not d['converged'] or d['separation_detected'] or d['warnings'] or d['rank']!=d['parameters'] for d in diagnostics):
            raise ValueError(f'{stage} saved diagnostics invalid')
        for name in ['run_metadata.json','model_diagnostics.json','all_model_coefficients.csv']:
            inputs[(folder/name).relative_to(ROOT).as_posix()] = digest(folder/name)
    return inputs


def main():
    source = ROOT/'data/processed/admissions_c71_audited.csv'
    data = pd.read_csv(source)
    if not data.admission_id.is_unique or data.death.isna().any() or not data.death.isin([0,1]).all():
        raise ValueError('Invalid identifiers or death outcomes')
    if data.anatomy.isna().any() or not data.anatomy.isin(GROUPS).all():
        raise ValueError('Invalid anatomy outcomes')
    verified = data.residence_area_mapping_verified
    if not verified.isin([True,False]).all() or not verified.eq(data.source_year.between(2018,2024)).all():
        raise ValueError('Residence mapping verification scope changed; review specification')
    data['ethnicity'] = data.etnia.astype('Int64').astype('string')
    data['year'] = data.source_year.astype('Int64').astype('string')
    model_inputs = validate_saved_models(digest(source))
    OUT.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    tests, scope_rows, missingness, reconciliations = [], [], [], []
    for number in [1,2]:
        variables = dict(VARIABLES)
        if number==1:
            variables['anatomy'] = GROUPS
        lines = [f'# Rebuilt Table {number} — '+('characteristics by discharge outcome' if number==1 else 'characteristics by recorded anatomical group'), '',
                 'Admission/discharge records with primary diagnosis C71, Ecuador, 2015–2024. '
                 f'All-year cohort N={len(data):,}; in-hospital deaths={int(data.death.sum()):,}; live discharges={int(data.death.eq(0).sum()):,}.', '',
                 'Counts in parentheses are column percentages within each characteristic block. '
                 + ('Fatality is a row percentage: deaths divided by admissions in that category.' if number==1 else
                    'Group definitions: supratentorial C710–C714; infratentorial/midline C715–C717; overlapping C718; unspecified C719. C715 is an operational midline assignment.'), '']
        numeric = []
        for index, (variable, levels) in enumerate(variables.items()):
            frame = data.loc[verified].copy() if variable=='residence_area' else data
            scope = '2018–2024 verified residence labels' if variable=='residence_area' else '2015–2024'
            scope_rows.append(dict(table=number,variable=variable,scope=scope,included=len(frame),
                                   excluded=len(data)-len(frame),deaths=int(frame.death.sum()),live=int(frame.death.eq(0).sum())))
            values = frame[variable]
            missingness.append(dict(table=number,variable=variable,scope=scope,null_count=int(values.isna().sum()),
                                    source_unknown_count=int(values.eq('9').sum()) if variable=='ethnicity' else 0))
            outcome_variable, outcome_levels = ('death',[0,1]) if number==1 else ('anatomy',GROUPS)
            cells, matrix = summarize(frame,variable,levels,(outcome_variable,outcome_levels))
            test = independence_test(matrix,SEED+number*100+index)
            tests.append(dict(table=number,variable=variable,scope=scope,**test))
            p = p_text(test['p_value'])
            if test['method'].startswith('Fixed-margin') and test['exceedances']==0:
                p = f'{1/(REPLICATES+1):.0e} (minimum attainable; 0/{REPLICATES:,} exceedances)'
            lines += [f'## {label(variable)}', '', f'Scope: {scope}; N={len(frame):,}; excluded from this block={len(data)-len(frame):,}. '
                      f'Null values={int(frame[variable].isna().sum())}. Omnibus p={p}; {test["method"]}.', '']
            if variable=='residence_area':
                excluded = data.loc[~verified]
                lines += [f'Excluded early-year records: {len(excluded):,}, comprising {int(excluded.death.sum()):,} deaths and {int(excluded.death.eq(0).sum()):,} live discharges. The restriction applies only to this block.', '']
            denominators = [int(frame[outcome_variable].eq(o).sum()) for o in outcome_levels]
            if number==1:
                lines += [f'| Category | All (N={len(frame):,}) | Live (N={denominators[0]:,}) | Dead (N={denominators[1]:,}) | Within-group fatality |',
                          '|---|---:|---:|---:|---:|']
            else:
                lines += ['| Category | All (N='+f'{len(frame):,}'+') | '+' | '.join(f'{o} (N={n:,})' for o,n in zip(outcome_levels,denominators))+' |',
                          '|---|---:|'+'---:|'*4]
            for level in dict.fromkeys(r['level'] for r in cells):
                row = [r for r in cells if r['level']==level]
                n = row[0]['group_admissions']
                total_pct = 100*n/len(frame)
                display = [f'{r["count"]:,} ({r["column_percent"]:.2f}%)' if r['column_denominator'] else f'{r["count"]:,} (n.a.)' for r in row]
                fatality = 100*row[1]['count']/n if number==1 and n else np.nan
                lines.append(f'| {label(level,variable)} | {n:,} ({total_pct:.2f}%) | '+' | '.join(display)+
                             (f' | {fatality:.2f}%' if number==1 and n else ' | n.a.' if number==1 else '')+' |')
                for r in row:
                    numeric.append(dict(table=number,scope=scope,**r,group_percent=total_pct,
                                        fatality_percent=fatality if number==1 else np.nan))
            if matrix.sum()!=len(frame) or not np.array_equal(matrix.sum(axis=0),denominators):
                raise ValueError('Table totals do not reconcile')
            reconciliations.append(dict(table=number,variable=variable,scope=scope,
                                         counted=int(matrix.sum()),expected=len(frame),passed=True))
            lines += ['']
        lines += ['Each characteristic partitions its stated cohort; do not add counts across characteristic blocks. '
                  'Unknown ethnicity (source 9) is retained separately from Other; true nulls, if present, appear as Missing. '
                  'A zero stay category is shown explicitly even when empty; 15–30 and 31+ are mutually exclusive. '
                  'Residence comparisons exclude all 2015–2017 records because their area labels remain provisional; all other blocks retain them. '
                  'The missingness and scope files give exact exclusion/outcome denominators.', '',
                  'One exploratory omnibus comparison per characteristic: uncorrected Pearson chi-square only when every observed and expected cell is ≥5; '
                  'sparse 2×2 tables use two-sided Fisher exact; larger sparse tables use fixed-margin Monte Carlo Pearson tests '
                  f'with {REPLICATES:,} replicates and deterministic per-comparison seeds. Zero-margin rows/columns are not tested. '
                  'Monte Carlo p=(exceedances+1)/(replicates+1), including ties. Simulation errors and tail-probability intervals are in provenance/t06/independence_tests.csv. '
                  'Full numerical p-values are retained there. Display precision is three significant digits; no multiplicity adjustment or significance highlighting.', '',
                  'Tests assume independent admissions; repeated persons/facilities are unresolved. Small p-values do not measure clinical importance, '
                  'causal effects, population cancer risks or temporal trends. Stay is observed during admission and is descriptive here. '
                  'Column composition percentages are not within-category fatality or individual risk.', '',
                  '[Specification, verification and sources](../../Writeable/t06_descriptive_tables.md).', '']
        text = '\n'.join(lines)
        (TABLES/f'table{number}_rebuilt.md').write_text(text,encoding='utf-8')
        (OUT/f'table{number}_rebuilt.md').write_text(text,encoding='utf-8')
        pd.DataFrame(numeric).to_csv(OUT/f'table{number}_cells.csv',index=False)
        pd.DataFrame(numeric).to_csv(TABLES/f'table{number}_rebuilt.csv',index=False)
    pd.DataFrame(tests).to_csv(OUT/'independence_tests.csv',index=False)
    pd.DataFrame(scope_rows).to_csv(OUT/'table_scopes.csv',index=False)
    pd.DataFrame(missingness).to_csv(OUT/'missingness.csv',index=False)
    pd.DataFrame(reconciliations).to_csv(OUT/'reconciliation.csv',index=False)
    render_models(ROOT)
    for number in [4,5]:
        (OUT/f'table{number}_rebuilt.md').write_bytes((TABLES/f'table{number}_rebuilt.md').read_bytes())
    inputs = {'data/processed/admissions_c71_audited.csv':digest(source),**model_inputs}
    for name in ['scripts/generate_descriptive_tables.py','scripts/table_reporting.py','provenance/t06/analysis_specification.md']:
        inputs[name] = digest(ROOT/name)
    metadata = dict(recorded_utc=datetime.now(timezone.utc).isoformat(), specification_date='2026-11-09',
                    inputs_sha256=inputs,python=platform.python_version(),platform=platform.platform(),
                    scipy=scipy.__version__,numpy=np.__version__,pandas=pd.__version__,
                    replicates=REPLICATES,seed_base=SEED,admissions=len(data),deaths=int(data.death.sum()),
                    model_estimates_changed=False,comparisons=len(tests))
    (OUT/'run_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    print(pd.DataFrame(tests)[['table','variable','admissions','method','p_value','exceedances']].to_string(index=False))
    print('Tables 1, 2, 4 and 5 written; all characteristic totals reconcile.')


if __name__=='__main__':
    main()
