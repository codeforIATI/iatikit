from os.path import abspath, dirname, join
from unittest import TestCase

import pytest

from pyandi import Sector
from pyandi.standard.codelist import Codelist
from pyandi.utils.exceptions import UnknownSectorVocabError, \
                                    UnknownSectorCodeError


class TestSector(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSector, self).__init__(*args, **kwargs)
        self.codelist_path = join(dirname(abspath(__file__)),
                                  'fixtures', 'codelists')

    def test_sector_repr(self):
        sector = Sector(12345, path=self.codelist_path)
        assert str(sector) == '<Sector (12345, Vocabulary: Unspecified)>'

        sector = Sector(151, vocabulary=2, path=self.codelist_path)
        sector_repr = '<Sector (Government and civil society, general ' + \
                      '(151), Vocabulary: OECD DAC CRS Purpose Codes ' + \
                      '(3 digit))>'
        assert str(sector) == sector_repr

        sector = Sector('ABCD', vocabulary=3, path=self.codelist_path)
        sector_repr = '<Sector (ABCD, Vocabulary: Classification of the ' + \
                      'Functions of Government (UN))>'
        assert str(sector) == sector_repr

    def test_sector_percentage(self):
        sector = Sector(12345, path=self.codelist_path, percentage=100)
        assert type(sector.percentage) is float
        assert sector.percentage == 100.0

    def test_sector_unknown_vocab(self):
        with pytest.raises(UnknownSectorVocabError):
            Sector(12345, path=self.codelist_path, vocabulary=10)

    def test_sector_unknown_code(self):
        with pytest.raises(UnknownSectorCodeError):
            Sector(12345, path=self.codelist_path, vocabulary=1)

    def test_sector_from_codelist_item(self):
        codelist = Codelist('Sector', self.codelist_path, '2.03')
        codelist_item = codelist.get('73010')
        sector = Sector(codelist_item, path=self.codelist_path)
        assert sector.code.code == '73010'
