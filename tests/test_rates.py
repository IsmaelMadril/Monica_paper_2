"""Independent mathematical controls for T03 standardization and uncertainty."""
import sys
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import chi2, binomtest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from calculate_rates import standardized_rate, wilson
from prepare_population import group_age
ROOT = Path(__file__).resolve().parents[1]

class RateMethods(unittest.TestCase):
    def test_direct_standardization_and_variance(self):
        # 10/1000 and 20/2000 are both 1%; weighted rate stays 1%.
        result = standardized_rate([10, 20], [.25/1000, .75/2000])
        self.assertAlmostEqual(result['rate_per_100k'], 1000)
        expected_variance = (10*(.25/1000)**2+20*(.75/2000)**2)*100000**2
        self.assertAlmostEqual(result['variance_per_100k2'], expected_variance)
    def test_equal_coefficients_reduce_to_exact_poisson_interval(self):
        coefficient = 1/1000000
        result = standardized_rate([3, 7], [coefficient, coefficient])
        self.assertAlmostEqual(result['lower_95'], .5*chi2.ppf(.025, 20)*coefficient*100000)
        self.assertAlmostEqual(result['upper_95'], .5*chi2.ppf(.975, 22)*coefficient*100000)
    def test_zero_events_have_nonzero_upper_limit(self):
        result = standardized_rate([0, 0], [1/100000, 2/100000])
        self.assertEqual(result['rate_per_100k'], 0)
        self.assertEqual(result['lower_95'], 0)
        self.assertAlmostEqual(result['upper_95'], -np.log(.025)*2)
    def test_invalid_events_and_denominators_rejected(self):
        for counts, coefficients in [([-1], [1]), ([1], [0]), ([1.5], [1]), ([1, 2], [1])]:
            with self.assertRaises(ValueError):standardized_rate(counts, coefficients)
    def test_wilson_matches_scipy_independent_api(self):
        for deaths, admissions in [(0, 20), (10, 100), (20, 20), (963, 10969)]:
            _, low, high = wilson(deaths, admissions)
            reference = binomtest(deaths, admissions).proportion_ci(method='wilson')
            self.assertAlmostEqual(low/100, reference.low)
            self.assertAlmostEqual(high/100, reference.high)
    def test_narrow_age_bands_and_oldest_tail(self):
        self.assertEqual(group_age(0, 'five_years'), '0-4')
        self.assertEqual(group_age(84, 'five_years'), '80-84')
        self.assertEqual(group_age(85, 'five_years'), '85+')
        self.assertEqual(group_age(100, 'five_years'), '85+')

@unittest.skipUnless((ROOT/'provenance/t03/annual_standardized_rates.csv').exists(), 'Run T03 first')
class RateIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = pd.read_csv(ROOT/'provenance/t03/annual_standardized_rates.csv')
        cls.s = pd.read_csv(ROOT/'provenance/t03/period_summary_rates.csv')
    def test_components_add_and_deaths_do_not_exceed_admissions(self):
        for _, frame in self.a.groupby(['policy', 'scheme', 'year', 'measure']):
            total = frame.loc[frame.anatomy.eq('Total'), 'rate_per_100k'].iloc[0]
            self.assertAlmostEqual(total, frame.loc[frame.anatomy.ne('Total'), 'rate_per_100k'].sum(), places=12)
        p = self.a.pivot(index=['policy', 'scheme', 'year', 'anatomy'], columns='measure', values='rate_per_100k')
        self.assertTrue(p.deaths.le(p.admissions+1e-12).all())
    def test_means_reproduce_from_ten_years(self):
        for row in self.s.loc[self.s.estimator.str.startswith('arithmetic')].itertuples():
            matched = self.a.loc[self.a.policy.eq(row.policy) & self.a.scheme.eq(row.scheme) & self.a.anatomy.eq(row.anatomy) & self.a.measure.eq(row.measure)]
            self.assertEqual(len(matched), 10)
            self.assertAlmostEqual(row.rate_per_100k, matched.rate_per_100k.mean(), places=12)
    def test_population_and_standard_are_distinct_and_reconciled(self):
        p = pd.read_csv(ROOT/'provenance/t03/population_single_age.csv')
        s = pd.read_csv(ROOT/'provenance/t03/census_2022_single_age.csv')
        self.assertEqual(int(s.standard_population.sum()), 16938986)
        self.assertEqual(len(s), 101)
        self.assertEqual(len(p), 1010)
        self.assertEqual(int(p.loc[p.year.eq(2022), 'population'].sum()), 17715301)
        w = pd.read_csv(ROOT/'provenance/t03/standard_weights_2022.csv')
        for _, frame in w.groupby('scheme'):
            self.assertAlmostEqual(frame.standard_weight.sum(), 1, places=12)
    def test_foreign_exclusions_and_nonzero_2024_unspecified_rate(self):
        f = pd.read_csv(ROOT/'provenance/t03/rate_cohort_selection.csv')
        self.assertEqual(int(f.loc[f.policy.eq('resident'), 'foreign_excluded'].sum()), 3)
        self.assertEqual(int(f.loc[f.policy.eq('resident'), 'included_admissions'].sum()), 10969)
        rate = self.a.query("policy=='resident' and scheme=='five_groups' and year==2024 and anatomy=='Unspecified' and measure=='admissions'")
        self.assertEqual(int(rate.events.iloc[0]), 379)
        self.assertGreater(rate.rate_per_100k.iloc[0], 0)

if __name__ == '__main__':unittest.main()
