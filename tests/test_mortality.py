"""Outcome direction, separation detection and independent logistic controls for T04."""
import json
import hashlib
from pathlib import Path
import struct
import sys
import unittest
from unittest import mock
import tempfile
import zipfile
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from fit_mortality import design, separation_check, fit_one
from inspect_legacy_mortality import decode_encoding
import inspect_legacy_mortality as legacy_inspector
from profile_sparse_mortality import profile_interval
ROOT = Path(__file__).resolve().parents[1]

class MortalityMethods(unittest.TestCase):
    def test_separation_detects_complete_and_quasi(self):
        x = np.column_stack([np.ones(4), [-2, -1, 1, 2]])
        self.assertTrue(separation_check(x, [0, 0, 1, 1])['separation_detected'])
        x[:,1] = [-1, 0, 0, 1]
        self.assertTrue(separation_check(x, [0, 0, 1, 1])['separation_detected'])
    def test_overlap_is_not_separation(self):
        x = np.column_stack([np.ones(4), [0, 0, 1, 1]])
        self.assertFalse(separation_check(x, [0, 1, 0, 1])['separation_detected'])
    def test_two_by_two_model_has_known_odds_ratio(self):
        frame = pd.DataFrame({'sector_binary':['Private']*10+['Public']*10,
                              'death':[1]*2+[0]*8+[1]*4+[0]*6})
        rows, diagnostic, result, x, terms = fit_one(frame, 'control', ['sector_binary'])
        self.assertAlmostEqual(rows[0]['aor'], (4/6)/(2/8), places=8)
        self.assertTrue(diagnostic['converged'])
        self.assertEqual(diagnostic['references']['sector_binary'], 'Private')
        low, high = profile_interval(x, frame.death.to_numpy(), result, 'sector_binary[Public]')
        self.assertLess(low, rows[0]['aor'])
        self.assertGreater(high, rows[0]['aor'])
    def test_predicting_survival_reverses_log_odds(self):
        frame = pd.DataFrame({'sector_binary':['Private']*10+['Public']*10,
                              'death':[1]*2+[0]*8+[1]*4+[0]*6})
        death, *_ = fit_one(frame, 'death', ['sector_binary'])
        frame.death = 1-frame.death
        survival, *_ = fit_one(frame, 'survival', ['sector_binary'])
        self.assertAlmostEqual(death[0]['beta'], -survival[0]['beta'], places=9)
    def test_unavailable_spv_preserves_historical_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            out=root/'provenance/t04'
            out.mkdir(parents=True)
            evidence=out/'legacy_encoding.json'
            evidence.write_text('{"status":"decoded"}',encoding='utf-8')
            with mock.patch.object(legacy_inspector,'ROOT',root), mock.patch.object(legacy_inspector,'OUT',out), mock.patch('builtins.print'):
                legacy_inspector.main()
            self.assertEqual(evidence.read_text(encoding='utf-8'),'{"status":"decoded"}')
    def test_unrecognized_category_fails_instead_of_dropping(self):
        with self.assertRaisesRegex(ValueError, 'Unrecognized'):
            design(pd.DataFrame({'sex':['Hombre','unexpected']}), ['sex'])

@unittest.skipUnless((ROOT/'Results/RESULTADOS.spv').exists(), 'Original SPV not restored')
class LegacyEncoding(unittest.TestCase):
    def test_decoded_original_event_is_survival(self):
        with zipfile.ZipFile(ROOT/'Results/RESULTADOS.spv') as archive:
            data = archive.read('00000000055_lightTableData.bin')
        encoding = decode_encoding(data)
        self.assertEqual(encoding['Fallecid']['internal_value'],0)
        self.assertEqual(encoding['Vivo']['internal_value'],1)
        broken = bytearray(data)
        broken[-8:] = struct.pack('<d',2)
        with self.assertRaises(ValueError):decode_encoding(broken)

@unittest.skipUnless((ROOT/'provenance/t04/all_model_coefficients.csv').exists(), 'Run T04 first')
class MortalityIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.coefficients=pd.read_csv(ROOT/'provenance/t04/all_model_coefficients.csv')
        cls.diagnostics=json.loads((ROOT/'provenance/t04/model_diagnostics.json').read_text(encoding='utf-8'))
    def test_t03_cohort_matches_up_to_line_endings(self):
        raw=(ROOT/'data/processed/admissions_c71_audited.csv').read_bytes()
        lf=raw.replace(b'\r\n',b'\n')
        expected=json.loads((ROOT/'provenance/t03/run_metadata.json').read_text(encoding='utf-8'))['inputs_sha256']['data/processed/admissions_c71_audited.csv']
        variants=[hashlib.sha256(x).hexdigest() for x in [raw,lf,lf.replace(b'\n',b'\r\n')]]
        self.assertIn(expected,variants)
    def test_primary_sample_covariates_and_event(self):
        primary=next(r for r in self.diagnostics if r['model']=='primary')
        self.assertEqual((primary['admissions'],primary['deaths']),(10972,963))
        self.assertEqual(primary['parameters'],27)
        x=self.coefficients.query("model=='primary'")
        self.assertFalse(x.variable.isin(['los_group','residence_area']).any())
        encoding=pd.read_csv(ROOT/'provenance/t04/outcome_encoding.csv')
        self.assertEqual(dict(zip(encoding.con_egrpa,encoding.death)),{1:0,2:1,3:1})
    def test_all_fits_finite_converged_without_separation(self):
        self.assertEqual(len(self.diagnostics),8)
        for r in self.diagnostics:
            self.assertTrue(r['converged'])
            self.assertFalse(r['separation_detected'])
            self.assertEqual(r['warnings'],[])
            self.assertEqual(r['rank'],r['parameters'])
            self.assertLess(r['score_max_abs'],1e-5)
            self.assertGreater(r['smallest_information_eigenvalue'],0)
        c=self.coefficients
        self.assertTrue(np.isfinite(c[['beta','se','aor','lower_95','upper_95']].to_numpy()).all())
        self.assertTrue((c.lower_95<c.aor).all() and (c.upper_95>c.aor).all())
    def test_robust_covariance_does_not_change_coefficients(self):
        c=self.coefficients
        p=c.query("model=='primary'").set_index('term')
        h=c.query("model=='record_HC0'").set_index('term')
        np.testing.assert_allclose(p.beta,h.beta,rtol=0,atol=1e-12)
    def test_restricted_year_reference_and_profile_outputs(self):
        restricted=next(r for r in self.diagnostics if r['model']=='verified_years_residence')
        self.assertEqual(restricted['references']['year'],'2018')
        self.assertEqual(restricted['admissions'],7621)
        p=pd.read_csv(ROOT/'provenance/t04/sparse_profile_intervals.csv')
        self.assertEqual(len(p),6)
        self.assertTrue((p.profile_lower_95<p.aor).all() and (p.profile_upper_95>p.aor).all())

if __name__=='__main__':unittest.main()
