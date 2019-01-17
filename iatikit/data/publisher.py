import json
import logging
from os.path import basename, exists, join
from glob import glob
import webbrowser

from ..utils.abstract import GenericSet
from .dataset import DatasetSet
from .activity import ActivitySet


class Publisher(object):
    """Class representing an IATI publisher."""

    def __init__(self, data_path, metadata_path, metadata_filepath):
        self.data_path = data_path
        self.metadata_path = metadata_path
        self.metadata_filepath = metadata_filepath
        self._metadata = None

    @property
    def name(self):
        """Return the "registry name" or "shortname" of this publisher,
        derived from the filepath.
        """
        return basename(self.data_path)

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, self.name)

    def show(self):
        """Open a new browser tab to the iatiregistry.org page
        for this publisher.
        """
        url = 'https://iatiregistry.org/publisher/{}'.format(
            self.name)
        webbrowser.open_new_tab(url)

    @property
    def datasets(self):
        """Return an iterator of all datasets for this publisher."""
        data_path = join(self.data_path, '*')
        metadata_path = join(self.metadata_path, '*')
        return DatasetSet(data_path, metadata_path)

    @property
    def activities(self):
        """Return an iterator of all activities for this publisher."""
        return ActivitySet(self.datasets)

    @property
    def metadata(self):
        """Return a dictionary of registry metadata for this publisher."""
        if self._metadata is None:
            if exists(self.metadata_filepath):
                with open(self.metadata_filepath) as handler:
                    self._metadata = json.load(handler)
            else:
                msg = 'No metadata was found for publisher "%s"'
                logging.warning(msg, self.name)
                self._metadata = {}
        return self._metadata


class PublisherSet(GenericSet):
    """Class representing a grouping of ``Publisher`` objects.

    Objects in this grouping can be filtered and iterated over.
    Queries are only constructed and run when needed, so they
    can be efficient.
    """

    _filters = ['name']
    _key = 'name'
    _instance_class = Publisher

    def __init__(self, data_path, metadata_path, **kwargs):
        super(PublisherSet, self).__init__()
        self.wheres = kwargs
        self.data_path = data_path
        self.metadata_path = metadata_path

    def __iter__(self):
        data_paths = sorted(glob(self.data_path))
        metadata_paths = sorted(glob(join(self.metadata_path, '')))
        metadata_filepaths = sorted(glob(join(self.metadata_path + '.json')))
        paths = zip(data_paths, metadata_paths, metadata_filepaths)

        name = self.wheres.get('name')
        if name is not None:
            paths = filter(lambda x: basename(x[0]) == name,
                           paths)

        for data_path, metadata_path, metadata_filepath in paths:
            yield Publisher(data_path, metadata_path, metadata_filepath)
