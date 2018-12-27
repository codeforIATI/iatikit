from datetime import datetime
from os.path import join
import json
import warnings

from .publisher import PublisherSet
from .dataset import DatasetSet
from .activity import ActivitySet
from ..utils.exceptions import NoDataError
from ..utils import download


class Registry(object):
    def __init__(self, path=None):
        self._last_updated = None
        if path:
            self.path = path
        else:
            self.path = join('__pyandicache__', 'registry')

        last_updated = self.last_updated
        days_ago = (datetime.now() - last_updated).days
        if days_ago > 7:
            warning_msg = 'Warning: Data was last updated {} days ' + \
                          'ago. Consider downloading a fresh ' + \
                          'data dump, using:\n\n   ' + \
                          '>>> pyandi.download.data()\n'
            warnings.warn(warning_msg.format(days_ago))

    @property
    def last_updated(self):
        if not self._last_updated:
            try:
                with open(join(self.path, 'metadata.json')) as f:
                    j = json.load(f)
            except FileNotFoundError:
                error_msg = 'Error: No data found! ' + \
                            'Download a fresh data dump ' + \
                            'using:\n\n   ' + \
                            '>>> pyandi.download.data()\n'
                raise NoDataError(error_msg)
            last_updated = j['updated_at']
            self._last_updated = datetime.strptime(
                last_updated, '%Y-%m-%dT%H:%M:%SZ')
        return self._last_updated

    @property
    def publishers(self):
        data_path = join(self.path, 'data', '*')
        metadata_path = join(self.path, 'metadata', '*')
        return PublisherSet(data_path, metadata_path)

    @property
    def datasets(self):
        r = self.publishers
        data_path = join(r.data_path, '*')
        metadata_path = join(r.metadata_path, '', '*')
        return DatasetSet(data_path, metadata_path)

    @property
    def activities(self):
        return ActivitySet(self.datasets)

    def download(self):
        return download.data(self.path)
