import json
from os.path import join
from os import unlink, makedirs
import shutil
import zipfile

import requests


def data(path=None):
    # downloads from https://andylolz.github.io/iati-data-dump/
    data_url = 'https://www.dropbox.com/s/kkm80yjihyalwes/iati_dump.zip?dl=1'
    if not path:
        data_path = join('__pyandicache__', 'data')
    else:
        data_path = path
    shutil.rmtree(data_path, ignore_errors=True)
    makedirs(data_path)
    zip_filepath = join(data_path, 'iati_dump.zip')

    print('Downloading data...')
    r = requests.get(data_url, stream=True)
    with open(zip_filepath, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    print('Unzipping data...')
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(data_path)
    print('Cleaning up...')
    unlink(zip_filepath)
    print('Downloading zip metadata...')
    meta_filepath = join(data_path, 'metadata.json')
    meta = 'https://www.dropbox.com/s/6a3wggckhbb9nla/metadata.json?dl=1'
    zip_metadata = requests.get(meta)
    with open(meta_filepath, 'wb') as f:
        f.write(zip_metadata.content)
    metadata()
    # TODO: Check they're in sync
    # e.g. by comparing number of files


def codelists():
    versions_url = 'http://reference.iatistandard.org/105/codelists/' + \
                   'downloads/clv2/json/en/Version.json'
    versions = [d['code'] for d in requests.get(versions_url).json()['data']]
    maxver = {}
    for version in versions:
        version_str = version.replace('.', '')
        major = version.split('.')[0]
        maxver[major] = max(maxver[major], version_str) \
            if major in maxver else version_str
    versions = maxver.items()
    base_tmpl = 'http://reference.iatistandard.org/{version}/' + \
                'codelists/downloads/'
    print('Downloading codelists...')
    for major, version in versions:
        codelist_path = join('__pyandicache__', 'codelists', major)
        shutil.rmtree(codelist_path, ignore_errors=True)
        makedirs(codelist_path)
        codelist_url = base_tmpl.format(version=version) + 'clv1/codelist.json'
        j = requests.get(codelist_url).json()
        codelist_names = [x['name'] for x in j['codelist']]
        for codelist_name in codelist_names:
            codelist_url = base_tmpl.format(version=version) + \
                           'clv2/json/en/{}.json'.format(codelist_name)
            r = requests.get(codelist_url)
            codelist_filepath = join(codelist_path, '{}.json'.format(
                codelist_name))
            with open(codelist_filepath, 'wb') as f:
                f.write(r.content)


def schemas():
    print('Downloading schemas...')
    schemas_path = join('__pyandicache__', 'schemas')
    versions_url = 'http://reference.iatistandard.org/codelists/downloads/' + \
                   'clv2/json/en/Version.json'
    versions = [v['code'] for v in requests.get(versions_url).json()['data']]

    old_tmpl = 'http://reference.iatistandard.org/downloads/{version}/{schema}'
    tmpl = 'http://reference.iatistandard.org/{version}/schema/' + \
           'downloads/{schema}'
    schema_names = [
        'xml.xsd',
        'iati-common.xsd',
        'iati-activities-schema.xsd',
        'iati-organisations-schema.xsd',
    ]
    for version in versions:
        schema_path = join(schemas_path, version)
        shutil.rmtree(schema_path, ignore_errors=True)
        makedirs(schema_path)
        for schema_name in schema_names:
            schema_filepath = join(schema_path, schema_name)
            if version in ['1.01', '1.02', '1.03']:
                url = old_tmpl.format(
                    version=version,
                    schema=schema_name)
            else:
                url = tmpl.format(
                    version=version.replace('.', ''),
                    schema=schema_name)
            r = requests.get(url, stream=True)
            r.raise_for_status()
            with open(schema_filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)


def metadata(path=None, delete_first=True):
    print('Downloading dataset metadata...')
    if not path:
        metadata_path = join('__pyandicache__', 'metadata')
    else:
        metadata_path = path
    if delete_first:
        shutil.rmtree(metadata_path, ignore_errors=True)
    url_tmpl = 'https://iatiregistry.org/api/3/action/package_search' + \
               '?start={start}&rows=1000'
    start = 0
    while True:
        j = requests.get(url_tmpl.format(start=start)).json()
        if len(j['result']['results']) == 0:
            break
        for r in j['result']['results']:
            org = r['organization']
            if not org:
                continue
            org_name = org['name']
            dataset_name = r['name']
            orgpath = join(metadata_path, org_name)
            makedirs(orgpath, exist_ok=True)
            with open(join(orgpath, dataset_name + '.json'), 'w') as f:
                json.dump(r, f)
        start += 1000
