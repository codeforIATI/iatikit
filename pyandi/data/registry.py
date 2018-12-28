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
    """Class representing the IATI registry."""

    def __init__(self, path=None):
        """Construct a new Registry object.

        The file system location of the data and metadata can be specified
        with the ``path`` argument.

        A warning is raised if the data is more than 7 days old.
        """
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
        """Return the datetime when the local cache was last updated.

        Raise a ``FileNotFoundError`` if there is no data.
        """
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
        """Return an iterator of all publishers on the registry."""
        data_path = join(self.path, 'data', '*')
        metadata_path = join(self.path, 'metadata', '*')
        return PublisherSet(data_path, metadata_path)

    @property
    def datasets(self):
        """Return an iterator of all IATI datasets on the registry."""
        r = self.publishers
        data_path = join(r.data_path, '*')
        metadata_path = join(r.metadata_path, '', '*')
        return DatasetSet(data_path, metadata_path)

    @property
    def activities(self):
        """Return an iterator of all IATI activities on the registry."""
        return ActivitySet(self.datasets)

    def download(self):
        """Download all IATI data and registry metadata."""
        return download.data(self.path)
