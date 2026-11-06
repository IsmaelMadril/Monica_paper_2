"""T04: reproducible admission-level mortality associations and prespecified sensitivities."""
import hashlib
import json
import math
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from scipy.optimize import linprog
from scipy.special import expit
from scipy.stats import norm
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'provenance/t04'
TABLES = ROOT/'outputs/tables'
CORE = ['age_group', 'sex', 'ethnicity', 'sector_binary', 'anatomy', 'year']
LEVELS = {
    'age_group': ['0-17', '18-44', '45-64', '65-79', '80+'],
    'sex': ['Hombre', 'Mujer'],
    'ethnicity': ['6', '1', '2', '3', '4', '5', '7', '8', '9'],
    'sector_binary': ['Private', 'Public'],
    'anatomy': ['Supratentorial', 'Infratentorial/midline', 'Overlapping', 'Unspecified'],
    'year': [str(y) for y in range(2015, 2025)],
    'residence_area': ['Urbana', 'Rural'],
    'los_group': ['1-3', '4-14', '15-30', '31+'],
}
ETHNICITY = {'1':'Indigenous', '2':'Afro-Ecuadorian/Afrodescendant (source 2)', '3':'Negro/a (source 3)', '4':'Mulato/a (source 4)', '5':'Montubio', '6':'Mestizo', '7':'White', '8':'Other', '9':'Unknown/not recorded'}


def design(data, variables):
    frame = pd.DataFrame({'Intercept': np.ones(len(data))}, index=data.index)
    terms = []
    refs = {}
    for variable in variables:
        if data[variable].isna().any():
            raise ValueError(f'Missing predictor: {variable}')
        observed = set(data[variable].astype(str))
        if observed-set(LEVELS[variable]):
            raise ValueError(f'Unrecognized {variable} levels: {observed-set(LEVELS[variable])}')
        levels = [level for level in LEVELS[variable] if level in observed]
        if len(levels) < 2:
            raise ValueError(f'{variable} has fewer than two levels')
        refs[variable] = levels[0]
        for level in levels[1:]:
            name = f'{variable}[{level}]'
            frame[name] = data[variable].astype(str).eq(level).astype(float)
            terms.append(dict(term=name, variable=variable, level=level, reference=levels[0]))
    return frame, terms, refs


def separation_check(x, y):
    """LP finds a separating direction, including quasi-separation; intercept is in X."""
    x, y = np.asarray(x, float), np.asarray(y, int)
    margins = (2*y-1)[:, None]*x
    # Under ||beta||_infinity <= 1, maximize sum(margins) subject to all margins >= 0.
    result = linprog(-margins.sum(axis=0), A_ub=-margins,
                     b_ub=np.zeros(len(y)), bounds=[(-1, 1)]*x.shape[1], method='highs')
    if not result.success:
        raise RuntimeError('Separation LP failed: '+result.message)
    objective = float(-result.fun)
    quasi_or_complete = objective > 1e-6
    return dict(separation_detected=quasi_or_complete, objective=objective,
                minimum_margin=float((margins@result.x).min()), lp_status=result.message)


def crude_contrasts(data, terms):
    rows = []
    for term in terms:
        counts = []
        for level in [term['level'], term['reference']]:
            values = data.loc[data[term['variable']].astype(str).eq(level), 'death']
            counts.append((int(values.sum()), int(len(values)-values.sum())))
        (a, b), (c, d) = counts
        row = dict(**term, deaths=a, alive=b, ref_deaths=c, ref_alive=d)
        if min(a, b, c, d) == 0:
            row.update(crude_or=np.nan, lower_95=np.nan, upper_95=np.nan, status='zero cell; conventional OR/interval not estimable')
        else:
            beta = math.log(a/b)-math.log(c/d)
            se = math.sqrt(1/a+1/b+1/c+1/d)
            row.update(crude_or=math.exp(beta), lower_95=math.exp(beta-1.959963984540054*se),
                       upper_95=math.exp(beta+1.959963984540054*se), status='estimable')
        rows.append(row)
    return rows


