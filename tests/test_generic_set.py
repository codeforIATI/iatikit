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

    def test_set_first(self):
        first_dataset = self.registry.datasets.first()
        zero_index_dataset = self.registry.datasets[0]
        assert first_dataset.name == zero_index_dataset.name

    def test_set_count(self):
        datasets = self.registry.datasets
        assert datasets.count() == 3

    def test_set_all(self):
        dataset_names = [
            'fixture-org-activities',
            'fixture-org-org',
            'old-org-acts',
        ]
        datasets = self.registry.datasets.all()
        assert type(datasets) is list
        assert len(datasets) == 3
        for x in datasets:
            assert x.name in dataset_names

    def test_set_filter_chaining(self):
        act_datasets = self.registry.datasets.filter(filetype='activity')
        no_datasets = act_datasets.filter(name='fixture-org-org')
        assert no_datasets.count() == 0

        org_datasets = self.registry.datasets.filter(filetype='organisation')
        org_dataset = org_datasets.filter(name='fixture-org-org')
        assert org_dataset.count() == 1

    def test_set_where_chaining(self):
        act_datasets = self.registry.datasets.where(filetype='activity')
        no_datasets = act_datasets.where(name='fixture-org-org')
        assert no_datasets.count() == 0

        org_datasets = self.registry.datasets.where(filetype='organisation')
        org_dataset = org_datasets.where(name='fixture-org-org')
        assert org_dataset.count() == 1
