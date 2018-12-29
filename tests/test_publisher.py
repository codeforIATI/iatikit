from os.path import abspath, dirname, join
from unittest import TestCase

from pyandi.data.publisher import PublisherSet


class TestPublishers(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPublishers, self).__init__(*args, **kwargs)
        self.registry_path = join(dirname(abspath(__file__)),
                                  'fixtures', 'registry')

    def setUp(self):
        # TODO: Fix this signature. It is very weird!
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
        assert len(empty_publisher_list) == 0

        filtered_pubs = self.publishers.where(name='fixture-org')
        publisher_list = list(filtered_pubs)
        assert len(publisher_list) == 1
        assert publisher_list[0].name == 'fixture-org'

    def test_publishers_index_slicing(self):
        publisher_list = self.publishers[:]
        assert len(publisher_list) == 2

    def test_publishers_indexing(self):
        publisher_names = ['fixture-org', 'old-org']
        assert self.publishers[0].name in publisher_names
        assert self.publishers[1].name in publisher_names
