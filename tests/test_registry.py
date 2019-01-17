from datetime import datetime
from os.path import abspath, dirname, join
import shutil
import tempfile
from unittest import TestCase

from freezegun import freeze_time
import pytest

from iatikit.data.registry import Registry
from iatikit.utils.exceptions import NoDataError
from iatikit.utils.config import CONFIG
import iatikit.data


class TestNoData(TestCase):
    def setUp(self):
        self.empty_path = tempfile.mkdtemp(dir=dirname(abspath(__file__)))
        config_dict = {'paths': {'registry': self.empty_path}}
        CONFIG.read_dict(config_dict)

    def test_no_data(self):
        with pytest.raises(NoDataError):
            Registry()

    def tearDown(self):
        shutil.rmtree(self.empty_path, ignore_errors=True)


class TestRegistry(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRegistry, self).__init__(*args, **kwargs)
        registry_path = join(dirname(abspath(__file__)),
                             'fixtures', 'registry')
        config_dict = {'paths': {'registry': registry_path}}
        CONFIG.read_dict(config_dict)

    @freeze_time("2015-12-09 08:00:00")
    def test_last_updated(self):
        with pytest.warns(UserWarning, match=r'last updated 8 days ago'):
            registry = Registry()
        assert registry.last_updated == datetime(2015, 12, 1, 3, 57, 19)

    @freeze_time("2015-12-02")
    def test_publishers(self):
        publisher_names = ['fixture-org', 'old-org']
        registry = Registry()
        publishers = registry.publishers
        assert len(publishers) == 2
        assert publishers[0].name in publisher_names

    @freeze_time("2015-12-02")
    def test_datasets(self):
        dataset_names = [
            'fixture-org-activities',
            'fixture-org-activities2',
            'fixture-org-org',
            'old-org-acts',
        ]
        registry = Registry()
        datasets = registry.datasets
        assert len(datasets) == 4
        for dataset in datasets:
            assert dataset.name in dataset_names

    @freeze_time("2015-12-02")
    def test_activities(self):
        activity_dataset_names = [
            'fixture-org-activities',
            'fixture-org-activities2',
            'old-org-acts',
        ]
        registry = Registry()
        activities = registry.activities
        assert len(activities) == 6
        for activity in activities:
            assert activity.dataset.name in activity_dataset_names

    @freeze_time("2015-12-02")
    def test_shortcut(self):
        registry = iatikit.data()
        assert(len(registry.datasets)) == 4
