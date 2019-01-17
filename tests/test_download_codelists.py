import json
from os.path import abspath, dirname, join
import shutil
import tempfile
from unittest import TestCase

from mock import patch

from iatikit.utils import download
from iatikit.utils.config import CONFIG
from .helpers import CodelistMockRequest


class TestDownloadCodelists(TestCase):
    def setUp(self):
        self.standard_path = tempfile.mkdtemp(dir=dirname(abspath(__file__)))
        config_dict = {'paths': {'standard': self.standard_path}}
        CONFIG.read_dict(config_dict)

    @patch('requests.get', CodelistMockRequest)
    def test_download_codelists(self):
        download.codelists()

        codelists_expected = {
            "ActivityStatus": ["2.01", "1.05", "1.04", "1.03", "1.02", "1.01"],
            "Sector": ["2.01", "1.05", "1.04", "1.03", "1.02", "1.01"],
            "SectorVocabulary": ["2.01"],
            "Vocabulary": ["1.05", "1.04", "1.03", "1.02", "1.01"],
            "Version": ["2.01", "1.05", "1.04", "1.03", "1.02", "1.01"],
        }

        path = join(self.standard_path, 'codelists', 'codelists.json')
        with open(path) as handler:
            codelists = json.load(handler)
        assert codelists == codelists_expected

    @patch('requests.get', CodelistMockRequest)
    def test_download_codelist_from_until(self):
        download.codelists()

        path = join(self.standard_path, 'codelists', 'ActivityStatus.json')
        with open(path) as handler:
            vocabs = json.load(handler)
        assert len(vocabs['data']) == 6
        assert vocabs['data']['6']['from'] == '1.05'
        assert vocabs['data']['6']['until'] == '2.01'
        assert vocabs['data']['1']['from'] == '1.01'
        assert vocabs['data']['1']['until'] == '2.01'

    @patch('requests.get', CodelistMockRequest)
    def test_download_codelist_items(self):
        download.codelists()

        path = join(self.standard_path, 'codelists', 'Sector.json')
        with open(path) as handler:
            vocabs = json.load(handler)
        assert len(vocabs['data']) == 2
        sector_name = 'Media and free flow of information'
        assert vocabs['data']['15153']['name'] == sector_name

    @patch('requests.get', CodelistMockRequest)
    def test_download_codelist_mappings(self):
        download.codelists()

        path = join(self.standard_path, 'codelist_mappings')
        with open(join(path, '201', 'activity-mappings.json')) as handler:
            mappings = json.load(handler)
        assert len(mappings) == 6

        with open(join(path, '201', 'organisation-mappings.json')) as handler:
            mappings = json.load(handler)
        assert len(mappings) == 1

        with open(join(path, '105', 'activity-mappings.json')) as handler:
            mappings = json.load(handler)
        assert len(mappings) == 4

        with open(join(path, '105', 'organisation-mappings.json')) as handler:
            mappings = json.load(handler)
        assert mappings == []

    def tearDown(self):
        shutil.rmtree(self.standard_path, ignore_errors=True)
