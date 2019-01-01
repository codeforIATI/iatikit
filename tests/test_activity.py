import datetime
from os.path import abspath, dirname, join
from unittest import TestCase

from pyandi.data.dataset import DatasetSet
from pyandi.data.activity import ActivitySet


class TestActivitySet(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestActivitySet, self).__init__(*args, **kwargs)
        registry_path = join(dirname(abspath(__file__)),
                             'fixtures', 'registry')
        org_datasets = DatasetSet(
            join(registry_path, 'data', 'fixture-org', '*'),
            join(registry_path, 'metadata', 'fixture-org', '*'),
        )
        self.fixture_org_acts = ActivitySet(org_datasets)

    def test_activities_iter(self):
        activities = list(self.fixture_org_acts)
        assert len(activities) == 4

    def test_activities_len(self):
        assert len(self.fixture_org_acts) == 4

    def test_activities_filter_by_id(self):
        iati_id = 'GB-COH-01234567-Humanitarian Aid-1'
        acts = self.fixture_org_acts.where(id=iati_id).all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == iati_id

    def test_activities_filter_by_iati_identifier(self):
        iati_id = 'GB-COH-01234567-Humanitarian Aid-1'
        acts = self.fixture_org_acts.where(iati_identifier=iati_id).all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == iati_id

    def test_activities_filter_by_title_v1(self):
        title = 'Humanitarian Aid - Implementer 2'
        acts = self.fixture_org_acts.where(title=title).all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == 'GB-COH-01234567-Humanitarian Aid-1'

    def test_activities_filter_by_title_v2(self):
        title = 'Development work'
        acts = self.fixture_org_acts.where(title=title).all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == 'GB-COH-01234567-1'

    def test_activities_filter_by_description_contains(self):
        acts = self.fixture_org_acts.where(
            description__contains='bibendum tortor at orci').all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == 'GB-COH-01234567-1'

    def test_activities_filter_by_planned_start_v2(self):
        acts = self.fixture_org_acts.where(
            planned_start='2011-11-01').all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == 'GB-COH-01234567-1'

    def test_activities_filter_by_actual_start_v2(self):
        acts = self.fixture_org_acts.where(
            actual_start='2011-10-01').all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == 'GB-COH-01234567-1'

    def test_activities_filter_by_planned_end_v2(self):
        planned_end = datetime.date(2019, 9, 30)
        acts = self.fixture_org_acts.where(
            planned_end=planned_end).all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == 'GB-COH-01234567-1'

    def test_activities_filter_by_xpath(self):
        implmentation_ids = [
            'GB-COH-01234567-1',
            'GB-COH-01234567-Humanitarian Aid-0',
        ]
        acts = self.fixture_org_acts.where(
            xpath='activity-status/@code="2"').all()
        assert len(acts) == 2
        for act in acts:
            assert act.iati_identifier in implmentation_ids
