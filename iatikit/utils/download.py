import csv
from collections import OrderedDict, defaultdict
import json
from os.path import exists, join
from os import listdir, makedirs, unlink as _unlink
import shutil
import logging
import zipfile

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from ..standard.codelist import CodelistSet
from .config import CONFIG
from . import helpers


http_adapter = HTTPAdapter(max_retries=Retry(total=3))


def data():
    session = requests.Session()
    session.mount('https://', http_adapter)
    path = CONFIG['paths']['registry']
    # downloads from https://iati-data-dump.codeforiati.org
    download_url = 'https://iati-data-dump.codeforiati.org/download'
    response = session.get(download_url)
    data_url = response.text.strip()
    shutil.rmtree(path, ignore_errors=True)
    makedirs(path)
    zip_filepath = join(path, 'iati_dump.zip')

    logging.getLogger(__name__).info('Downloading all IATI registry data...')
    response = session.get(data_url, stream=True)
    with open(zip_filepath, 'wb') as handler:
        shutil.copyfileobj(response.raw, handler)
    logging.getLogger(__name__).info('Unzipping data...')
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(path)
    logging.getLogger(__name__).info('Cleaning up...')
    zip_output_path = join(path, 'iati-data-main')
    for f in listdir(zip_output_path):
        shutil.move(join(zip_output_path, f), path)
    _unlink(zip_filepath)


def metadata():
    session = requests.Session()
    session.mount('https://', http_adapter)
    logging.getLogger(__name__).info(
        'Downloading metadata from the IATI registry...')
    path = join(CONFIG['paths']['registry'], 'metadata')
    shutil.rmtree(path, ignore_errors=True)
    makedirs(path)

    url_tmpl = 'https://iatiregistry.org/api/3/action/package_search' + \
               '?start={start}&rows=1000'
    org_url_tmpl = 'https://iatiregistry.org/api/3/action/group_show' + \
                   '?id={org_slug}'
    start = 0
    while True:
        j = session.get(url_tmpl.format(start=start)).json()
        if len(j['result']['results']) == 0:
            break
        for res in j['result']['results']:
            org = res['organization']
            if not org:
                continue
            org_name = org['name']
            if not exists(join(path, org_name + '.json')):
                j = session.get(org_url_tmpl.format(org_slug=org_name)).json()
                with open(join(path, org_name + '.json'), 'w') as f:
                    json.dump(j['result'], f)
            dataset_name = res['name']
            orgpath = join(path, org_name)
            makedirs(orgpath, exist_ok=True)
            with open(join(orgpath, dataset_name + '.json'), 'w') as f:
                json.dump(res, f)
        start += 1000


_VERY_OLD_IATI_VERSIONS = ['1.01', '1.02']
_VERY_OLD_CODELISTS_URL = 'http://codelists102.archive.iatistandard.org' + \
                         '/data/codelist.csv'
_VERY_OLD_CODELIST_TMPL = 'http://codelists102.archive.iatistandard.org' + \
                         '/data/codelist/{codelist_name}.csv'

_OLD_IATI_VERSIONS = ['1.03']
_OLD_CODELISTS_URL = 'http://codelists103.archive.iatistandard.org' + \
                    '/data/codelist.json'
_OLD_CODELIST_TMPL = 'http://codelists103.archive.iatistandard.org' + \
                    '/data/codelist/{codelist_name}.csv'

_NEW_CODELISTS_TMPL = 'https://iatistandard.org/' + \
                      'reference_downloads/{version}/' + \
                      'codelists/downloads/clv2/codelists.json'
_NEW_CODELIST_TMPL = 'https://iatistandard.org/' + \
                     'reference_downloads/{version}/' + \
                     'codelists/downloads/clv2/json/en/{codelist_name}.json'


def _get_codelist_mappings(versions):
    all_codelists = CodelistSet()

    session = requests.Session()
    session.mount('https://', http_adapter)

    path = join(CONFIG['paths']['standard'], 'codelist_mappings')
    shutil.rmtree(path, ignore_errors=True)
    makedirs(path)

    logging.getLogger(__name__).info(
        'Downloading IATI Standard codelist mappings...')

    tmpl = 'https://iatistandard.org/reference_downloads/' + \
           '{version}/codelists/downloads/clv2/mapping.json'
    for version in versions:
        if version not in ['1.01', '1.02', '1.03']:
            version_path = version.replace('.', '')
            mapping_path = join(path, version_path)
            makedirs(mapping_path)

            mapping_url = tmpl.format(version=version_path)
            mappings = session.get(mapping_url).json()

            activity_mappings = [
                x for x in mappings
                if not x['path'].startswith('//iati-org')]
            filepath = join(mapping_path, 'activity-mappings.json')
            with open(filepath, 'w') as handler:
                json.dump(activity_mappings, handler)

            organisation_mappings = [
                x for x in mappings
                if not x['path'].startswith('//iati-act')]
            filepath = join(mapping_path, 'organisation-mappings.json')
            with open(filepath, 'w') as handler:
                json.dump(organisation_mappings, handler)


