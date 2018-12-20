from collections import OrderedDict
import csv
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
    very_old_versions = ['1.01', '1.02']
    old_versions = ['1.03']
    very_old_codelists_url = 'http://codelists102.archive.iatistandard.org' + \
                             '/data/codelist.csv'
    old_codelists_url = 'http://codelists103.archive.iatistandard.org' + \
                        '/data/codelist.json'
    new_codelists_tmpl = 'http://reference.iatistandard.org/{version}/' + \
                         'codelists/downloads/clv2/codelists.json'
    very_old_codelist_tmpl = 'http://codelists102.archive.iatistandard.org' + \
                             '/data/codelist/{codelist_name}.csv'
    old_codelist_tmpl = 'http://codelists103.archive.iatistandard.org' + \
                        '/data/codelist/{codelist_name}.csv'
    new_codelist_tmpl = 'http://reference.iatistandard.org/{version}/' + \
                        'codelists/downloads/clv2/json/en/{codelist_name}.json'
    if not path:
        path = join('__pyandicache__', 'standard', 'codelists')

    shutil.rmtree(path, ignore_errors=True)
    makedirs(path)

    logger.info('Downloading IATI Standard codelists...')
    versions_url = 'http://reference.iatistandard.org/codelists/' + \
                   'downloads/clv2/json/en/Version.json'
    versions = [d['code'] for d in requests.get(versions_url).json()['data']]
    versions.reverse()

    codelist_versions_by_name = {}
    for version in versions:
        if version in very_old_versions:
            r = requests.get(very_old_codelists_url)
            codelists = [x['name'] for x in csv.DictReader(
                [x.decode() for x in r.iter_lines()])]
        elif version in old_versions:
            j = requests.get(old_codelists_url).json()
            codelists = [x['name'] for x in j['codelist']]
        else:
            codelists_url = new_codelists_tmpl.format(
                version=version.replace('.', ''))
            codelists = requests.get(codelists_url).json()

        # make unique.
        #
        # See: https://github.com/IATI/IATI-Codelists/issues/183
        codelists = list(set(codelists))

        for codelist_name in codelists:
            if codelist_name not in codelist_versions_by_name:
                codelist_versions_by_name[codelist_name] = []
            codelist_versions_by_name[codelist_name].append(version)

    with open(join(path, 'codelists.json'), 'w') as f:
        json.dump(codelist_versions_by_name, f)

    for codelist_name, versions in codelist_versions_by_name.items():
        codelist = None
        for version in versions:
            if version in very_old_versions:
                codelist_url = very_old_codelist_tmpl.format(
                    codelist_name=codelist_name)
                r = requests.get(codelist_url)
                codes = list(csv.DictReader(
                    [x.decode() for x in r.iter_lines()]))
                version_codelist = {'data': codes}
            elif version in old_versions:
                codelist_url = old_codelist_tmpl.format(
                    codelist_name=codelist_name)
                r = requests.get(codelist_url)
                codes = list(csv.DictReader(
                    [x.decode() for x in r.iter_lines()]))
                version_codelist = {'data': codes}
            else:
                codelist_url = new_codelist_tmpl.format(
                    codelist_name=codelist_name,
                    version=version.replace('.', ''))
                version_codelist = requests.get(codelist_url).json()
            if codelist_name not in EMBEDDED_CODELISTS:
                codelist = version_codelist
                codelist['data'] = OrderedDict(
                    [(x['code'], x) for x in codelist['data']])
                break
            if codelist is None:
                codelist = {
                    'attributes': version_codelist.get('attributes'),
                    'metadata': version_codelist.get('metadata'),
                    'data': OrderedDict(),
                }
            for item in version_codelist['data']:
                if item['code'] not in codelist['data']:
                    item['from'] = version
                    item['until'] = version
                    codelist['data'][item['code']] = item
                else:
                    current_item = codelist['data'][item['code']]
                    if version < current_item['from']:
                        current_item['from'] = version
                    if version > current_item['until']:
                        current_item['until'] = version
                    codelist['data'][item['code']] = current_item

        with open(join(path, codelist_name + '.json'), 'w') as f:
            json.dump(codelist, f)
