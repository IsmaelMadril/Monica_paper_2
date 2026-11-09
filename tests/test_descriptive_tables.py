"""Independent denominator, conditional-tail and model-presentation controls for T06."""
import json
import math
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd
from scipy.stats import chi2, fisher_exact

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from generate_descriptive_tables import independence_test, summarize
from table_reporting import p_text


class DescriptiveMethods(unittest.TestCase):
    def test_large_table_matches_independent_pearson_calculation(self):
        counts = np.array([[30,20],[10,40]])
        expected = np.outer(counts.sum(1),counts.sum(0))/counts.sum()
        statistic = ((counts-expected)**2/expected).sum()
        result = independence_test(counts,123)
        self.assertEqual(result['method'],'Pearson chi-square (no continuity correction)')
        self.assertAlmostEqual(result['statistic'],statistic)
        self.assertAlmostEqual(result['p_value'],chi2.sf(statistic,1))

    def test_sparse_two_by_two_uses_two_sided_fisher(self):
        counts = [[1,9],[11,3]]
        result = independence_test(counts,123)
        self.assertEqual(result['method'],'Fisher exact (two-sided)')
        self.assertAlmostEqual(result['p_value'],fisher_exact(counts,alternative='two-sided').pvalue)

    def test_monte_carlo_matches_enumerated_small_conditional_distribution(self):
        # All 2x3 tables with column margins (2,2,2) and row margins (3,3).
        counts = np.array([[2,1,0],[0,1,2]])
        observed = ((counts-1)**2).sum()
        probability = 0.
        for a in range(3):
            for b in range(3):
                c = 3-a-b
                if 0<=c<=2:
                    candidate = np.array([[a,b,c],[2-a,2-b,2-c]])
                    if ((candidate-1)**2).sum() >= observed:
                        probability += math.comb(2,a)*math.comb(2,b)*math.comb(2,c)/math.comb(6,3)
        result = independence_test(counts,123,replicates=19999)
        self.assertEqual(result['method'],'Fixed-margin Monte Carlo Pearson')
        self.assertAlmostEqual(result['p_value'],probability,delta=5*result['monte_carlo_se'])
        self.assertEqual(result,independence_test(counts,123,replicates=19999))

    def test_zero_margin_and_invalid_counts(self):
        result = independence_test([[0,0],[20,30],[30,20]],123)
        self.assertEqual(result['active_rows'],2)
        self.assertEqual(independence_test([[0,0],[20,30]],123)['p_value'],None)
        for invalid in [[[1,-1],[2,3]],[[.5,1],[2,3]]]:
            with self.assertRaises(ValueError):
                independence_test(invalid,123)

    def test_missing_and_unknown_keep_distinct_denominators(self):
        frame = pd.DataFrame({'ethnicity':['6','9',None,'6'],'death':[0,1,1,0]})
        rows, counts = summarize(frame,'ethnicity',['6','9'],('death',[0,1]))
        self.assertEqual(counts.tolist(),[[2,0],[0,1],[0,1]])
        unknown = next(r for r in rows if r['level']=='9' and r['outcome']=='1')
        self.assertEqual(unknown['column_percent'],50)
        self.assertEqual(unknown['group_admissions'],1)
        self.assertEqual(len([r for r in rows if r['level']=='Missing']),2)

    def test_p_precision_not_substituted_by_point_zero_zero_one(self):
        self.assertEqual(p_text(.000123456),'1.23e-04')
        self.assertEqual(p_text(.078383),'0.0784')
        self.assertNotEqual(p_text(1e-20),'0')


@unittest.skipUnless((ROOT/'provenance/t06/run_metadata.json').exists(),'Run T06 first')
class DescriptiveIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pd.read_csv(ROOT/'data/processed/admissions_c71_audited.csv')
        cls.tables = {i:pd.read_csv(ROOT/f'provenance/t06/table{i}_cells.csv') for i in [1,2]}

    def test_every_cell_reconciles_to_source_counts_and_denominator(self):
        source = self.data.copy()
        source['ethnicity'] = source.etnia.astype(int).astype(str)
        source['year'] = source.source_year.astype(str)
        for number,table in self.tables.items():
            for r in table.itertuples():
                frame = source.loc[source.residence_area_mapping_verified] if r.variable=='residence_area' else source
                variable = 'death' if number==1 else 'anatomy'
                outcome = int(r.outcome) if number==1 else r.outcome
                group = frame[r.variable].astype(str).eq(str(r.level))
                mask = frame[variable].eq(outcome)
                self.assertEqual(r.count,int((group & mask).sum()))
                self.assertEqual(r.column_denominator,int(mask.sum()))
                self.assertEqual(r.group_admissions,int(group.sum()))
                self.assertAlmostEqual(r.column_percent,100*r.count/r.column_denominator)

    def test_2024_alive_percentage_and_fatality_have_different_denominators(self):
        table = self.tables[1]
        row = table.loc[table.variable.eq('year') & table.level.eq('2024') & table.outcome.eq(0)].iloc[0]
        self.assertEqual((row.group_admissions,row['count'],row.column_denominator),(1019,932,10009))
        self.assertAlmostEqual(row.column_percent,932/10009*100)
        self.assertAlmostEqual(row.fatality_percent,87/1019*100)

    def test_residence_restriction_and_source_unknown_are_explicit(self):
        scopes = pd.read_csv(ROOT/'provenance/t06/table_scopes.csv')
        for r in scopes.itertuples():
            self.assertEqual(r.included,7621 if r.variable=='residence_area' else 10972)
            self.assertEqual(r.excluded,3351 if r.variable=='residence_area' else 0)
        missing = pd.read_csv(ROOT/'provenance/t06/missingness.csv')
        self.assertTrue(missing.null_count.eq(0).all())
        self.assertTrue(missing.loc[missing.variable.eq('ethnicity'),'source_unknown_count'].eq(1290).all())

    def test_anatomical_totals_and_all_characteristic_reconciliation(self):
        table = self.tables[2]
        expected = {'Supratentorial':4669,'Infratentorial/midline':1523,'Overlapping':112,'Unspecified':4668}
        for variable,frame in table.groupby('variable'):
            for outcome,subset in frame.groupby('outcome'):
                self.assertEqual(subset['count'].sum(),subset.column_denominator.iloc[0])
                if variable!='residence_area':
                    self.assertEqual(subset['count'].sum(),expected[outcome])
        checks = pd.read_csv(ROOT/'provenance/t06/reconciliation.csv')
        self.assertTrue(checks.passed.all())
        self.assertTrue(checks.counted.eq(checks.expected).all())

    def test_model_csvs_unchanged_and_legends_consistent(self):
        for number,stage in [(4,'t04'),(5,'t05')]:
            expected = pd.read_csv(ROOT/f'provenance/{stage}/all_model_coefficients.csv').query('model=="primary"').reset_index(drop=True)
            actual = pd.read_csv(ROOT/f'outputs/tables/table{number}_rebuilt.csv')
            pd.testing.assert_frame_equal(actual,expected)
            text = (ROOT/f'outputs/tables/table{number}_rebuilt.md').read_text()
            self.assertNotIn('schizophrenia',text.lower())
            self.assertNotIn('Hombre',text)
            self.assertIn('Wald',text)
            self.assertIn('References',text)
        metadata = json.loads((ROOT/'provenance/t06/run_metadata.json').read_text())
        self.assertFalse(metadata['model_estimates_changed'])


if __name__=='__main__':
    unittest.main()
