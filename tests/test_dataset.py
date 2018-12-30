from os.path import abspath, dirname, join
from unittest import TestCase

import pytest

from pyandi.data.publisher import DatasetSet


class TestDatasets(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDatasets, self).__init__(*args, **kwargs)
        self.registry_path = join(dirname(abspath(__file__)),
                                  'fixtures', 'registry')

    def setUp(self):
        self.org_datasets = DatasetSet(
            join(self.registry_path, 'data', 'fixture-org', '*'),
            join(self.registry_path, 'metadata', 'fixture-org', '*'),
        )

    def test_datasets_iter(self):
        dataset_list = list(self.org_datasets)
        assert len(dataset_list) == 2

    def test_datasets_filter_by_filetype(self):
        act_datasets = self.org_datasets.where(filetype='activity').all()
        assert len(act_datasets) == 1
        assert act_datasets[0].name == 'fixture-org-activities'

    def test_datasets_filter_by_name(self):
        org_datasets = self.org_datasets.where(name='fixture-org-org').all()
        assert len(org_datasets) == 1
        assert org_datasets[0].name == 'fixture-org-org'

    def test_datasets_get(self):
        org_dataset = self.org_datasets.get('fixture-org-org')
        assert org_dataset.name == 'fixture-org-org'

    def test_datasets_get_unknown(self):
        unknown_dataset = self.org_datasets.get('unknown')
        assert unknown_dataset is None

    def test_datasets_find(self):
        org_dataset = self.org_datasets.find(name='fixture-org-org')
        assert org_dataset.name == 'fixture-org-org'

    def test_datasets_not_found(self):
        with pytest.raises(IndexError):
            self.org_datasets.find(name='not-a-dataset')

    def test_datasets_count(self):
        assert self.org_datasets.count() == 2
