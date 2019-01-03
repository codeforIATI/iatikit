from os.path import abspath, dirname, join
import shutil
import tempfile
from unittest import TestCase

import pytest

from pyandi.standard.codelist import CodelistSet
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
