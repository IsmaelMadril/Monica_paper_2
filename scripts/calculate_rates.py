"""T03: national admission/death rates and admission-level fatality, with model-based CIs.

Method references and study-specific choices: Writeable/reconstruction_rationale.md.
Fay-Feuer (1997) for rate intervals; Wilson (1927) for admission proportions.
"""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import gamma, norm
from prepare_population import group_age

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / 'provenance/t03'
TABLES = ROOT / 'outputs/tables'
ANATOMY = ['Total', 'Overlapping', 'Infratentorial/midline', 'Supratentorial', 'Unspecified']
SCALE = 100000


def standardized_rate(counts, coefficients, alpha=0.05):
    """Weighted independent-Poisson sum; Fay–Feuer gamma interval, per 100,000.

    coefficients = fixed standard weight / annual population (or mean-rate coefficient).
    Zero-count strata remain in the vector so the conservative upper weight is correct.
    """
    k = np.asarray(counts, dtype=float)
    a = np.asarray(coefficients, dtype=float)
    if k.shape != a.shape or k.size == 0:
        raise ValueError('Counts and coefficients must be nonempty matching vectors')
    if not np.isfinite(k).all() or not np.isfinite(a).all() or (k < 0).any() or (a <= 0).any():
        raise ValueError('Finite nonnegative counts and positive coefficients required')
    if not np.equal(k, np.floor(k)).all():
        raise ValueError('Event counts must be integers')
    rate = float(np.dot(k, a))
    variance = float(np.dot(k, a*a))
    maximum = float(a.max())
    lower = 0.0 if rate == 0 else float(gamma.ppf(alpha/2, rate*rate/variance, scale=variance/rate))
    augmented = rate + maximum
    augmented_variance = variance + maximum*maximum
    upper = float(gamma.ppf(1-alpha/2, augmented*augmented/augmented_variance,
                           scale=augmented_variance/augmented))
    return dict(rate_per_100k=rate*SCALE, lower_95=lower*SCALE, upper_95=upper*SCALE,
                variance_per_100k2=variance*SCALE*SCALE)


def wilson(deaths, admissions, alpha=0.05):
    if admissions <= 0 or deaths < 0 or deaths > admissions:
        raise ValueError('Require 0 <= deaths <= admissions and positive admissions')
    z = float(norm.ppf(1-alpha/2))
    p = deaths/admissions
    denominator = 1+z*z/admissions
    center = (p+z*z/(2*admissions))/denominator
    margin = z*math.sqrt(p*(1-p)/admissions+z*z/(4*admissions*admissions))/denominator
    return p*100, (center-margin)*100, (center+margin)*100


