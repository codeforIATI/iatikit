import json
from os.path import abspath, dirname, join
import re
import shutil
import tempfile
from unittest import TestCase

from mock import patch

from pyandi.utils import download
from pyandi.utils.config import CONFIG


class MockRequest():
    def __init__(self, url):
        codelist_path = join(dirname(abspath(__file__)),
                             'fixtures', 'codelist_downloads')

        match = re.search(r'(\d{3}).*?/([^\.\/]+)\.(csv|json)', url)
        if match:
            version, name, extension = match.groups()
            fname = '{name}-v{version}.{extension}'.format(
                name=name,
                version=version,
                extension=extension)
        else:
            raise NotImplementedError()
        self.filepath = join(codelist_path, fname)

    def json(self):
        with open(self.filepath) as handler:
            return json.load(handler)

    def iter_lines(self):
        with open(self.filepath, 'rb') as handler:
            return handler.readlines()


class TestDownloadCodelists(TestCase):
    def setUp(self):
        self.standard_path = tempfile.mkdtemp(dir=dirname(abspath(__file__)))
        config_dict = {'paths': {'standard': self.standard_path}}
        CONFIG.read_dict(config_dict)

    @patch('requests.get', MockRequest)
    def test_download_data(self):
        download.codelists()

        codelists_expected = {
            "ActivityStatus": ["2.01", "1.05", "1.04", "1.03", "1.02", "1.01"],
            "Sector": ["2.01", "1.05", "1.04", "1.03", "1.02", "1.01"],
            "SectorVocabulary": ["2.01"],
            "Vocabulary": ["1.05", "1.04", "1.03", "1.02", "1.01"],
        }

        path = join(self.standard_path, 'codelists', 'codelists.json')
        with open(path) as handler:
            codelists = json.load(handler)
        assert codelists == codelists_expected

        path = join(self.standard_path, 'codelists', 'ActivityStatus.json')
        with open(path) as handler:
            vocabs = json.load(handler)
        assert len(vocabs['data']) == 6
        assert vocabs['data']['6']['from'] == '1.05'
        assert vocabs['data']['6']['until'] == '2.01'
        assert vocabs['data']['1']['from'] == '1.01'
        assert vocabs['data']['1']['until'] == '2.01'

        path = join(self.standard_path, 'codelists', 'Sector.json')
        with open(path) as handler:
            vocabs = json.load(handler)
        assert len(vocabs['data']) == 2
        sector_name = 'Media and free flow of information'
        assert vocabs['data']['15153']['name'] == sector_name

        path = join(self.standard_path, 'codelists', 'SectorVocabulary.json')
        with open(path) as handler:
            vocabs = json.load(handler)
        assert len(vocabs['data']) == 1
        vocab_name = 'OECD DAC CRS Purpose Codes (5 digit)'
        assert vocabs['data']['1']['name'] == vocab_name

        path = join(self.standard_path, 'codelists', 'Vocabulary.json')
        with open(path) as handler:
            vocabs = json.load(handler)
        assert len(vocabs['data']) == 1
        vocab_name = 'OECD Development Assistance Committee'
        assert vocabs['data']['DAC']['name'] == vocab_name
        assert vocabs['data']['DAC']['from'] == '1.01'
        assert vocabs['data']['DAC']['until'] == '1.05'

    def tearDown(self):
        shutil.rmtree(self.standard_path, ignore_errors=True)