def codelists():
    def get_list_of_codelists(version):
        session = requests.Session()
        session.mount('https://', http_adapter)
        if version in _VERY_OLD_IATI_VERSIONS:
            request = session.get(_VERY_OLD_CODELISTS_URL)
            # import pdb; pdb.set_trace()
            list_of_codelists = [x['name'] for x in csv.DictReader(
                [x.decode() for x in request.iter_lines()])]
        elif version in _OLD_IATI_VERSIONS:
            j = session.get(_OLD_CODELISTS_URL).json()
            list_of_codelists = [x['name'] for x in j['codelist']]
        else:
            codelists_url = _NEW_CODELISTS_TMPL.format(
                version=version.replace('.', ''))
            list_of_codelists = session.get(codelists_url).json()
        return list_of_codelists

    def get_codelist(codelist_name, version):
        session = requests.Session()
        session.mount('https://', http_adapter)
        if version in _VERY_OLD_IATI_VERSIONS:
            codelist_url = _VERY_OLD_CODELIST_TMPL.format(
                codelist_name=codelist_name)
            request = session.get(codelist_url)
            codes = list(csv.DictReader(
                [x.decode() for x in request.iter_lines()]))
            version_codelist = {'data': codes}
        elif version in _OLD_IATI_VERSIONS:
            codelist_url = _OLD_CODELIST_TMPL.format(
                codelist_name=codelist_name)
            request = session.get(codelist_url)
            codes = list(csv.DictReader(
                [x.decode() for x in request.iter_lines()]))
            version_codelist = {'data': codes}
        else:
            codelist_url = _NEW_CODELIST_TMPL.format(
                codelist_name=codelist_name,
                version=version.replace('.', ''))
            version_codelist = session.get(codelist_url).json()
        return version_codelist

    path = join(CONFIG['paths']['standard'], 'codelists')
    shutil.rmtree(path, ignore_errors=True)
    makedirs(path)

    logging.getLogger(__name__).info(
        'Downloading IATI Standard codelists...')

    codelist_versions_by_name = defaultdict(list)
    all_versions = helpers.get_iati_versions()
    for version in all_versions:
        for codelist_name in get_list_of_codelists(version):
            codelist_versions_by_name[codelist_name].append(version)

    with open(join(path, 'codelists.json'), 'w') as handler:
        json.dump(codelist_versions_by_name, handler)

    for codelist_name, versions in codelist_versions_by_name.items():
        codelist = None
        for version in versions:
            version_codelist = get_codelist(codelist_name, version)

            if version_codelist.get('attributes', {}).get('embedded') == '0':
                codelist = version_codelist
                codelist['data'] = OrderedDict(
                    [(x['code'], x) for x in codelist['data']])
                break

            if codelist is None:
                codelist = {
                    'attributes': version_codelist.get('attributes', {}),
                    'metadata': version_codelist.get('metadata', {}),
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

        with open(join(path, codelist_name + '.json'), 'w') as handler:
            json.dump(codelist, handler)

    _get_codelist_mappings(all_versions)


def schemas():
    session = requests.Session()
    session.mount('https://', http_adapter)
    path = join(CONFIG['paths']['standard'], 'schemas')
    shutil.rmtree(path, ignore_errors=True)
    makedirs(path)

    versions_url = 'https://iatistandard.org/reference_downloads/' + \
                   '201/codelists/downloads/clv2/json/en/' + \
                   'Version.json'
    versions = [d['code'] for d in session.get(versions_url).json()['data']]
    versions.reverse()

    logging.getLogger(__name__).info('Downloading IATI Standard schemas...')
    filenames = ['iati-activities-schema.xsd', 'iati-organisations-schema.xsd',
                 'iati-common.xsd', 'xml.xsd']
    tmpl = 'https://raw.githubusercontent.com/IATI/IATI-Schemas/' + \
           'version-{version}/{filename}'
    for version in versions:
        version_path = version.replace('.', '')
        makedirs(join(path, version_path))
        for filename in filenames:
            url = tmpl.format(version=version, filename=filename)
            request = session.get(url)
            filepath = join(path, version_path, filename)
            with open(filepath, 'wb') as handler:
                handler.write(request.content)


def standard():
    schemas()
    codelists()
