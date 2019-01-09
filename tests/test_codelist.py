from os.path import abspath, dirname, join
import shutil
import tempfile
from unittest import TestCase

import pytest

import pyandi
from pyandi.standard.codelist import CodelistSet, Codelist
from pyandi.utils.exceptions import NoCodelistsError


class TestNoCodelists(TestCase):
    def setUp(self):
        self.empty_path = tempfile.mkdtemp(dir=dirname(abspath(__file__)))

    def test_no_codelists(self):
        with pytest.raises(NoCodelistsError):
            CodelistSet(path=self.empty_path)

    def tearDown(self):
        shutil.rmtree(self.empty_path, ignore_errors=True)


class TestCodelistSet(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCodelistSet, self).__init__(*args, **kwargs)
        self.codelist_path = join(dirname(abspath(__file__)),
                                  'fixtures', 'standard', 'codelists')
        self.codelists = CodelistSet(self.codelist_path)

    def test_codelists_iter(self):
        codelist_slugs = [
            'Sector',
            'SectorCategory',
            'SectorVocabulary',
            'Vocabulary',
        ]
        assert len([x for x in self.codelists]) == 4
        for x in self.codelists:
            assert x.slug in codelist_slugs

    def test_codelists_shortcut(self):
        codelists = pyandi.codelists(self.codelist_path)
        assert(len(codelists)) == 4

    def test_codelists_filter_version(self):
        codelist_slugs = [
            'Sector',
            'SectorCategory',
            'Vocabulary',
        ]
        codelists = [x for x in self.codelists.where(version='1.01')]
        assert len(codelists) == 3
        for x in codelists:
            assert x.slug in codelist_slugs

    def test_codelists_filter_slug(self):
        sector_codelist = self.codelists.find(slug='Sector')
        assert sector_codelist.slug == 'Sector'


class TestCodelist(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCodelist, self).__init__(*args, **kwargs)
        codelist_path = join(dirname(abspath(__file__)),
                             'fixtures', 'standard', 'codelists')
        self.codelist = Codelist('Sector', codelist_path, '1.05')

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
        for x in codelist_items:
            assert x.name in codelist_item_names

    def test_codelist_item(self):
        codelist_item = self.codelist.get('73010')
        item_repr = '<CodelistItem (Reconstruction relief and ' + \
                    'rehabilitation (73010))>'
        assert str(codelist_item) == item_repr
