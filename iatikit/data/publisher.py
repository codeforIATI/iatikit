import json
import logging
from os.path import basename, exists, join, split, splitext
from glob import glob
import webbrowser

from past.builtins import basestring

from ..utils.abstract import GenericSet
from .dataset import DatasetSet
from .activity import ActivitySet
from .organisation import OrganisationSet


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
        if isinstance(self.data_path, basestring):
            return split(self.data_path)[1]
        elif isinstance(self.metadata_path, basestring):
            return split(self.metadata_path)[1]
        else:
            return 'publisher'

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, self.name)

    def show(self):
        """Open a new browser tab to the iatiregistry.org page
        for this publisher.
        """
        name = self.metadata.get('name')
        if name:
            url = 'https://iatiregistry.org/publisher/{}'.format(name)
            webbrowser.open_new_tab(url)
            return True
        logging.warning('Can\'t show publisher - metadata missing.')
        return False

    @property
    def datasets(self):
        """Return an iterator of all datasets for this publisher."""
        data_path = join(self.data_path, '*') \
            if self.data_path else None
        metadata_path = join(self.metadata_path, '*') \
            if self.metadata_path else None
        return DatasetSet(data_path, metadata_path)

    @property
    def activities(self):
        """Return an iterator of all activities for this publisher."""
        return ActivitySet(self.datasets)

    @property
    def organisations(self):
        """Return an iterator of all organisations for this publisher."""
        return OrganisationSet(self.datasets)

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
        super(PublisherSet, self).__init__(**kwargs)
        self.data_path = data_path
        self.metadata_path = metadata_path

    def __iter__(self):
        data_paths = {basename(x): x
                      for x in glob(self.data_path)
                      if not x.endswith('.json')}
        metadata_paths = {basename(x): x
                          for x in glob(self.metadata_path)
                          if not x.endswith('.json')}
        metadata_filepaths = {splitext(basename(x))[0]: x
                              for x in glob(self.metadata_path + '.json')}
        paths = {x: (data_paths.get(x),
                     metadata_paths.get(x),
                     metadata_filepaths.get(x))
                 for x in set(list(data_paths.keys()) +
                              list(metadata_paths.keys()) +
                              list(metadata_filepaths.keys()))}

        where_name = self.wheres.get('name')
        if where_name is not None:
            paths = [paths[where_name]] if where_name in paths else []
        else:
            paths = sorted(list(paths.values()))

        for data_path, metadata_path, metadata_filepath in paths:
            yield Publisher(data_path, metadata_path, metadata_filepath)
