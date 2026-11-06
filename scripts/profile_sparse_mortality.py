"""Supplementary profile-likelihood intervals for sparse primary mortality levels."""
import warnings
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import chi2
import statsmodels.api as sm
from fit_mortality import ROOT, OUT, CORE, design


def profile_interval(x, y, fitted, parameter):
    names = list(x.columns)
    j = names.index(parameter)
    others = [i for i in range(len(names)) if i != j]
    reduced = x.iloc[:, others]
    fixed = x.iloc[:, j].to_numpy()
    center, se = float(fitted.params.iloc[j]), float(fitted.bse.iloc[j])
    target = float(chi2.ppf(.95, 1))
    cache = {}
    def equation(value):
        if value not in cache:
            with warnings.catch_warnings(record=True) as messages:
                warnings.simplefilter('always')
                result = sm.GLM(y, reduced, family=sm.families.Binomial(), offset=fixed*value).fit(
                    start_params=fitted.params.iloc[others], maxiter=100, tol=1e-10)
            if not result.converged or messages:
                raise RuntimeError('Profile nuisance fit failed/warned')
            cache[value] = 2*(fitted.llf-result.llf)-target
        return cache[value]
    endpoints=[]
    for direction in [-1, 1]:
        step = max(2*se, .25)
        boundary = center+direction*step
        for _ in range(12):
            if equation(boundary)>0:break
            step *= 2
            boundary = center+direction*step
        else:raise RuntimeError('Profile bound could not be bracketed')
        endpoints.append(brentq(equation, min(center,boundary), max(center,boundary), xtol=1e-8))
    return np.exp(endpoints)


def main():
    metadata = json.loads((OUT/'run_metadata.json').read_text(encoding='utf-8'))
    for relative, expected in metadata['inputs_sha256'].items():
        with (ROOT/relative).open('rb') as stream:
            if hashlib.file_digest(stream, 'sha256').hexdigest() != expected:
                raise ValueError('Primary inputs changed; rerun fit_mortality.py before profiling')
    data = pd.read_csv(ROOT/'data/processed/admissions_c71_audited.csv')
    data['ethnicity'] = data.etnia.astype(int).astype(str)
    data['year'] = data.source_year.astype(int).astype(str)
    x, _, _ = design(data, CORE)
    fitted = sm.GLM(data.death.to_numpy(), x, family=sm.families.Binomial()).fit(maxiter=100,tol=1e-10)
    primary = pd.read_csv(OUT/'all_model_coefficients.csv').query("model=='primary' and sparse_level")
    rows=[]
    for row in primary.itertuples():
        if not np.isclose(np.exp(fitted.params[row.term]), row.aor, rtol=1e-10, atol=1e-12):
            raise ValueError('Primary coefficients stale; rerun fit_mortality.py')
        low, high = profile_interval(x, data.death.to_numpy(), fitted, row.term)
        rows.append(dict(term=row.term, admissions=row.admissions, deaths=row.deaths, aor=row.aor,
                         wald_lower_95=row.lower_95, wald_upper_95=row.upper_95,
                         profile_lower_95=low, profile_upper_95=high))
        print(row.term, 'profile interval', low, high, flush=True)
    pd.DataFrame(rows).to_csv(OUT/'sparse_profile_intervals.csv', index=False)

if __name__=='__main__':main()
