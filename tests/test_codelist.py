from os.path import abspath, dirname, join
import shutil
import tempfile
from unittest import TestCase

import pytest

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
        codelist_path = join(dirname(abspath(__file__)),
                             'fixtures', 'codelists')
        self.codelists = CodelistSet(codelist_path)

    def test_codelists_iter(self):
        codelist_slugs = [
            'Sector',
            'SectorVocabulary',
            'Vocabulary',
        ]
        assert len([x for x in self.codelists]) == 3
        for x in self.codelists:
            assert x.slug in codelist_slugs

    def test_codelists_filter_version(self):
        codelist_slugs = [
            'Sector',
            'Vocabulary',
        ]
        codelists = [x for x in self.codelists.where(version='1.01')]
        assert len(codelists) == 2
        for x in codelists:
            assert x.slug in codelist_slugs

    def test_codelists_filter_slug(self):
        sector_codelist = self.codelists.find(slug='Sector')
        assert sector_codelist.slug == 'Sector'


class TestCodelist(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCodelist, self).__init__(*args, **kwargs)
        codelist_path = join(dirname(abspath(__file__)),
                             'fixtures', 'codelists')
        self.codelist = Codelist('Sector', codelist_path, '1.05')

    def test_metadata(self):
        metadata = {
            'category-codelist': 'SectorCategory',
            'name': 'Sector',
            'complete': '1',
            'url': 'http://www.oecd.org/dac/stats/dacandcrscodelists.htm',
            'name': 'DAC 5 Digit Sector',
            'description': 'Sector codelist description',
        }
        assert self.codelist.metadata == metadata
