from os.path import abspath, dirname, join
from unittest import TestCase

from mock import patch
from lxml import etree as ET

from iatikit.data.dataset import DatasetSet, Dataset
from iatikit.data.organisation import OrganisationSet, Organisation
from iatikit.standard.organisation_schema import OrganisationSchema203
from iatikit.utils.config import CONFIG


class TestOrganisationSet(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestOrganisationSet, self).__init__(*args, **kwargs)
        registry_path = join(dirname(abspath(__file__)),
                             'fixtures', 'registry')
        org_datasets = DatasetSet(
            join(registry_path, 'data', 'fixture-org', '*'),
            join(registry_path, 'metadata', 'fixture-org', '*'),
        )
        self.fixture_org_orgs = OrganisationSet(org_datasets)

        standard_path = join(dirname(abspath(__file__)), 'fixtures',
                             'standard')
        config_dict = {'paths': {'standard': standard_path}}
        CONFIG.read_dict(config_dict)

    def test_organisations_iter(self):
        organisations = list(self.fixture_org_orgs)
        assert len(organisations) == 1

    def test_organisations_len(self):
        assert len(self.fixture_org_orgs) == 1

    def test_organisations_filter_by_id(self):
        iati_id = 'GB-COH-01234567'
        orgs = self.fixture_org_orgs.where(id=iati_id).all()
        assert len(orgs) == 1
        assert orgs[0].org_identifier == iati_id

        not_iati_id = 'GB-COH-01234567-No-identifier'
        orgs = self.fixture_org_orgs.where(id=not_iati_id).all()
        assert len(orgs) == 0

    def test_organisations_filter_by_iati_identifier(self):
        iati_id = 'GB-COH-01234567'
        orgs = self.fixture_org_orgs.where(org_identifier=iati_id).all()
        assert len(orgs) == 1
        assert orgs[0].org_identifier == iati_id

        not_iati_id = 'GB-COH-01234567-No-identifier'

        orgs = self.fixture_org_orgs.where(org_identifier=not_iati_id).all()
        assert len(orgs) == 0


class TestOrganisation(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestOrganisation, self).__init__(*args, **kwargs)
        data_path = join(dirname(abspath(__file__)),
                         'fixtures', 'registry', 'data', 'fixture-org',
                         'fixture-org-org.xml')
        etree = ET.parse(data_path)
        org_el = etree.xpath('//iati-organisation')[0]
        dataset = Dataset(data_path, None)
        schema = OrganisationSchema203()
        self.organisation = Organisation(org_el, dataset, schema)

    @patch('webbrowser.open_new_tab')
    def test_activity_show(self, fake_open_new_tab):
        url = 'http://d-portal.org/ctrack.html' + \
              '?publisher=GB-COH-01234567#view=main'
        self.organisation.show()
        fake_open_new_tab.assert_called_once_with(url)

    def test_organisation_xml(self):
        xml = self.organisation.xml
        first_line = '<iati-organisation last-updated-datetime=' + \
                     '"2018-10-23T22:27:45" default-currency="GBP" ' + \
                     'xml:lang="en">'
        assert xml.decode().split('\n', 1)[0] == first_line

    def test_organisation_id(self):
        id_ = 'GB-COH-01234567'
        assert self.organisation.id == id_
        assert self.organisation.org_identifier == id_

    def test_organisation_repr(self):
        org_repr = '<Organisation (GB-COH-01234567)>'
        assert str(self.organisation) == org_repr
