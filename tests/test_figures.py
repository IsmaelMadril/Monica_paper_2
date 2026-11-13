"""T09 independent rate/denominator, geography-join and geometry controls."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
HAVE_PLOTTING=importlib.util.find_spec('matplotlib') is not None
if HAVE_PLOTTING:
    from generate_figures import province_grid,join_boundaries,validate_rates,polygon_path,ring_area,YEARS,PROVINCES


@unittest.skipUnless(HAVE_PLOTTING,'Install requirements-figures.txt for T09 controls')
class FigureMethods(unittest.TestCase):
    def toy(self):
        return pd.DataFrame({'source_year':YEARS,'prov_res':['20']*10,
                             'residence_province':['Galapagos','Galápagos']*5})

    def test_code_joins_unify_accent_variants_without_losing_records(self):
        result=province_grid(self.toy(),'prov_res','residence_province',True)
        self.assertEqual(len(result),240)
        self.assertEqual(result.admissions.sum(),10)
        self.assertEqual(set(result.loc[result.province_code.eq('20'),'admissions']),{1})
        zeros=result.loc[result.province_code.eq('01')]
        self.assertTrue(zeros.admissions.eq(0).all())
        self.assertTrue(zeros.status.eq('observed_zero').all())

    def test_missing_year_is_not_silently_plotted_as_zero(self):
        with self.assertRaisesRegex(ValueError,'ten audited source years'):
            province_grid(self.toy().iloc[:-1],'prov_res','residence_province',True)

    def test_unknown_or_inconsistent_province_rejected(self):
        for code,name in [('99','Unknown'),(None,'Galápagos'),('20','Guayas')]:
            frame=self.toy();frame.loc[0,'prov_res']=code;frame.loc[0,'residence_province']=name
            with self.assertRaises(ValueError):province_grid(frame,'prov_res','residence_province',True)

    def test_foreign_residence_not_joined_to_a_domestic_province(self):
        frame=self.toy();frame.loc[0,'prov_res']='88';frame.loc[0,'residence_province']='Exterior'
        result=province_grid(frame,'prov_res','residence_province',True)
        self.assertEqual(result.admissions.sum(),9)
        self.assertNotIn('88',set(result.province_code))
        with self.assertRaises(ValueError):province_grid(frame,'prov_res','residence_province',False)

    def test_holes_have_opposite_winding_and_invalid_ring_fails(self):
        outside=[[0,0],[0,4],[4,4],[4,0],[0,0]]
        hole=[[1,1],[3,1],[3,3],[1,3],[1,1]]
        path=polygon_path([outside,hole])
        self.assertGreater(ring_area(path.vertices[:5]),0)
        self.assertLess(ring_area(path.vertices[5:]),0)
        with self.assertRaisesRegex(ValueError,'Invalid polygon ring'):
            polygon_path([[[0,0],[1,1]]])

    def test_boundary_join_uses_name_crosswalk_not_source_iso(self):
        geo=json.loads((ROOT/'provenance/t09/ecuador_adm1.geojson').read_text())
        features,crosswalk=join_boundaries(geo)
        self.assertEqual(set(features),set(PROVINCES))
        self.assertEqual(crosswalk.loc[crosswalk.province.eq('Chimborazo'),'province_code'].iloc[0],'06')
        bad=copy.deepcopy(geo);bad['features'][0]['properties']['shapeName']='Not a province'
        with self.assertRaisesRegex(ValueError,'Unmatched'):join_boundaries(bad)
        duplicate=copy.deepcopy(geo);duplicate['features'][0]=copy.deepcopy(duplicate['features'][1])
        with self.assertRaisesRegex(ValueError,'Duplicate'):join_boundaries(duplicate)

    def test_corrupted_rate_point_or_duplicate_key_rejected(self):
        evidence=pd.read_csv(ROOT/'provenance/t03/annual_standardized_rates.csv')
        table=evidence.query('policy=="resident" and scheme=="five_groups"').copy()
        validate_rates(table,evidence)
        table.iloc[0,table.columns.get_loc('rate_per_100k')]=999.
        with self.assertRaisesRegex(ValueError,'differs'):validate_rates(table,evidence)
        duplicate=pd.concat([table.iloc[1:],table.iloc[[1]]])
        with self.assertRaisesRegex(ValueError,'unique'):validate_rates(duplicate,evidence)


@unittest.skipUnless(HAVE_PLOTTING and all((ROOT/name).exists() for name in [
    'provenance/t09/run_metadata.json','outputs/figures/figure2_residence_counts.svg',
    'outputs/figures/figureS1_2024.svg','outputs/tables/table3_rebuilt.csv',
    'data/processed/admissions_c71_audited.csv']),'Generate T09 figures first')
class FigureIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=pd.read_csv(ROOT/'data/processed/admissions_c71_audited.csv',dtype={'prov_res':str,'prov_ubi':str})
        cls.meta=json.loads((ROOT/'provenance/t09/run_metadata.json').read_text())

    def test_all_480_geographic_cells_match_independent_record_filters(self):
        for filename,field in [('figure2_residence_counts','prov_res'),('facility_counts','prov_ubi')]:
            table=pd.read_csv(ROOT/f'provenance/t09/{filename}.csv',dtype={'province_code':str})
            self.assertEqual(len(table),240)
            self.assertFalse(table.duplicated(['province_code','source_year']).any())
            for r in table.itertuples():
                expected=int((self.data[field].str.zfill(2).eq(r.province_code)&self.data.source_year.eq(r.source_year)).sum())
                self.assertEqual(r.admissions,expected)

    def test_flagged_rates_and_exact_table3_equality(self):
        rates=pd.read_csv(ROOT/'provenance/t09/figure1_rates.csv')
        source=pd.read_csv(ROOT/'outputs/tables/table3_rebuilt.csv')
        keys=['year','anatomy','measure']
        pd.testing.assert_frame_equal(rates.sort_values(keys).reset_index(drop=True),source.sort_values(keys).reset_index(drop=True))
        controls=self.meta['rate_controls']
        self.assertAlmostEqual(controls['2017_total_death_rate']['rate_per_100k'],.7581663368164497,places=12)
        self.assertEqual(controls['2017_total_death_rate']['events'],113)
        self.assertAlmostEqual(controls['2024_total_admission_rate']['rate_per_100k'],5.783972830194686,places=12)
        self.assertAlmostEqual(controls['2024_unspecified_admission_rate']['rate_per_100k'],2.1522338509559074,places=12)
        self.assertEqual(controls['2024_unspecified_admission_rate']['events'],379)

    def test_exclusions_margins_and_fixed_scale(self):
        m=pd.read_csv(ROOT/'provenance/t09/geography_reconciliation.csv')
        self.assertTrue(m.passed.all())
        self.assertEqual(m.residence_admissions.sum(),10969)
        self.assertEqual(m.facility_admissions.sum(),10972)
        self.assertEqual(m.foreign_excluded.sum(),3)
        np.testing.assert_array_equal(m.residence_admissions+m.foreign_excluded,m.source_admissions)
        self.assertEqual((self.meta['count_scale_min'],self.meta['count_scale_max']),(0,500))
        self.assertEqual(self.meta['count_scale_type'],'shared linear')

    def test_svg_contains_all_province_labels_and_maps_all_years(self):
        svg=(ROOT/'outputs/figures/figure2_residence_counts.svg').read_text()
        for name in PROVINCES.values():self.assertIn(name,svg)
        for year in YEARS:
            text=(ROOT/f'outputs/figures/figureS1_{year}.svg').read_text()
            self.assertIn(f'{year}  Admissions',text)
            self.assertIn('Galápagos inset',text)


if __name__=='__main__':unittest.main()
