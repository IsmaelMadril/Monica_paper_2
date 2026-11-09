"""T05 outcome semantics, estimator controls and saved-output integrity checks."""
import json
from pathlib import Path
import sys
import unittest

import numpy as np
import pandas as pd
from scipy.special import logsumexp

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from fit_anatomy import panel_data, build_design, fit_binary, separation_certificates
ROOT=Path(__file__).resolve().parents[1]

class AnatomyMethods(unittest.TestCase):
    def test_coding_panel_includes_overlaps_but_labels_unspecified_as_zero(self):
        x=pd.DataFrame({'icd10':['C710','C715','C718','C719'],'anatomy':['Supratentorial','Infratentorial/midline','Overlapping','Unspecified']})
        c=panel_data(x,'coding')
        self.assertEqual(c.event.tolist(),[1,1,1,0])
        self.assertEqual(len(c),4)
    def test_site_panel_excludes_overlaps_and_unspecified(self):
        x=pd.DataFrame({'icd10':['C710','C715','C718','C719'],'anatomy':['Supratentorial','Infratentorial/midline','Overlapping','Unspecified']})
        c=panel_data(x,'site')
        self.assertEqual(c.icd10.tolist(),['C710','C715'])
        self.assertEqual(c.event.tolist(),[0,1])
    def test_adult_reference_is_explicit(self):
        x,terms,refs=build_design(pd.DataFrame({'age_group':['0-17','18-44','80+']}),['age_group'])
        self.assertEqual(refs['age_group'],'18-44')
        self.assertEqual(x['age_group[0-17]'].tolist(),[1,0,0])
        self.assertTrue(all(t['reference']=='18-44' for t in terms))
    def test_two_by_two_logistic_matches_hand_calculation(self):
        x=pd.DataFrame({'sector_binary':['Private']*10+['Public']*10,'event':[1]*2+[0]*8+[1]*4+[0]*6})
        rows,d,_,_,_=fit_binary(x,'control','primary',['sector_binary'])
        self.assertAlmostEqual(rows[0]['aor'],(4/6)/(2/8),places=8)
        self.assertEqual((d['events'],d['non_events']),(6,14))
        self.assertNotIn('deaths',d)
    def test_invalid_event_or_category_rejected(self):
        with self.assertRaisesRegex(ValueError,'Unrecognized'):
            build_design(pd.DataFrame({'sex':['Hombre','invalid']}),['sex'])
        with self.assertRaisesRegex(ValueError,'Binary event'):
            fit_binary(pd.DataFrame({'sector_binary':['Private','Public'],'event':[0,2]}),'control','invalid',['sector_binary'])
    def test_zero_cell_certificate_has_increasing_multinomial_likelihood(self):
        x=pd.DataFrame({'ethnicity':['1','1','6','6'],'anatomy':['Supratentorial','Unspecified','Overlapping','Supratentorial']})
        certificates=separation_certificates(x)
        self.assertEqual(len(certificates),1)
        self.assertEqual(certificates[0]['level'],'1')
        y=np.array([0,3,2,0])
        def ll(t):
            logits=np.zeros((4,4));logits[:2,2]=-t
            return float((logits[np.arange(4),y]-logsumexp(logits,axis=1)).sum())
        self.assertLess(ll(0),ll(3));self.assertLess(ll(3),ll(6))

@unittest.skipUnless((ROOT/'provenance/t05/all_model_coefficients.csv').exists(),'Run T05 first')
class AnatomyIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=pd.read_csv(ROOT/'provenance/t05/all_model_coefficients.csv')
        cls.d=json.loads((ROOT/'provenance/t05/model_diagnostics.json').read_text(encoding='utf-8'))
    def test_all_fifteen_fits_converged_without_separation(self):
        self.assertEqual(len(self.d),15)
        for d in self.d:
            self.assertTrue(d['converged']);self.assertFalse(d['separation_detected'])
            self.assertEqual(d['rank'],d['parameters']);self.assertEqual(d['warnings'],[])
            self.assertLess(d['score_max_abs'],1e-5)
            self.assertGreater(d['smallest_information_eigenvalue'],0)
        self.assertTrue(np.isfinite(self.c[['beta','se','aor','lower_95','upper_95']].to_numpy()).all())
    def test_panel_flow_and_eligibility(self):
        f=pd.read_csv(ROOT/'provenance/t05/model_flow.csv').set_index('panel')
        self.assertEqual((f.loc['coding','included_admissions'],f.loc['coding','events']),(10972,6304))
        self.assertEqual((f.loc['site','included_admissions'],f.loc['site','events']),(6192,1523))
        self.assertEqual(int(f.loc['site','excluded_c718']+f.loc['site','excluded_c719']),4780)
    def test_primary_covariates_and_references(self):
        for panel in ['coding','site']:
            c=self.c.query('panel==@panel and model=="primary"')
            self.assertEqual(set(c.variable),{'age_group','sex','sector_binary','year'})
            d=next(r for r in self.d if r['panel']==panel and r['model']=='primary')
            self.assertEqual(d['references']['age_group'],'18-44')
            self.assertEqual(d['parameters'],16)
            restricted=next(r for r in self.d if r['panel']==panel and r['model']=='verified_years_residence')
            self.assertEqual(restricted['references']['year'],'2018')
    def test_four_outcome_zero_cells_are_explicit(self):
        c=pd.read_csv(ROOT/'provenance/t05/four_outcome_separation_certificates.csv')
        self.assertEqual(set(c.level),{1,3,4,5})
        self.assertTrue(c.outcome_count.eq(0).all())
        self.assertTrue(c.other_outcomes.gt(0).all())
        descriptions=pd.read_csv(ROOT/'provenance/t05/anatomy_descriptive.csv')
        self.assertEqual(int(descriptions.admissions.sum()),10972)
        self.assertAlmostEqual(descriptions.percent.sum(),100)
    def test_hc0_and_reference_reexpression(self):
        contrasts=pd.read_csv(ROOT/'provenance/t05/reference_contrasts.csv').set_index('panel')
        for panel in ['coding','site']:
            p=self.c.query('panel==@panel and model=="primary"').set_index('term')
            h=self.c.query('panel==@panel and model=="record_HC0"').set_index('term')
            np.testing.assert_allclose(p.beta,h.beta,atol=1e-12,rtol=0)
            ratio=p.loc['age_group[0-17]','aor']/p.loc['age_group[80+]','aor']
            self.assertAlmostEqual(contrasts.loc[panel,'aor'],ratio,places=10)
    def test_sparse_extended_intervals_and_no_los(self):
        p=pd.read_csv(ROOT/'provenance/t05/sparse_profile_intervals.csv')
        self.assertEqual(len(p),8)
        self.assertTrue((p.profile_lower_95<p.aor).all() and (p.profile_upper_95>p.aor).all())
        self.assertFalse(self.c.variable.isin(['death','los_group']).any())

if __name__=='__main__':unittest.main()
