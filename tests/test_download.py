from filecmp import dircmp
from io import BytesIO
import os
from os.path import abspath, dirname, join
import shutil
import sys
import tempfile
from unittest import TestCase
import zipfile

from mock import patch
from six import StringIO

from pyandi.utils import download


class MockRequest():
    def __init__(self, url, stream=False):
        registry_path = join(dirname(abspath(__file__)),
                             'fixtures', 'registry')
        if url.endswith('iati_dump.zip?dl=1'):
            self.raw = BytesIO()
            with zipfile.ZipFile(self.raw, 'w') as ziph:
                for path in ['data', 'metadata']:
                    for root, _, files in os.walk(join(registry_path, path)):
                        for file in files:
                            fullpath = join(root, file)
                            ziph.write(fullpath, fullpath[len(registry_path):])
            self.raw.seek(0)
        elif url.endswith('metadata.json?dl=1'):
            metadata_path = join(registry_path, 'metadata.json')
            with open(metadata_path, 'rb') as source:
                self.content = source.read()


class TestDownloadData(TestCase):
    def setUp(self):
        self.data_path = tempfile.mkdtemp(dir=dirname(abspath(__file__)))

    def compare(self, first, second):
        comp = dircmp(first, second)
        _stdout = sys.stdout
        _stringio = StringIO()
        sys.stdout = _stringio
        comp.report_full_closure()
        sys.stdout = _stdout
        _stringio.seek(0)
        report = _stringio.read()
        del _stringio
        return report

    @patch('requests.get', MockRequest)
    def test_download_data(self):
        registry_path = join(dirname(abspath(__file__)),
                             'fixtures', 'registry')
        download.data(self.data_path)
        report = self.compare(registry_path, self.data_path)

        assert 'Only in' not in report
        assert 'Differing files' not in report

    def tearDown(self):
        shutil.rmtree(self.data_path, ignore_errors=True)
