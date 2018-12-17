import json
from os.path import join
from os import makedirs
import shutil
import logging

import requests

from ..data.registry import Registry


logger = logging.getLogger(__name__)


# Ideally, information about embedded / non-embedded would
# come from the codelist API, rather than a hardcoded list.
#
# See: https://github.com/IATI/IATI-Codelists/issues/189
EMBEDDED_CODELISTS = [
    'ActivityDateType',
    'ActivityStatus',
    'AidTypeFlag',
    'BudgetStatus',
    'BudgetType',
    'DocumentCategory',
    'GazetteerAgency',
    'OrganisationRole',
    'RelatedActivityType',
    'TransactionType',
    'Vocabulary',
]


def data(path=None):
    Registry(path).download()


def codelists(path=None):
    if not path:
        path = join('__pyandicache__', 'standard', 'codelists')

    shutil.rmtree(path, ignore_errors=True)
    makedirs(path)
    makedirs(join(path, 'non-embedded'))

    logger.info('Downloading IATI Standard codelists...')
    versions_url = 'http://reference.iatistandard.org/105/codelists/' + \
                   'downloads/clv2/json/en/Version.json'
    versions = [d['code'] for d in requests.get(versions_url).json()['data']]
    base_tmpl = 'http://reference.iatistandard.org/{version}/' + \
                'codelists/downloads/'

    codelist_versions_by_name = {}
    for version in versions[::-1]:
        if version in ['1.01', '1.02', '1.03']:
            # TODO: these are available, but only as XML / CSV
            continue
        version_str = version.replace('.', '')
        makedirs(join(path, version_str))
        codelist_url = base_tmpl.format(version=version_str) + \
            'clv2/codelists.json'
        codelists = requests.get(codelist_url).json()

        # make unique.
        #
        # See: https://github.com/IATI/IATI-Codelists/issues/183
        codelists = list(set(codelists))

        codelist_filepath = join(path, version_str, 'codelists.json')
        for codelist_name in codelists:
            codelist_url = base_tmpl.format(version=version_str) + \
                           'clv2/json/en/{}.json'.format(codelist_name)
            r = requests.get(codelist_url)
            if 'non-embedded' in \
                    codelist_versions_by_name.get(codelist_name, []):
                continue
            if codelist_name not in EMBEDDED_CODELISTS:
                codelist_filepath = join(
                    path, 'non-embedded', '{}.json'.format(codelist_name))
                codelist_versions_by_name[codelist_name] = ['non-embedded']
            else:
                codelist_filepath = join(
                    path, version_str, '{}.json'.format(codelist_name))
                if codelist_name not in codelist_versions_by_name:
                    codelist_versions_by_name[codelist_name] = []
                codelist_versions_by_name[codelist_name].append(version)
            with open(codelist_filepath, 'wb') as f:
                f.write(r.content)

    with open(join(path, 'codelists.json'), 'w') as f:
        json.dump(codelist_versions_by_name, f)
