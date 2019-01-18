from os.path import abspath, dirname, join
from unittest import TestCase

from mock import patch
import pytest

from iatikit.data.publisher import PublisherSet, Publisher
from iatikit.utils.exceptions import FilterError


class TestPublishers(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPublishers, self).__init__(*args, **kwargs)
        self.registry_path = join(dirname(abspath(__file__)),
                                  'fixtures', 'registry')

    def setUp(self):
        self.publishers = PublisherSet(
            join(self.registry_path, 'data', '*'),
            join(self.registry_path, 'metadata', '*'),
        )

    def test_publishers_iter(self):
        publisher_list = list(self.publishers)
        assert len(publisher_list) == 2

    def test_publishers_filter(self):
        bad_filtered_pubs = self.publishers.where(name='does-not-exist')
        empty_publisher_list = list(bad_filtered_pubs)
        assert empty_publisher_list == []

        filtered_pubs = self.publishers.where(name='fixture-org')
        publisher_list = list(filtered_pubs)
        assert len(publisher_list) == 1
        assert publisher_list[0].name == 'fixture-org'

    def test_publishers_unknown_filter(self):
        with pytest.raises(FilterError):
            self.publishers.find(unknown='unknown')

    def test_publishers_index_slicing(self):
        publisher_list = self.publishers[:]
        assert len(publisher_list) == 2

    def test_publishers_indexing(self):
        publisher_names = ['fixture-org', 'old-org']
        assert self.publishers[0].name in publisher_names
        assert self.publishers[1].name in publisher_names

    def test_publisher_from_publishers(self):
        fixture_org = self.publishers.get('fixture-org')
        assert fixture_org.name == 'fixture-org'
        assert fixture_org.datasets.count() == 3
        assert fixture_org.metadata.get(
            'publisher_iati_id') == 'GB-COH-01234567'

        old_org = self.publishers.get('old-org')
        assert old_org.name == 'old-org'
        assert old_org.datasets.count() == 1
        assert old_org.metadata.get(
            'publisher_iati_id') == 'NL-CHC-98765'


class TestPublisher(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPublisher, self).__init__(*args, **kwargs)
        self.registry_path = join(dirname(abspath(__file__)),
                                  'fixtures', 'registry')

    def setUp(self):
        self.fixture_org = Publisher(
            join(self.registry_path, 'data', 'fixture-org'),
            join(self.registry_path, 'metadata', 'fixture-org'),
            join(self.registry_path, 'metadata', 'no-metadata.json'),
        )
        self.old_org = Publisher(
            join(self.registry_path, 'data', 'old-org'),
            join(self.registry_path, 'metadata', 'old-org'),
            join(self.registry_path, 'metadata', 'old-org.json'),
        )

    def test_publisher_name(self):
        assert self.fixture_org.name == 'fixture-org'

    def test_publisher_repr(self):
        publisher_repr = '<Publisher (fixture-org)>'
        assert str(self.fixture_org) == publisher_repr

    @patch('webbrowser.open_new_tab')
    def test_publisher_show(self, fake_open_new_tab):
        url = 'https://iatiregistry.org/publisher/old-org'
        self.old_org.show()
        fake_open_new_tab.assert_called_once_with(url)

    def test_datasets(self):
        old_org_datasets = self.old_org.datasets.all()
        assert len(old_org_datasets) == 1
        assert old_org_datasets[0].name == 'old-org-acts'

    def test_activities(self):
        assert self.old_org.activities.count() == 2
        old_org_activity = self.old_org.activities[0]
        assert old_org_activity.id == 'NL-CHC-98765-NL-CHC-98765-XX0D9001'

    def test_metadata(self):
        old_org_metadata = self.old_org.metadata
        assert old_org_metadata.get('publisher_country') == 'NL'

    def test_no_metadata(self):
        assert self.fixture_org.metadata == {}
