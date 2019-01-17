from os.path import abspath, dirname, join
from unittest import TestCase

import pytest

from iatikit import Sector
from iatikit.standard.codelist import Codelist
from iatikit.utils.exceptions import UnknownSectorVocabError, \
                                    UnknownSectorCodeError, \
                                    InvalidSectorCodeError
from iatikit.utils.config import CONFIG


class TestSector(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSector, self).__init__(*args, **kwargs)
        standard_path = join(dirname(abspath(__file__)),
                             'fixtures', 'standard')
        config_dict = {'paths': {'standard': standard_path}}
        CONFIG.read_dict(config_dict)

    def test_sector_repr(self):
        sector = Sector(12345)
        assert str(sector) == '<Sector (12345, Vocabulary: Unspecified)>'

        sector = Sector(151, vocabulary=2)
        sector_repr = '<Sector (Government and civil society, general ' + \
                      '(151), Vocabulary: OECD DAC CRS Purpose Codes ' + \
                      '(3 digit))>'
        assert str(sector) == sector_repr

        sector = Sector('ABCD', vocabulary=3)
        sector_repr = '<Sector (ABCD, Vocabulary: Classification of the ' + \
                      'Functions of Government (UN))>'
        assert str(sector) == sector_repr

    def test_sector_percentage(self):
        sector = Sector(12345, percentage=100)
        assert isinstance(sector.percentage, float)
        assert sector.percentage == 100.0

    def test_sector_unknown_vocab(self):
        with pytest.raises(UnknownSectorVocabError):
            Sector(12345, vocabulary=10)

    def test_sector_unknown_code(self):
        with pytest.raises(UnknownSectorCodeError):
            Sector(12345, vocabulary=1)

    def test_sector_from_dac_5_codelist_item(self):
        codelist = Codelist('Sector', '2.03')
        codelist_item = codelist.get('73010')
        sector = Sector(codelist_item)
        assert sector.code.code == '73010'

    def test_sector_from_dac_3_codelist_item(self):
        codelist = Codelist('SectorCategory', '2.03')
        codelist_item = codelist.get('151')
        sector = Sector(codelist_item)
        assert sector.code.code == '151'

    def test_sector_from_bad_codelist_item(self):
        codelist = Codelist('Vocabulary', '1.05')
        codelist_item = codelist.get('DAC')
        with pytest.raises(InvalidSectorCodeError):
            Sector(codelist_item)
