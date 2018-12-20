from datetime import datetime
import shutil
import zipfile
from os import unlink, makedirs
from os.path import join
import logging
import json

import requests

from .publisher import PublisherSet
from .dataset import DatasetSet
from .activity import ActivitySet
from ..utils.exceptions import NoDataError


logger = logging.getLogger(__name__)


class Registry:
    def __init__(self, path=None):
        if path:
            self.path = path
        else:
            self.path = join('__pyandicache__', 'registry')

        if self.last_updated:
            days_ago = (datetime.now() - self.last_updated).days
            if days_ago > 7:
                warning_msg = 'Warning: Data was last updated {} days ' + \
                              'ago. Consider downloading a fresh ' + \
                              'data dump, using:\n\n   ' + \
                              '>>> pyandi.download.data()\n'
                logger.warn(warning_msg.format(days_ago))
        else:
            error_msg = 'Error: No data found! ' + \
                          'Download a fresh data dump ' + \
                          'using:\n\n   ' + \
                          '>>> pyandi.download.data()\n'
            raise NoDataError(error_msg)

    @property
    def last_updated(self):
        try:
            with open(join(self.path, 'metadata.json')) as f:
                j = json.load(f)
            last_updated = j['updated_at']
            last_updated = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%S')
        except:
            last_updated = None
        return last_updated

    @property
    def publishers(self):
        data_path = join(self.path, 'data', '*')
        metadata_path = join(self.path, 'metadata', '*', '')
        return PublisherSet(data_path, metadata_path)

    @property
    def datasets(self):
        r = self.publishers
        data_path = join(r.data_path, '*')
        metadata_path = join(r.metadata_path, '*')
        return DatasetSet(data_path, metadata_path)

    @property
    def activities(self):
        return ActivitySet(self.datasets)

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
