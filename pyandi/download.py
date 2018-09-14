from time import time
from os.path import join
from os import unlink, makedirs
import shutil
import zipfile

import requests


def timer(func):
    def wrapper(*args, **kwargs):
        if not kwargs.get('timer'):
            return func(*args, **kwargs)
        else:
            start = time()
            out = func(*args, **kwargs)
            end = time()
            print('Elapsed time: {:.1f} seconds.'.format(end - start))
            return out

    return wrapper


@timer
def refresh_data(**kwargs):
    # downloads from https://andylolz.github.io/iati-data-dump/
    data_url = 'https://www.dropbox.com/s/kkm80yjihyalwes/iati_dump.zip?dl=1'
    data_path = join('__pyandicache__', 'data')
    shutil.rmtree(data_path, ignore_errors=True)
    makedirs(data_path)
    zip_filepath = join(data_path, 'iati_dump.zip')

    print('Downloading...')
    r = requests.get(data_url, stream=True)
    with open(zip_filepath, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    print('Unzipping...')
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(data_path)
    print('Cleaning up...')
    unlink(zip_filepath)


@timer
def refresh_codelists(**kwargs):
    base_tmpl = 'http://reference.iatistandard.org/{version}/' + \
                'codelists/downloads/'
    print('Refreshing codelists...')
    for version in ['105', '201']:
        codelist_path = join('__pyandicache__', 'codelists', version[0])
        shutil.rmtree(codelist_path, ignore_errors=True)
        makedirs(codelist_path)
        codelist_url = base_tmpl.format(version=version) + 'clv1/codelist.json'
        j = requests.get(codelist_url).json()
        codelist_names = [x['name'] for x in j['codelist']]
        for codelist_name in codelist_names:
            codelist_url = base_tmpl.format(version=version) + \
                           'clv2/json/en/{}.json'.format(codelist_name)
            j = requests.get(codelist_url)
            codelist_filepath = join(codelist_path, '{}.json'.format(
                codelist_name))
            with open(codelist_filepath, 'wb') as f:
                f.write(j.content)