def fit_one(data, name, variables, covariance='nonrobust'):
    x, terms, references = design(data, variables)
    y = data.death.to_numpy(dtype=float)
    rank = int(np.linalg.matrix_rank(x))
    if rank != x.shape[1]:
        raise RuntimeError(f'{name}: rank deficient')
    separation = separation_check(x, y)
    if separation['separation_detected']:
        raise RuntimeError(f'{name}: separation detected; select a justified alternative before reporting')
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter('always')
        result = sm.GLM(y, x, family=sm.families.Binomial()).fit(maxiter=100, tol=1e-10,
                                                              cov_type=covariance)
    p = result.predict()
    info = x.to_numpy().T@((p*(1-p))[:, None]*x.to_numpy())
    eigen = np.linalg.eigvalsh(info)
    score = x.to_numpy().T@(y-p)
    score_max = float(np.abs(score).max())
    if not result.converged or not np.isfinite(result.params).all() or eigen.min() <= 0 or score_max > 1e-5:
        raise RuntimeError(f'{name}: fit diagnostics failed')
    rows = []
    for term in terms:
        label = term['term']
        beta, se = float(result.params[label]), float(result.bse[label])
        values = data.loc[data[term['variable']].astype(str).eq(term['level']), 'death']
        n, deaths = len(values), int(values.sum())
        rows.append(dict(model=name, **term, beta=beta, se=se, aor=math.exp(beta),
                         lower_95=math.exp(beta-1.959963984540054*se),
                         upper_95=math.exp(beta+1.959963984540054*se),
                         p_value=float(2*norm.sf(abs(beta/se))), admissions=n, deaths=deaths,
                         sparse_level=deaths<10 or n-deaths<10,
                         interval_method='Wald', covariance=covariance))
    leverage = result.get_hat_matrix_diag()
    diagnostic = dict(model=name, admissions=len(data), deaths=int(y.sum()), alive=int(len(data)-y.sum()),
                      parameters=x.shape[1], rank=rank, events_per_parameter=float(y.sum()/x.shape[1]),
                      converged=bool(result.converged), iterations=int(result.fit_history['iteration']),
                      score_max_abs=score_max, smallest_information_eigenvalue=float(eigen.min()),
                      information_condition_number=float(eigen.max()/eigen.min()),
                      log_likelihood=float(result.llf), deviance=float(result.deviance),
                      max_abs_coefficient=float(np.abs(result.params).max()), max_standard_error=float(result.bse.max()),
                      min_fitted_death_probability=float(p.min()), max_fitted_death_probability=float(p.max()),
                      max_leverage=float(leverage.max()), warnings=[str(w.message) for w in captured],
                      references=references, **separation)
    return rows, diagnostic, result, x, terms


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    path = ROOT/'data/processed/admissions_c71_audited.csv'
    data = pd.read_csv(path)
    expected = data.con_egrpa.map({1:0, 2:1, 3:1})
    if expected.isna().any() or not data.death.eq(expected).all():
        raise ValueError('Rebuilt outcome does not match explicit source discharge codes')
    if not data.admission_id.is_unique or data.age_group.isna().any():
        raise ValueError('Invalid audited cohort identifiers/age groups')
    if not data.etnia.isin(range(1, 10)).all() or not data.source_year.isin(range(2015, 2025)).all():
        raise ValueError('Unknown or noninteger ethnicity/year source code')
    data['ethnicity'] = data.etnia.astype(int).astype(str)
    data['year'] = data.source_year.astype(int).astype(str)
    source_map = data.groupby(['con_egrpa', 'death'], dropna=False).size().rename('admissions').reset_index()
    source_map.to_csv(OUT/'outcome_encoding.csv', index=False)
    required = CORE+['death']
    flow = [{'stage':'audited discharges', 'admissions':len(data), 'deaths':int(data.death.sum())}]
    missing = data[required].isna().sum()
    if missing.any():
        raise ValueError('Required model variables contain missing values: '+str(missing[missing.gt(0)].to_dict()))
    flow.append({'stage':'primary eligible; no exclusions', 'admissions':len(data), 'deaths':int(data.death.sum())})
    pd.DataFrame(flow).to_csv(OUT/'model_flow.csv', index=False)
    verified = data.loc[data.residence_area_mapping_verified].copy()
    specifications = [
        ('primary', data, CORE, 'nonrobust'),
        ('resident_only', data.loc[~data.residence_foreign], CORE, 'nonrobust'),
        ('exclude_2017_2023', data.loc[~data.source_year.isin([2017,2023])], CORE, 'nonrobust'),
        ('verified_years_core', verified, CORE, 'nonrobust'),
        ('verified_years_residence', verified, CORE+['residence_area'], 'nonrobust'),
        ('post_outcome_los', data, CORE+['los_group'], 'nonrobust'),
        ('known_ethnicity', data.loc[data.ethnicity.ne('9')], CORE, 'nonrobust'),
        ('record_HC0', data, CORE, 'HC0'),
    ]
    all_rows, diagnostics = [], []
    primary_result = primary_x = primary_terms = None
    for name, frame, variables, covariance in specifications:
        rows, diagnostic, result, x, terms = fit_one(frame.copy(), name, variables, covariance)
        all_rows.extend(rows)
        diagnostics.append(diagnostic)
        if name == 'primary':
            primary_result, primary_x, primary_terms = result, x, terms
            pd.DataFrame(crude_contrasts(frame, terms)).to_csv(OUT/'crude_odds_ratios.csv', index=False)
            primary_result.cov_params().to_csv(OUT/'primary_covariance.csv', index_label='term')
            counts = []
            for variable in CORE:
                for level, group in frame.groupby(variable, sort=False):
                    counts.append(dict(variable=variable, level=level, admissions=len(group), deaths=int(group.death.sum()), alive=int(len(group)-group.death.sum())))
            pd.DataFrame(counts).to_csv(OUT/'marginal_outcome_counts.csv', index=False)
        print(name, 'n=',len(frame),'deaths=',int(frame.death.sum()),'converged=',result.converged,
              'max_score=',diagnostic['score_max_abs'], flush=True)
    coefficients = pd.DataFrame(all_rows)
    coefficients.to_csv(OUT/'all_model_coefficients.csv', index=False)
    (OUT/'model_diagnostics.json').write_text(json.dumps(diagnostics, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    base = coefficients.loc[coefficients.model.eq('primary')]
    compare = coefficients.loc[coefficients.model.ne('primary')].merge(
        base[['term', 'reference', 'beta', 'aor']].rename(columns={'beta':'primary_beta', 'aor':'primary_aor'}),
        on=['term','reference'], how='left', validate='many_to_one')
    compare['log_or_change'] = compare.beta-compare.primary_beta
    compare['or_ratio_to_primary'] = compare.aor/compare.primary_aor
    compare.to_csv(OUT/'sensitivity_comparison.csv', index=False)
    pd.DataFrame(diagnostics).drop(columns=['references','warnings']).to_csv(OUT/'model_sample_sizes_and_fit.csv', index=False)
    lines=['# Rebuilt Table 4 — adjusted associations with in-hospital death', '',
           'Primary logistic model: all audited C71 admissions, 2015–2024; death=1, live discharge=0. Final length of stay and provisional residence-area labels excluded.', '',
           '| Variable | Category vs reference | Admissions | Deaths | aOR | 95% Wald CI | Wald p | Sparse level |',
           '|---|---|---:|---:|---:|---|---:|---|']
    for row in base.itertuples():
        level = ETHNICITY.get(row.level,row.level) if row.variable=='ethnicity' else row.level
        reference = ETHNICITY.get(row.reference,row.reference) if row.variable=='ethnicity' else row.reference
        p = '<0.001' if row.p_value < .001 else f'{row.p_value:.3f}'
        lines.append(f'| {row.variable} | {level} vs {reference} | {row.admissions} | {row.deaths} | {row.aor:.3f} | {row.lower_95:.3f}–{row.upper_95:.3f} | {p} | {"Yes" if row.sparse_level else ""} |')
    lines += ['', 'References: ages 0–17, male (Hombre), Mestizo ethnicity (code 6), private sector, supratentorial anatomy and discharge year 2015. Reference categories are coded in the model and are not separately estimated. Sparse flags identify levels with fewer than ten deaths or live discharges; their estimates are imprecise. Supplementary profile-likelihood intervals for these levels are generated by profile_sparse_mortality.py and saved in provenance/t04/sparse_profile_intervals.csv.', '',
              'Intervals and p-values assume independent admission records. They do not account for repeated admissions of the same person or unobserved facility clustering. These are adjusted admission-level associations, not causal effects, patient survival estimates or a validated prediction tool.', '',
              'The primary model has 10,972 admissions and 963 deaths; no exclusions for source-coded unknown ethnicity. Unknown ethnicity is retained as code 9. No significance-based variable selection. HC0 and specified sensitivity results are in the T04 evidence files.', '']
    (TABLES/'table4_rebuilt.md').write_text('\n'.join(lines), encoding='utf-8')
    base.to_csv(TABLES/'table4_rebuilt.csv', index=False)
    inputs = {'data/processed/admissions_c71_audited.csv':hashlib.sha256(path.read_bytes()).hexdigest(),
              'provenance/t04/analysis_specification.md':hashlib.sha256((OUT/'analysis_specification.md').read_bytes()).hexdigest()}
    (OUT/'run_metadata.json').write_text(json.dumps(dict(inputs_sha256=inputs, statsmodels=sm.__version__,
        primary_event='death=1', primary_covariance='Observed-information, independent admissions',
        assumption='Unobserved patient/facility dependence remains unresolved', primary_references=diagnostics[0]['references']), indent=2)+'\n', encoding='utf-8')
    print(base.loc[base.variable.isin(['age_group','sector_binary']), ['term','aor','lower_95','upper_95','p_value']].to_string(index=False))

if __name__ == '__main__':main()
