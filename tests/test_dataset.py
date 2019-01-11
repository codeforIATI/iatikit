from os.path import abspath, dirname, join
from unittest import TestCase

from mock import patch
import pytest

from pyandi.data.dataset import DatasetSet, Dataset
from pyandi.utils.exceptions import MappingsNotFoundError
from pyandi.utils.config import CONFIG


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
        assert len(dataset_list) == 3

    def test_datasets_filter_by_filetype(self):
        act_datasets = self.org_datasets.where(filetype='activity').all()
        assert len(act_datasets) == 2
        assert act_datasets[0].name == 'fixture-org-activities'

    def test_datasets_filter_by_name(self):
        org_datasets = self.org_datasets.where(name='fixture-org-org').all()
        assert len(org_datasets) == 1
        assert org_datasets[0].name == 'fixture-org-org'


class TestDataset(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDataset, self).__init__(*args, **kwargs)
        registry_path = join(dirname(abspath(__file__)),
                             'fixtures', 'registry')
        self.activity_dataset = Dataset(
            join(registry_path, 'data',
                 'old-org', 'old-org-acts.xml'),
            join(registry_path, 'metadata',
                 'old-org', 'old-org-acts.json'),
        )

        standard_path = join(dirname(abspath(__file__)),
                             'fixtures', 'standard')
        config_dict = {'paths': {'standard': standard_path}}
        CONFIG.read_dict(config_dict)

    def test_dataset_name(self):
        assert self.activity_dataset.name == 'old-org-acts'

    def test_dataset_version(self):
        assert self.activity_dataset.version == '1.03'

    def test_dataset_repr(self):
        dataset_repr = '<Dataset (old-org-acts)>'
        assert str(self.activity_dataset) == dataset_repr

    def test_dataset_validate_xml(self):
        assert bool(self.activity_dataset.validate_xml()) is True

    def test_dataset_validate_iati(self):
        assert bool(self.activity_dataset.validate_iati()) is True

    @patch('logging.Logger.warning')
    def test_dataset_validate_codelists_old(self, fake_logger_warning):
        assert bool(self.activity_dataset.validate_codelists()) is True
        msg = ('Can\'t perform codelist validation for ' +
               'IATI version %s datasets.', '1.03')
        fake_logger_warning.assert_called_once_with(*msg)

    def test_dataset_validate_unique_ids(self):
        assert bool(self.activity_dataset.validate_unique_ids()) is True

    def test_dataset_root(self):
        assert self.activity_dataset.root == 'iati-activities'

    @patch('webbrowser.open_new_tab')
    def test_dataset_show(self, fake_open_new_tab):
        url = 'https://iatiregistry.org/dataset/old-org-acts'
        self.activity_dataset.show()
        fake_open_new_tab.assert_called_once_with(url)

    def test_activities(self):
        assert self.activity_dataset.activities.count() == 2
        activity = self.activity_dataset.activities[1]
        assert activity.id == 'NL-CHC-98765-NL-CHC-98765-XGG00NS00'

    def test_metadata(self):
        dataset_metadata = self.activity_dataset.metadata
        assert dataset_metadata.get('extras') \
            .get('publisher_organization_type') == '21'
