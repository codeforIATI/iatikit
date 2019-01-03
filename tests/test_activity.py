import datetime
from os.path import abspath, dirname, join
from unittest import TestCase

from mock import patch
from lxml import etree as ET

from pyandi.data.dataset import DatasetSet, Dataset
from pyandi.data.activity import ActivitySet, Activity
from pyandi.standard.activity_schema import ActivitySchema105
from pyandi import Sector


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

    def test_activities_filter_by_description(self):
        description = 'Just a short description.'
        acts = self.fixture_org_acts.where(
            description=description).all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == 'GB-COH-01234567-Humanitarian Aid-1'

    def test_activities_filter_by_sector(self):
        path = join(dirname(abspath(__file__)), 'fixtures', 'codelists')
        sector = Sector('15163', vocabulary='DAC', path=path)
        acts = self.fixture_org_acts.where(
            sector=sector).all()
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


def mod_join(*args):
    if '/'.join(args) == '__pyandicache__/standard/codelists':
        path = join(dirname(abspath(__file__)), 'fixtures', 'codelists')
        return path
    else:
        return join(*args)


class TestActivity(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestActivity, self).__init__(*args, **kwargs)
        data_path = join(dirname(abspath(__file__)),
                         'fixtures', 'registry', 'data', 'fixture-org',
                         'fixture-org-activities2.xml')
        etree = ET.parse(data_path)
        activity_el = etree.xpath('//iati-activity')[0]
        dataset = Dataset(data_path, None)
        schema = ActivitySchema105()
        self.activity = Activity(activity_el, dataset, schema)

    @patch('webbrowser.open_new_tab')
    def test_activity_show(self, fake_open_new_tab):
        url = 'http://d-portal.org/q.html' + \
              '?aid=GB-COH-01234567-Humanitarian+Aid-0'
        self.activity.show()
        fake_open_new_tab.assert_called_once_with(url)

    def test_activity_xml(self):
        xml = self.activity.xml
        first_line = '<iati-activity default-currency="GBP" ' + \
                     'last-updated-datetime="2016-01-12T15:17:15">'
        assert xml.decode().split('\n', 1)[0] == first_line

    def test_activity_id(self):
        id_ = 'GB-COH-01234567-Humanitarian Aid-0'
        assert self.activity.id == id_
        assert self.activity.iati_identifier == id_

    def test_activity_title(self):
        title = 'Humanitarian Aid - Implementor 1'
        assert self.activity.title[0] == title

    def test_activity_description(self):
        assert len(self.activity.description) == 0

    @patch('os.path.join', mod_join)
    def test_activity_sector(self):
        sector = Sector('73010', vocabulary='1')
        self.activity.sector[0] == sector

    def test_activity_start(self):
        assert self.activity.start == datetime.date(2013, 4, 16)

    def test_activity_end(self):
        assert self.activity.end is None
