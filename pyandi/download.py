from os.path import join
from os import unlink, makedirs
import shutil
import zipfile

import requests


def data():
    # downloads from https://andylolz.github.io/iati-data-dump/
    data_url = 'https://www.dropbox.com/s/kkm80yjihyalwes/iati_dump.zip?dl=1'
    data_path = join('__pyandicache__')
    shutil.rmtree(data_path, ignore_errors=True)
    makedirs(data_path)
    zip_filepath = join(data_path, 'iati_dump.zip')

    print('Downloading all IATI registry data...')
    r = requests.get(data_url, stream=True)
    with open(zip_filepath, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    print('Unzipping data...')
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(data_path)
    print('Cleaning up...')
    unlink(zip_filepath)
    print('Downloading zipfile metadata...')
    meta_filepath = join(data_path, 'metadata.json')
    meta = 'https://www.dropbox.com/s/6a3wggckhbb9nla/metadata.json?dl=1'
    zip_metadata = requests.get(meta)
    with open(meta_filepath, 'wb') as f:
        f.write(zip_metadata.content)


def codelists():
    print('Downloading IATI Standard codelists...')
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
    print('Downloading IATI Standard schemas...')
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
