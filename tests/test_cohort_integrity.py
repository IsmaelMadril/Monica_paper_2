"""Controls for the audited 23 October 2026 source releases (run extraction first)."""
import unittest
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
COHORT=ROOT/'data/processed/admissions_c71_audited.csv'

@unittest.skipUnless(COHORT.exists(),'Run extraction and audit first')
class CohortIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.c=pd.read_csv(COHORT)
    def test_source_flow_and_totals(self):
        c=self.c
        self.assertEqual(len(c),10972)
        self.assertEqual(int(c.death.sum()),963)
        f=pd.read_csv(ROOT/'provenance/t02/selection_flow.csv')
        self.assertEqual(c.groupby('source_year').size().tolist(),f.eligible_c710_c719.tolist())
        self.assertTrue(c.admission_id.is_unique)
    def test_outcomes_and_anatomical_corrections(self):
        c=self.c
        self.assertTrue(c.loc[c.con_egrpa.eq(1),'death'].eq(0).all())
        self.assertTrue(c.loc[c.con_egrpa.isin([2,3]),'death'].eq(1).all())
        self.assertTrue(c.loc[c.icd10.eq('C714'),'anatomy'].eq('Supratentorial').all())
        self.assertTrue(c.loc[c.icd10.eq('C717'),'anatomy'].eq('Infratentorial/midline').all())
    def test_unknown_and_provisional_values_are_exposed(self):
        c=self.c
        self.assertEqual(int(c.ethnicity_unknown.sum()),1290)
        self.assertEqual(int(c.residence_foreign.sum()),3)
        self.assertTrue(c.residence_area_mapping_verified.eq(c.source_year.ge(2018)).all())
        self.assertTrue(c.loc[c.dia_estad.eq(30),'los_group'].eq('15-30').all())
