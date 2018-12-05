import shutil
import zipfile
from os import unlink, makedirs
from os.path import join
import logging

import requests

from .publisher import PublisherSet


logger = logging.getLogger(__name__)


class Registry:
    def __init__(self, path=None):
        if path:
            self.path = path
        else:
            self.path = join('__pyandicache__', 'registry')

    def publishers(self):
        return PublisherSet(self.path)

    def download(self):
        # downloads from https://andylolz.github.io/iati-data-dump/
        data_url = 'https://www.dropbox.com/s/kkm80yjihyalwes/' + \
                   'iati_dump.zip?dl=1'
        shutil.rmtree(self.path, ignore_errors=True)
        makedirs(self.path)
        zip_filepath = join(self.path, 'iati_dump.zip')

        logger.info('Downloading all IATI registry data...')
        r = requests.get(data_url, stream=True)
        with open(zip_filepath, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        logger.info('Unzipping data...')
        with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
            zip_ref.extractall(self.path)
        logger.info('Cleaning up...')
        unlink(zip_filepath)
        logger.info('Downloading zipfile metadata...')
        meta_filepath = join(self.path, 'metadata.json')
        meta = 'https://www.dropbox.com/s/6a3wggckhbb9nla/metadata.json?dl=1'
        zip_metadata = requests.get(meta)
        with open(meta_filepath, 'wb') as f:
            f.write(zip_metadata.content)


def publishers():
    return Registry().publishers()
