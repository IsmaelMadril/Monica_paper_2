"""Reconstruction must use INEC inputs independently of the thesis baseline."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import audit_admissions as audit


class AuditDependencies(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.out = self.root/'data/processed'
        self.prov = self.root/'provenance/t02'
        (self.out/'inec_c71').mkdir(parents=True)
        self.prov.mkdir(parents=True)
        archive = self.root/'data/raw/source.zip'
        archive.parent.mkdir(parents=True)
        archive.write_bytes(b'preserved INEC archive')
        pd.DataFrame([{
            'path': archive.relative_to(self.root).as_posix(),
            'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
        }]).to_csv(self.root/'provenance/inec_download_manifest.csv', index=False)
        for year in range(2015, 2025):
            row = {
                'source_year': year, 'source_row': 1, 'icd10': 'C714',
                'cau_cie10': 'C714', 'con_egrpa': 2 if year == 2024 else 1,
                'cod_edad': 4, 'edad': 62, 'dia_estad': 3,
                'prov_ubi': '17', 'prov_res': '17', 'sexo': 1, 'etnia': 6,
                'area_res': 1, 'area_ubi': 1, 'sector': 1,
                'anio_ingr': year, 'mes_ingr': 1, 'dia_ingr': 1,
                'anio_egr': year, 'mes_egr': 1, 'dia_egr': 4,
            }
            path = self.out/f'inec_c71/{year}.csv'
            pd.DataFrame([row]).to_csv(path, index=False)
            (self.prov/f'{year}_flow.json').write_text(json.dumps({
                'extract_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            }), encoding='utf-8')
            (self.prov/f'{year}_schema.json').write_text(json.dumps({
                'value_labels': {'con_egrpa': {
                    '1.0': 'Vivo', '2.0': 'Fallecido', '3.0': 'Fallecido',
                }},
            }), encoding='utf-8')
        for name, value in [('ROOT', self.root), ('OUT', self.out), ('PROV', self.prov)]:
            patcher = mock.patch.object(audit, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def run_audit(self, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            audit.main(**kwargs)

    def test_default_builds_without_thesis_files_and_preserves_historical_reports(self):
        historical = self.prov/'annual_reconciliation.csv'
        historical.write_bytes(b'historical comparison\n')
        with mock.patch('freeze_inputs.verify', side_effect=AssertionError('Thesis verification called')):
            self.run_audit()
        cohort = pd.read_csv(self.out/'admissions_c71_audited.csv')
        self.assertEqual(len(cohort), 10)
        self.assertEqual(int(cohort.death.sum()), 1)
        self.assertTrue(cohort.admission_id.is_unique)
        self.assertEqual(cohort.source_year.tolist(), list(range(2015, 2025)))
        annual = pd.read_csv(self.prov/'annual_counts.csv')
        self.assertEqual(int(annual.admissions.sum()), 10)
        self.assertNotIn('legacy_admissions', annual.columns)
        summary = json.loads((self.prov/'audit_summary.json').read_text())
        self.assertEqual(summary['legacy_comparison_status'], 'not_run')
        self.assertIsNone(summary['legacy_misclassified_anatomy'])
        self.assertIsNone(summary['legacy_projected_duplicates_beyond_first'])
        self.assertEqual(historical.read_bytes(), b'historical comparison\n')
        self.assertFalse((self.root/'Data_base').exists())
        self.assertFalse((self.prov/'workbook_reconciliation.json').exists())

    def test_changed_official_archive_still_blocks_generation(self):
        (self.root/'data/raw/source.zip').write_bytes(b'changed')
        with self.assertRaises(AssertionError):
            self.run_audit()
        self.assertFalse((self.out/'admissions_c71_audited.csv').exists())

    def test_changed_annual_extract_still_blocks_generation(self):
        path = self.out/'inec_c71/2020.csv'
        path.write_bytes(path.read_bytes()+b'\n')
        with self.assertRaises(AssertionError):
            self.run_audit()
        self.assertFalse((self.out/'admissions_c71_audited.csv').exists())

    def test_requested_legacy_comparison_requires_verified_baseline(self):
        with mock.patch('freeze_inputs.verify', side_effect=SystemExit('Missing/changed inputs')) as verify:
            with self.assertRaisesRegex(SystemExit, 'Missing/changed inputs'):
                self.run_audit(compare_legacy=True)
        verify.assert_called_once_with()
        self.assertFalse((self.out/'admissions_c71_audited.csv').exists())

    def test_requested_legacy_comparison_writes_reconciliation_and_metrics(self):
        legacy = pd.DataFrame({
            'cau_cie10': ['C714']*10,
            'CIE10': ['No Especificado / Otros']*10,
            'A\u00f1o': list(range(2015, 2025)),
            'con_egrpa': ['Vivo']*9+['Fallecido'],
        })
        metadata = SimpleNamespace(column_names=list(legacy))
        folder = self.root/'Data_base'
        folder.mkdir()
        (folder/'example.xlsx').touch()
        with mock.patch('freeze_inputs.verify') as verify, \
             mock.patch('pyreadstat.read_sav', return_value=(legacy.copy(), metadata)), \
             mock.patch.object(pd, 'read_excel', return_value=legacy.copy()):
            self.run_audit(compare_legacy=True)
        verify.assert_called_once_with()
        annual = pd.read_csv(self.prov/'annual_reconciliation.csv')
        self.assertEqual(annual.admissions_difference.tolist(), [0]*10)
        self.assertEqual(annual.deaths_difference.tolist(), [0]*10)
        summary = json.loads((self.prov/'audit_summary.json').read_text())
        self.assertEqual(summary['legacy_comparison_status'], 'completed')
        self.assertEqual(summary['legacy_misclassified_anatomy'], 10)
        self.assertEqual(summary['legacy_projected_duplicates_beyond_first'], 0)
        book = json.loads((self.prov/'workbook_reconciliation.json').read_text())
        self.assertTrue(book[0]['same_order_and_values_as_sav_after_numeric_format_normalization'])


if __name__ == '__main__':
    unittest.main()
