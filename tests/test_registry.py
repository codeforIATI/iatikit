from datetime import datetime
from os.path import abspath, dirname, join
import shutil
import tempfile
from unittest import TestCase

from freezegun import freeze_time
import pytest

from pyandi.data.registry import Registry
from pyandi.utils.exceptions import NoDataError


class TestNoData(TestCase):
    def setUp(self):
        self.empty_path = tempfile.mkdtemp(dir=dirname(abspath(__file__)))

    def test_no_data(self):
        with pytest.raises(NoDataError):
            Registry(self.empty_path)

    def tearDown(self):
        shutil.rmtree(self.empty_path, ignore_errors=True)


class TestRegistry(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRegistry, self).__init__(*args, **kwargs)
        self.registry_path = join(dirname(abspath(__file__)),
                                  'fixtures', 'registry')

    @freeze_time("2015-12-09 08:00:00")
    def test_last_updated(self):
        with pytest.warns(UserWarning, match=r'last updated 8 days ago'):
            registry = Registry(self.registry_path)
        assert registry.last_updated == datetime(2015, 12, 1, 3, 57, 19)

    @freeze_time("2015-12-02")
    def test_publishers(self):
        registry = Registry(self.registry_path)
        publishers = registry.publishers
        assert len(publishers) == 1
        assert publishers[0].name == 'fixture-org'

    @freeze_time("2015-12-02")
    def test_datasets(self):
        registry = Registry(self.registry_path)
        datasets = registry.datasets
        assert len(datasets) == 2
        for x in datasets:
            assert x.name in ['fixture-org-activities', 'fixture-org-org']

    @freeze_time("2015-12-02")
    def test_activities(self):
        registry = Registry(self.registry_path)
        activities = registry.activities
        assert len(activities) == 1
        assert activities[0].version == '2.03'
