"""Input restoration must preserve expected hashes and refuse replacements."""
import csv
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock

spec = importlib.util.spec_from_file_location('restore_analysis_inputs', Path(__file__).resolve().parents[1]/'scripts/restore_analysis_inputs.py')
restore = importlib.util.module_from_spec(spec)
spec.loader.exec_module(restore)

class RestoreInputs(unittest.TestCase):
    def test_existing_input_verified_and_mismatch_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root/'data/raw/example.zip'
            target.parent.mkdir(parents=True)
            target.write_bytes(b'original')
            row = {'path':'data/raw/example.zip', 'sha256':hashlib.sha256(b'original').hexdigest()}
            self.assertEqual(restore.ensure_file(root,row),'verified')
            row['sha256'] = hashlib.sha256(b'other').hexdigest()
            with self.assertRaisesRegex(ValueError,'CHECKSUM MISMATCH'):
                restore.ensure_file(root,row,download=True)
            self.assertEqual(target.read_bytes(),b'original')
    def test_missing_check_does_not_create_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.assertEqual(restore.ensure_file(root,{'path':'data/raw/absent.zip'}),'missing')
            self.assertFalse((root/'data/raw').exists())
    def test_download_accepted_only_after_hash_verification(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            row = {'path':'data/raw/example.zip','url':'https://example.invalid/archive','sha256':hashlib.sha256(b'bytes').hexdigest()}
            with mock.patch('requests.get') as get:
                response = get.return_value.__enter__.return_value
                response.iter_content.return_value = [b'by',b'tes']
                self.assertEqual(restore.ensure_file(root,row,download=True),'downloaded and verified')
            self.assertEqual((root/row['path']).read_bytes(),b'bytes')
            self.assertEqual(list((root/'data/raw').glob('*.part')),[])
    def test_bad_download_is_not_installed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            row = {'path':'data/raw/example.zip','url':'https://example.invalid/archive','sha256':hashlib.sha256(b'expected').hexdigest()}
            with mock.patch('requests.get') as get:
                get.return_value.__enter__.return_value.iter_content.return_value = [b'wrong']
                with self.assertRaisesRegex(ValueError,'DOWNLOAD CHECKSUM MISMATCH'):
                    restore.ensure_file(root,row,download=True)
            self.assertFalse((root/row['path']).exists())
            self.assertEqual(list((root/'data/raw').glob('*.part')),[])
    def test_manifest_path_cannot_escape_raw_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            p = root/'manifest.csv'
            with p.open('w',newline='',encoding='utf-8') as stream:
                writer=csv.DictWriter(stream,fieldnames=['path','sha256'],lineterminator='\n')
                writer.writeheader();writer.writerow({'path':'../outside.zip','sha256':'abc'})
            with self.assertRaisesRegex(ValueError,'outside data/raw'):
                restore.read_entries(root,['manifest.csv'])

if __name__=='__main__':unittest.main()
