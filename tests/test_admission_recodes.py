"""Scientific boundary checks for the T02 cohort recodes."""
import sys
from pathlib import Path
import unittest
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_admissions import anatomy, age_group, los_group

class Recodes(unittest.TestCase):
    def test_anatomy_previously_misclassified(self):
        self.assertEqual(anatomy('C714'),'Supratentorial')
        self.assertEqual(anatomy('C717'),'Infratentorial/midline')
        self.assertTrue(pd.isna(anatomy('C7100')))
    def test_age_boundaries_and_units(self):
        for age,expected in [(17,'0-17'),(18,'18-44'),(44,'18-44'),(45,'45-64'),(64,'45-64'),(65,'65-79'),(79,'65-79'),(80,'80+')]:
            self.assertEqual(age_group(age,4),expected)
        for unit,value in [(1,23),(2,28),(3,11)]:
            self.assertEqual(age_group(value,unit),'0-17')
        for age,unit in [(9,9),(116,4),(-1,4),(12,3),(None,4),(30.5,4)]:
            self.assertTrue(pd.isna(age_group(age,unit)))
    def test_stay_day_30_is_not_in_final_group(self):
        for value,expected in [(0,'0 days'),(1,'1-3'),(3,'1-3'),(4,'4-14'),(14,'4-14'),(15,'15-30'),(30,'15-30'),(31,'31+')]:
            self.assertEqual(los_group(value),expected)
        for value in [-1,1.5,None]:self.assertTrue(pd.isna(los_group(value)))

if __name__=='__main__':unittest.main()
