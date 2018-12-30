from os.path import abspath, dirname, join
from unittest import TestCase

from freezegun import freeze_time
import pytest

from pyandi.data.registry import Registry


class TestGenericSet(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestGenericSet, self).__init__(*args, **kwargs)
        self.registry_path = join(dirname(abspath(__file__)),
                                  'fixtures', 'registry')

    @freeze_time("2015-12-02")
    def setUp(self):
        self.registry = Registry(self.registry_path)

    def test_set_get(self):
        org_dataset = self.registry.datasets.get('fixture-org-org')
        assert org_dataset.name == 'fixture-org-org'

    def test_set_get_unknown(self):
        unknown_dataset = self.registry.datasets.get('unknown')
        assert unknown_dataset is None

    def test_set_find(self):
        org_dataset = self.registry.datasets.find(name='fixture-org-org')
        assert org_dataset.name == 'fixture-org-org'

    def test_set_not_found(self):
        with pytest.raises(IndexError):
            self.registry.datasets.find(name='not-a-dataset')

    def test_set_count(self):
        assert self.registry.datasets.count() == 3
