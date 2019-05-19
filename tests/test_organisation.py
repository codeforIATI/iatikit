from os.path import abspath, dirname, join
from unittest import TestCase

from iatikit.data.dataset import DatasetSet
from iatikit.data.organisation import OrganisationSet
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
