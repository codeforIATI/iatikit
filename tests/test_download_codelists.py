import json
from os.path import abspath, dirname, join
import re
import shutil
import tempfile
from unittest import TestCase

from mock import patch

from pyandi.utils import download


class MockRequest():
    def __init__(self, url):
        codelist_path = join(dirname(abspath(__file__)),
                             'fixtures', 'codelist_downloads')
        fname = url.rsplit('/', 1)[-1]
        if fname in ['Version.json', 'Vocabulary.json', 'Sector.json',
                     'SectorVocabulary.json', 'Vocabulary.csv']:
            pass
        elif re.search(r'codelists?\.(csv|json)$', url):
            if 'codelists102' in url:
                fname = 'codelists-v102.csv'
            elif 'codelists103' in url:
                fname = 'codelists-v103.json'
            elif 'iatistandard.org/1' in url:
                fname = 'codelists-v104.json'
            elif 'iatistandard.org/2' in url:
                fname = 'codelists-v2.json'
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
        self.codelist_path = tempfile.mkdtemp(dir=dirname(abspath(__file__)))

    @patch('requests.get', MockRequest)
    def test_download_data(self):
        download.codelists(self.codelist_path)

        codelists_expected = {
            "Sector": ["2.01", "1.05", "1.04", "1.03", "1.02", "1.01"],
            "SectorVocabulary": ["2.01"],
            "Vocabulary": ["1.05", "1.04", "1.03", "1.02", "1.01"],
        }
        with open(join(self.codelist_path, 'codelists.json')) as handler:
            codelists = json.load(handler)
        assert codelists == codelists_expected

        with open(join(self.codelist_path, 'Sector.json')) as handler:
            vocabs = json.load(handler)
        assert len(vocabs['data']) == 2
        sector_name = 'Media and free flow of information'
        assert vocabs['data']['15153']['name'] == sector_name

        with open(join(self.codelist_path, 'SectorVocabulary.json')) \
                as handler:
            vocabs = json.load(handler)
        assert len(vocabs['data']) == 1
        vocab_name = 'OECD DAC CRS Purpose Codes (5 digit)'
        assert vocabs['data']['1']['name'] == vocab_name

        with open(join(self.codelist_path, 'Vocabulary.json')) as handler:
            vocabs = json.load(handler)
        assert len(vocabs['data']) == 1
        vocab_name = 'OECD Development Assistance Committee'
        assert vocabs['data']['DAC']['name'] == vocab_name
        assert vocabs['data']['DAC']['from'] == '1.01'
        assert vocabs['data']['DAC']['until'] == '1.05'

    def tearDown(self):
        shutil.rmtree(self.codelist_path, ignore_errors=True)
