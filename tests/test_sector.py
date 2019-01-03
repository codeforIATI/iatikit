from os.path import abspath, dirname, join
from unittest import TestCase

from pyandi import Sector


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
