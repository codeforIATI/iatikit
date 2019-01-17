from os.path import abspath, dirname, join
from unittest import TestCase

from mock import patch

from iatikit.data.dataset import DatasetSet, Dataset
from iatikit.utils.config import CONFIG


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
        self.old_org_acts = Dataset(
            join(registry_path, 'data',
                 'old-org', 'old-org-acts.xml'),
            join(registry_path, 'metadata',
                 'old-org', 'old-org-acts.json'),
        )

        self.fixture_org_acts = Dataset(
            join(registry_path, 'data',
                 'fixture-org', 'fixture-org-activities.xml'),
            join(registry_path, 'metadata',
                 'fixture-org', 'fixture-org-activities.json'),
        )

        standard_path = join(dirname(abspath(__file__)),
                             'fixtures', 'standard')
        config_dict = {'paths': {'standard': standard_path}}
        CONFIG.read_dict(config_dict)

    def test_dataset_name(self):
        assert self.old_org_acts.name == 'old-org-acts'

    def test_dataset_version(self):
        assert self.old_org_acts.version == '1.03'

    def test_dataset_repr(self):
        dataset_repr = '<Dataset (old-org-acts)>'
        assert str(self.old_org_acts) == dataset_repr

    def test_dataset_validate_xml(self):
        assert bool(self.old_org_acts.validate_xml()) is True

    def test_dataset_validate_iati(self):
        assert bool(self.old_org_acts.validate_iati()) is True

    @patch('logging.Logger.warning')
    def test_dataset_validate_codelists_old(self, fake_logger_warning):
        assert bool(self.old_org_acts.validate_codelists()) is True
        msg = ('Can\'t perform codelist validation for ' +
               'IATI version %s datasets.', '1.03')
        fake_logger_warning.assert_called_once_with(*msg)

    def test_dataset_validate_codelists(self):
        result = self.fixture_org_acts.validate_codelists()
        assert result.is_valid is False
        assert len(result.errors) == 2
        err_msgs = [
            'The value "999" is not in the Sector Vocabulary codelist.',
            'The value "6" is not in the Activity Status codelist.',
        ]
        for error in result.errors:
            assert str(error) in err_msgs

    def test_dataset_root(self):
        assert self.old_org_acts.root == 'iati-activities'

    @patch('webbrowser.open_new_tab')
    def test_dataset_show(self, fake_open_new_tab):
        url = 'https://iatiregistry.org/dataset/old-org-acts'
        self.old_org_acts.show()
        fake_open_new_tab.assert_called_once_with(url)

    def test_activities(self):
        assert self.old_org_acts.activities.count() == 2
        activity = self.old_org_acts.activities[1]
        assert activity.id == 'NL-CHC-98765-NL-CHC-98765-XGG00NS00'

    def test_metadata(self):
        dataset_metadata = self.old_org_acts.metadata
        assert dataset_metadata.get('extras') \
            .get('publisher_organization_type') == '21'
