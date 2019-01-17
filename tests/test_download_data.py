from io import BytesIO
import os
from os.path import abspath, dirname, join
import shutil
import tempfile
from unittest import TestCase
import zipfile

from mock import patch

from iatikit.utils import download
from iatikit.utils.config import CONFIG


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
        config_dict = {'paths': {'registry': self.data_path}}
        CONFIG.read_dict(config_dict)

    @patch('requests.get', MockRequest)
    def test_download_data(self):
        def list_files(path):
            all_files = []
            for root, _, files in os.walk(path):
                for file in files:
                    all_files.append(join(root, file)[len(path):])
            return all_files

        download.data()

        registry_path = join(dirname(abspath(__file__)),
                             'fixtures', 'registry')
        source_files = list_files(registry_path)
        dest_files = list_files(self.data_path)

        assert len(source_files) == len(dest_files)
        for dest_file in dest_files:
            assert dest_file in source_files

    def tearDown(self):
        shutil.rmtree(self.data_path, ignore_errors=True)
