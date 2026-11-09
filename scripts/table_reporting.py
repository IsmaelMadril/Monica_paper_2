"""Shared presentation of executed primary models; no fitting or estimate changes."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
LABELS = {'age_group': 'Age (years)', 'sex': 'Sex', 'ethnicity': 'Ethnicity',
          'sector_binary': 'Sector', 'sector_group': 'Detailed sector', 'anatomy': 'Recorded anatomical group',
          'year': 'Discharge year', 'source_year': 'Discharge year', 'los_group': 'Recorded stay (days)',
          'residence_area': 'Residence area (2018–2024 only)', 'Hombre': 'Male', 'Mujer': 'Female',
          'Urbana': 'Urban', 'Rural': 'Rural'}
ETHNICITY = {'1':'Indigenous', '2':'Afro-Ecuadorian/Afrodescendant (source 2)',
             '3':'Negro/a (source 3)', '4':'Mulato/a (source 4)', '5':'Montubio',
             '6':'Mestizo', '7':'White', '8':'Other', '9':'Unknown/not recorded'}


def label(value, variable=None):
    value = str(value)
    return ETHNICITY.get(value, value) if variable == 'ethnicity' else LABELS.get(value, value)


def p_text(value):
    if pd.isna(value):
        return 'Not tested'
    if value == 0:
        return '< floating-point resolution'
    return f'{value:.2e}' if value < .001 else f'{value:.3g}'


def render_models(root=ROOT, table=None):
    """Called after model execution or after the T06 saved-output validity checks."""
    tables = root/'outputs/tables'
    tables.mkdir(parents=True, exist_ok=True)
    if table in (None, 4):
        mortality = pd.read_csv(root/'provenance/t04/all_model_coefficients.csv')
        mortality = mortality.loc[mortality.model.eq('primary')]
        lines = ['# Rebuilt Table 4 — adjusted associations with in-hospital death', '',
                 'Binary logistic regression, maximum likelihood, all audited C71 admissions (2015–2024). '
                 'N=10,972; death=1 (963), live discharge=0 (10,009). No primary-model exclusions.', '',
                 '| Predictor | Category vs reference | Admissions in category | Deaths in category | aOR | 95% Wald CI | Wald p | Sparse level |',
                 '|---|---|---:|---:|---:|---|---:|---|']
        for r in mortality.itertuples():
            lines.append(f'| {label(r.variable)} | {label(r.level,r.variable)} vs {label(r.reference,r.variable)} | '
                         f'{r.admissions} | {r.deaths} | {r.aor:.3f} | {r.lower_95:.3f}–{r.upper_95:.3f} | '
                         f'{p_text(r.p_value)} | {"Yes" if r.sparse_level else ""} |')
        lines += ['', 'All included covariates: age group, sex, ethnicity, binary sector, recorded anatomical group and categorical discharge year. '
                  'References: ages 0–17, male, Mestizo (source code 6), private sector, supratentorial group and 2015. '
                  'Source ethnicity 9 is an explicit unknown category; Other is distinct. Reference rows have aOR=1 by definition and are not separately estimated.', '',
                  'aOR: adjusted odds ratio for death, conditional on the listed covariates. 95% Wald intervals and two-sided coefficient Wald p-values use observed-information covariance. '
                  'The model has 27 parameters including its intercept. Counts shown are marginal category counts, not separate fitted sample sizes. '
                  'Final stay and residence area are excluded. Sparse flags mean fewer than ten deaths or live discharges; supplementary profile-likelihood intervals are in provenance/t04/sparse_profile_intervals.csv.', '',
                  'Admission records are assumed independent; patient and facility clustering are unresolved. Exploratory comparisons have no multiplicity adjustment or significance highlighting. '
                  'These are admission-level associations, not causal effects, survival estimates or validated predictions. CSV retains full numerical p-values; displayed values use three significant digits.', '',
                  '[Model specification, diagnostics and sensitivities](../../Writeable/t04_mortality_analysis.md).', '']
        (tables/'table4_rebuilt.md').write_text('\n'.join(lines), encoding='utf-8')
        mortality.to_csv(tables/'table4_rebuilt.csv', index=False)
    if table in (None, 5):
        anatomy = pd.read_csv(root/'provenance/t05/all_model_coefficients.csv')
        primary = anatomy.loc[anatomy.model.eq('primary')]
        flow = pd.read_csv(root/'provenance/t05/model_flow.csv').set_index('panel')
        lines = ['# Rebuilt Table 5 — recorded coding and conditional anatomical group', '',
                 'Two exploratory maximum-likelihood binary logistic models replace the former multinomial model. '
                 'Both include age group, sex, binary sector and categorical discharge year (16 parameters including intercept each). '
                 'Results are adjusted odds ratios (aORs), not aRRRs.', '']
        for panel, title, event in [('coding','A. Non-C719 versus C719 coding','event=1: C710–C718; reference=0: C719'),
                                    ('site','B. Infratentorial/midline versus supratentorial','event=1: C715–C717; reference=0: C710–C714')]:
            f = flow.loc[panel]
            lines += [f'## {title}', '', f'{event}. N={f.included_admissions:,}; events={f.events:,}; non-events={f.non_events:,}. '
                      + ('No records excluded; C718 is included without asserting a single site.' if panel=='coding' else
                         f'Excludes {f.excluded_c718:,} C718 and {f.excluded_c719:,} C719 records.'), '',
                      '| Predictor | Category vs reference | aOR | 95% Wald CI | Wald p |', '|---|---|---:|---|---:|']
            for r in primary.loc[primary.panel.eq(panel)].itertuples():
                lines.append(f'| {label(r.variable)} | {label(r.level,r.variable)} vs {label(r.reference,r.variable)} | '
                             f'{r.aor:.3f} | {r.lower_95:.3f}–{r.upper_95:.3f} | {p_text(r.p_value)} |')
            lines += ['']
        lines += ['## C. All recorded categories (descriptive)', '',
                  '| Category | Admissions | Percent of all 10,972 admissions |', '|---|---:|---:|']
        for r in pd.read_csv(root/'provenance/t05/anatomy_descriptive.csv').itertuples():
            lines.append(f'| {r.anatomy} | {r.admissions} | {r.percent:.2f}% |')
        lines += ['', 'References in both models: ages 18–44, male, private sector and 2015; reference aOR=1 by definition. '
                  'Both primary models exclude ethnicity, final stay, death and residence area as predictors. Ethnicity is retained descriptively and in separate extended sensitivity models.', '',
                  '95% Wald intervals and two-sided coefficient Wald p-values use observed-information covariance assuming independent admission records. '
                  'Patient/facility clustering and systematic coding error are unresolved. Comparisons are exploratory without multiplicity adjustment or significance highlighting. '
                  'CSV retains full numerical p-values; displayed values use three significant digits.', '',
                  'C715 ventricular codes belong to the operational midline group; a sensitivity excludes them. Non-C719 coding is not validated coding accuracy. '
                  'Panel B is conditional on recorded site classification, not a missing-site correction or population tumour-location risk model. '
                  'C718 remains descriptive, with no forced compartment assignment. Period sensitivity is material; the pediatric contrast changes with the study years.', '',
                  'The legacy NOMREG Hessian warning and new separation certificates explain why the former four-outcome model is not reported. '
                  'All sample flows, fit/separation diagnostics, sensitivity estimates and sparse extended-ethnicity profile intervals are in provenance/t05/.', '',
                  '[Model decision, methods and primary sources](../../Writeable/t05_anatomy_analysis.md).', '']
        (tables/'table5_rebuilt.md').write_text('\n'.join(lines), encoding='utf-8')
        primary.to_csv(tables/'table5_rebuilt.csv', index=False)