def fingerprint(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def cell(estimate):
    return f"{estimate.rate_per_100k:.3f} ({estimate.lower_95:.3f}–{estimate.upper_95:.3f})"


def main():
    PROV.mkdir(exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    cohort_path = ROOT/'data/processed/admissions_c71_audited.csv'
    cohort = pd.read_csv(cohort_path)
    assert cohort.admission_id.is_unique
    assert cohort.age_years_completed.notna().all() and cohort.death.isin([0, 1]).all()
    assert cohort.residence_province_unknown.eq(False).all()
    weights = pd.read_csv(PROV/'standard_weights_2022.csv')
    population = pd.read_csv(PROV/'annual_population_by_age.csv')
    assert population.population.gt(0).all()
    assert not population.duplicated(['scheme', 'year', 'age_group']).any()
    policies = {'resident': cohort.loc[~cohort.residence_foreign].copy(), 'all_discharges': cohort.copy()}
    annual, specific, fatality, summaries, selections = [], [], [], [], []
    for policy, data in policies.items():
        for year in range(2015, 2025):
            original = cohort.loc[cohort.source_year.eq(year)]
            included = data.loc[data.source_year.eq(year)]
            selections.append(dict(policy=policy, year=year, source_admissions=len(original),
                                   foreign_excluded=len(original)-len(included), included_admissions=len(included),
                                   deaths=int(included.death.sum())))
        for scheme in ['five_groups', 'five_years']:
            data = data.assign(rate_age_group=data.age_years_completed.map(lambda a: group_age(a, scheme)))
            w = weights.loc[weights.scheme.eq(scheme)].set_index('age_group')
            assert abs(w.standard_weight.sum()-1) < 1e-12
            pop = population.loc[population.scheme.eq(scheme)]
            for location in ANATOMY:
                subset = data if location == 'Total' else data.loc[data.anatomy.eq(location)]
                annual_vectors = {'admissions': [], 'deaths': []}
                grouped = subset.groupby(['source_year', 'rate_age_group']).agg(admissions=('admission_id', 'size'), deaths=('death', 'sum'))
                for year in range(2015, 2025):
                    p = pop.loc[pop.year.eq(year)].set_index('age_group').reindex(w.index)
                    k = grouped.reindex(pd.MultiIndex.from_product([[year], w.index]), fill_value=0)
                    coefficients = w.standard_weight.to_numpy()/p.population.to_numpy()
                    for measure in ['admissions', 'deaths']:
                        values = k[measure].to_numpy()
                        for age, count, denominator, standard_weight in zip(w.index, values, p.population, w.standard_weight):
                            age_estimate = standardized_rate([count], [1/denominator])
                            specific.append(dict(policy=policy, scheme=scheme, year=year, anatomy=location,
                                                 measure=measure, age_group=age, count=int(count), population=int(denominator),
                                                 standard_weight=standard_weight, **age_estimate))
                        estimate = standardized_rate(values, coefficients)
                        annual.append(dict(policy=policy, scheme=scheme, year=year, anatomy=location,
                                           measure=measure, events=int(values.sum()), sparse_events=bool(values.sum()<10), **estimate))
                        annual_vectors[measure].append((values, coefficients))
                    if scheme == 'five_groups' and int(k.admissions.sum()) > 0:
                        d, n = int(k.deaths.sum()), int(k.admissions.sum())
                        percent, low, high = wilson(d, n)
                        fatality.append(dict(policy=policy, period=str(year), anatomy=location, admissions=n, deaths=d,
                                             percent=percent, lower_95=low, upper_95=high))
                for measure, vectors in annual_vectors.items():
                    counts = np.concatenate([k for k, _ in vectors])
                    coefficients = np.concatenate([a/10 for _, a in vectors])
                    estimate = standardized_rate(counts, coefficients)
                    summaries.append(dict(policy=policy, scheme=scheme, anatomy=location, measure=measure,
                                          estimator='arithmetic_mean_of_10_annual_standardized_rates', events=int(counts.sum()), **estimate))
                    # Alternative estimator: aggregate events and age-specific population-years first.
                    pooled_counts = np.stack([k for k, _ in vectors]).sum(axis=0)
                    pooled_pop = pop.groupby('age_group').population.sum().reindex(w.index).to_numpy()
                    pooled = standardized_rate(pooled_counts, w.standard_weight.to_numpy()/pooled_pop)
                    summaries.append(dict(policy=policy, scheme=scheme, anatomy=location, measure=measure,
                                          estimator='pooled_population_years_standardized_rate', events=int(pooled_counts.sum()), **pooled))
                if scheme == 'five_groups' and len(subset) > 0:
                    d, n = int(subset.death.sum()), len(subset)
                    percent, low, high = wilson(d, n)
                    fatality.append(dict(policy=policy, period='2015-2024', anatomy=location, admissions=n, deaths=d,
                                         percent=percent, lower_95=low, upper_95=high))
    a, s, f = pd.DataFrame(annual), pd.DataFrame(summaries), pd.DataFrame(fatality)
    # Arithmetic identities are checked using unrounded values, never confidence limits.
    for keys, frame in a.groupby(['policy', 'scheme', 'year', 'measure']):
        assert math.isclose(frame.loc[frame.anatomy.eq('Total'), 'rate_per_100k'].iloc[0],
                            frame.loc[frame.anatomy.ne('Total'), 'rate_per_100k'].sum(), abs_tol=1e-12)
    paired = a.pivot(index=['policy', 'scheme', 'year', 'anatomy'], columns='measure', values='rate_per_100k')
    assert (paired.deaths <= paired.admissions+1e-12).all()
    for row in s.loc[s.estimator.str.startswith('arithmetic')].itertuples():
        series = a.loc[a.policy.eq(row.policy) & a.scheme.eq(row.scheme) & a.anatomy.eq(row.anatomy) & a.measure.eq(row.measure)]
        assert math.isclose(row.rate_per_100k, series.rate_per_100k.mean(), abs_tol=1e-12)
    a.to_csv(PROV/'annual_standardized_rates.csv', index=False)
    pd.DataFrame(specific).to_csv(PROV/'age_specific_rates.csv', index=False)
    s.to_csv(PROV/'period_summary_rates.csv', index=False)
    f.to_csv(PROV/'admission_fatality.csv', index=False)
    pd.DataFrame(selections).to_csv(PROV/'rate_cohort_selection.csv', index=False)
    main = a.loc[a.policy.eq('resident') & a.scheme.eq('five_groups')]
    primary_summary = s.loc[s.policy.eq('resident') & s.scheme.eq('five_groups') & s.estimator.str.startswith('arithmetic')]
    lines = ['# Rebuilt Table 3', '', 'Resident C71-coded hospital discharges, Ecuador, 2015–2024. Direct standardization to the actual 2022 census distribution using five age groups. Rates per 100,000 residents; 95% model-based Fay–Feuer intervals in parentheses.', '']
    for measure, label in [('admissions', 'Age-adjusted hospitalization rate (AAHR)'), ('deaths', 'Age-adjusted in-hospital death rate (AAIMR)')]:
        lines += [f'## {label}', '', '| Year | Total | Overlapping | Infratentorial/midline | Supratentorial | Unspecified |', '|---|---:|---:|---:|---:|---:|']
        for year in range(2015, 2025):
            frame = main.loc[main.year.eq(year) & main.measure.eq(measure)].set_index('anatomy')
            lines.append('| '+str(year)+' | '+' | '.join(cell(frame.loc[k]) for k in ANATOMY)+' |')
        frame = primary_summary.loc[primary_summary.measure.eq(measure)].set_index('anatomy')
        lines.append('| Mean annual rate | '+' | '.join(cell(frame.loc[k]) for k in ANATOMY)+' |')
        lines += ['']
    lines += ['Three foreign-resident live discharges are excluded from resident-population rates (one in 2018, two in 2019). All-discharge sensitivity results, narrower age bands, age-specific rates, fatality percentages and pooled population-year estimates are provided in the T03 CSV outputs.', '', 'The mean row is the arithmetic mean of ten annual standardized rates. Its interval is calculated from the weighted sum of annual age-specific event counts, not by averaging interval limits. Small event counts (<10) are flagged in the machine-readable table; component intervals do not add to the total interval.', '', 'Poisson and Wilson intervals assume independent event records and fixed population denominators. Repeat admissions, facility clustering, systematic record errors and population-estimation uncertainty are not represented; these are conditional model-based intervals, not patient-level risk intervals. No trend hypothesis test is reported.', '']
    lines += [
        '## Sources and methodological rationale', '',
        'Discharge data: [INEC Camas y Egresos Hospitalarios](https://www.ecuadorencifras.gob.ec/camas-y-egresos-hospitalarios/). Annual denominators: [INEC Revision 2024](https://www.ecuadorencifras.gob.ec/proyecciones-poblacionales/), national sheet 1.1. Standard weights: [observed Ecuador 2022 census workbook](https://www.censoecuador.gob.ec/wp-content/uploads/2024/04/01_2022_CPV_Estructura_poblacional.xlsx), sheet 3. Exact source versions and hashes are in population_manifest.csv and inec_download_manifest.csv.', '',
        'Direct standardization follows the [NCI SEER rate definition](https://seer.cancer.gov/seerstat/tutorials/aarates/definition.html); rate intervals use [Fay and Feuer (1997)](https://wonder.cdc.gov/controller/pdf/FayFeuerConfidenceIntervals.pdf). Admission-fatality intervals in the accompanying CSV use [Wilson (1927)](https://jhanley.biostat.mcgill.ca/c607/ch08/wilson_jasa_1927.pdf).', '',
        'The Ecuador standard, five primary age bands, resident-only primary analysis, arithmetic mean and sparse-event flag are explicit study choices. Their arguments, evidence and limitations are in the [bibliographic rationale](../../Writeable/reconstruction_rationale.md), [decision register](../../provenance/reconstruction_decisions.csv) and [BibTeX library](../../references/reconstruction.bib). These sources support the methods; the [verification report](../../Writeable/table3_verification.md) documents the resulting numbers.', '',
    ]
    (TABLES/'table3_rebuilt.md').write_text('\n'.join(lines), encoding='utf-8')
    main.to_csv(TABLES/'table3_rebuilt.csv', index=False)
    source_files = [cohort_path, PROV/'population_manifest.csv', PROV/'annual_population_by_age.csv', PROV/'standard_weights_2022.csv']
    inputs = {p.relative_to(ROOT).as_posix(): fingerprint(p) for p in source_files}
    (PROV/'run_metadata.json').write_text(json.dumps(dict(recorded_utc=datetime.now(timezone.utc).isoformat(), inputs_sha256=inputs,
        primary_policy='resident; exclude source province code88 foreign; no unknown residence province in audited cohort',
        primary_age_groups=['0-17', '18-44', '45-64', '65-79', '80+'], standard='Actual CPV2022 census; 16,938,986 persons',
        denominator='June30 annual population; INEC Revision2024 expanded workbookv2',
        rate_ci='Fay-Feuer gamma; independent Poisson counts, fixed denominators', fatality_ci='Wilson binomial; admission records',
        methodological_rationale='Writeable/reconstruction_rationale.md',
        decision_register='provenance/reconstruction_decisions.csv',
        bibliography='references/reconstruction.bib',
        validation='Additivity, death<=admission component, exact mean reproduction passed'), indent=2)+'\n', encoding='utf-8')
    print(primary_summary.loc[primary_summary.anatomy.eq('Total'), ['measure', 'rate_per_100k', 'lower_95', 'upper_95']].to_string(index=False))
    print(f.loc[f.policy.eq('resident') & f.period.eq('2015-2024') & f.anatomy.eq('Total')].to_string(index=False))

if __name__ == '__main__':
    main()
