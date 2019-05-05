import datetime
from os.path import abspath, dirname, join
from unittest import TestCase

from mock import patch
from lxml import etree as ET
import pytest

from iatikit.data.dataset import DatasetSet, Dataset
from iatikit.data.activity import ActivitySet, Activity
from iatikit.standard.activity_schema import ActivitySchema105
from iatikit.utils.config import CONFIG
from iatikit import Sector


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

        standard_path = join(dirname(abspath(__file__)), 'fixtures',
                             'standard')
        config_dict = {'paths': {'standard': standard_path}}
        CONFIG.read_dict(config_dict)

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

    def test_activities_filter_by_title_startswith(self):
        title_start = 'Development'
        acts = self.fixture_org_acts.where(title__startswith=title_start).all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == 'GB-COH-01234567-1'

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
        sector = Sector('15163', vocabulary='DAC')
        acts = self.fixture_org_acts.where(
            sector=sector).all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == 'GB-COH-01234567-1'

    def test_activities_filter_by_bad_sector(self):
        err_msg = 'bad-sector is not a sector'
        with pytest.raises(Exception, match=err_msg):
            self.fixture_org_acts.where(sector='bad-sector').all()

    # TODO
    def test_activities_filter_by_sector_in(self):
        sector = Sector('151', vocabulary='2')
        acts = self.fixture_org_acts.where(
            sector__in=sector).all()
        assert len(acts) == 1

    def test_activities_filter_by_bad_sector_in(self):
        err_msg = 'bad-sector-cat is not a sector category'
        with pytest.raises(Exception, match=err_msg):
            self.fixture_org_acts.where(sector__in='bad-sector-cat').all()

    def test_activities_filter_by_sector_exists(self):
        acts = self.fixture_org_acts.where(
            sector__exists=False).all()
        assert len(acts) == 1

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

    def test_activities_filter_by_actual_end_exists(self):
        acts = self.fixture_org_acts.where(
            actual_end__exists=True).all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == 'GB-COH-01234567-Humanitarian Aid-1'

    def test_activities_filter_by_xpath(self):
        acts = self.fixture_org_acts.where(
            xpath='activity-status/@code="2"').all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == 'GB-COH-01234567-Humanitarian Aid-0'

    def test_activities_filter_by_humanitarian(self):
        acts = self.fixture_org_acts.where(
            humanitarian=True).all()
        assert len(acts) == 1
        assert acts[0].iati_identifier == 'GB-COH-01234567-1'

    def test_activities_filter_by_not_humanitarian(self):
        acts = self.fixture_org_acts.where(
            humanitarian=False).all()
        assert len(acts) == 3


class TestActivity(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestActivity, self).__init__(*args, **kwargs)
        data_path = join(dirname(abspath(__file__)),
                         'fixtures', 'registry', 'data', 'fixture-org',
                         'fixture-org-activities2.xml')
        etree = ET.parse(data_path)
        activity_el = etree.xpath('//iati-activity')[0]
        activity_el1 = etree.xpath('//iati-activity')[1]
        activity_el2 = etree.xpath('//iati-activity')[2]
        dataset = Dataset(data_path, None)
        schema = ActivitySchema105()
        self.activity = Activity(activity_el, dataset, schema)
        self.activity1 = Activity(activity_el1, dataset, schema)
        self.activity2 = Activity(activity_el2, dataset, schema)

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

    def test_activity_repr(self):
        act_repr = '<Activity (GB-COH-01234567-Humanitarian Aid-0)>'
        assert str(self.activity) == act_repr

    def test_activity_title(self):
        title = 'Humanitarian Aid - Implementor 1'
        assert self.activity.title[0] == title

    def test_activity_description(self):
        assert self.activity.description == []

    # TODO
    def test_activity_sector(self):
        sector = Sector('73010', vocabulary='1')
        assert self.activity.sector[0] == sector

    def test_activity_planned_start(self):
        assert self.activity2.planned_start == datetime.date(2009, 1, 1)

    def test_activity_start(self):
        assert self.activity.start == datetime.date(2013, 4, 16)

    def test_activity_no_end(self):
        assert self.activity.end is None

    def test_activity_end(self):
        assert self.activity1.end == datetime.date(2015, 1, 16)
