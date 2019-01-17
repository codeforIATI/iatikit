from os.path import abspath, dirname, join
import shutil
import tempfile
from unittest import TestCase

import pytest

import iatikit
from iatikit.standard.codelist import CodelistSet, Codelist
from iatikit.utils.exceptions import NoCodelistsError
from iatikit.utils.config import CONFIG


class TestNoCodelists(TestCase):
    def setUp(self):
        self.empty_path = tempfile.mkdtemp(dir=dirname(abspath(__file__)))
        config_dict = {'paths': {'standard': self.empty_path}}
        CONFIG.read_dict(config_dict)

    def test_no_codelists(self):
        with pytest.raises(NoCodelistsError):
            CodelistSet()

    def tearDown(self):
        shutil.rmtree(self.empty_path, ignore_errors=True)


class TestCodelistSet(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCodelistSet, self).__init__(*args, **kwargs)
        standard_path = join(dirname(abspath(__file__)),
                             'fixtures', 'standard')
        config_dict = {'paths': {'standard': standard_path}}
        CONFIG.read_dict(config_dict)
        self.codelists = CodelistSet()

    def test_codelists_iter(self):
        codelist_slugs = [
            'ActivityStatus',
            'Sector',
            'SectorCategory',
            'SectorVocabulary',
            'Vocabulary',
        ]
        assert len([x for x in self.codelists]) == 5
        for codelist in self.codelists:
            assert codelist.slug in codelist_slugs

    def test_codelists_shortcut(self):
        codelists = iatikit.codelists()
        assert(len(codelists)) == 5

    def test_codelists_filter_version(self):
        codelist_slugs = [
            'Sector',
            'SectorCategory',
            'Vocabulary',
        ]
        codelists = [x for x in self.codelists.where(version='1.01')]
        assert len(codelists) == 3
        for codelist in codelists:
            assert codelist.slug in codelist_slugs

    def test_codelists_filter_slug(self):
        sector_codelist = self.codelists.find(slug='Sector')
        assert sector_codelist.slug == 'Sector'


class TestCodelist(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCodelist, self).__init__(*args, **kwargs)
        standard_path = join(dirname(abspath(__file__)),
                             'fixtures', 'standard')
        config_dict = {'paths': {'standard': standard_path}}
        CONFIG.read_dict(config_dict)
        self.codelist = Codelist('Sector', '1.05')

    def test_codelist_name(self):
        assert self.codelist.name == 'DAC 5 Digit Sector'

    def test_codelist_description(self):
        description = 'Sector codelist description'
        assert self.codelist.description == description

    def test_codelist_url(self):
        url = 'http://www.oecd.org/dac/stats/dacandcrscodelists.htm'
        assert self.codelist.url == url

    def test_codelist_complete(self):
        assert self.codelist.complete is True

    def test_codelist_iter(self):
        items = [x for x in self.codelist]
        assert len(items) == 3

    def test_codelist_repr(self):
        assert str(self.codelist) == '<Codelist (Sector v1.05)>'

    def test_codelist_filter_category(self):
        codelist_item_names = [
            'Media and free flow of information',
            'Free flow of information',
        ]
        codelist_items = [x for x in self.codelist.filter(category='151')]
        assert len(codelist_items) == 2
        for codelist_item in codelist_items:
            assert codelist_item.name in codelist_item_names

    def test_codelist_item(self):
        codelist_item = self.codelist.get('73010')
        item_repr = '<CodelistItem (Reconstruction relief and ' + \
                    'rehabilitation (73010))>'
        assert str(codelist_item) == item_repr
