import json
from os.path import basename, join
from glob import glob

from ..utils.abstract import GenericSet
from .dataset import DatasetSet
from .activity import ActivitySet


class PublisherSet(GenericSet):
    def __init__(self, data_path, metadata_path, **kwargs):
        super().__init__()
        self._wheres = kwargs
        self._filters = ['name']
        self._key = 'name'
        self.data_path = data_path
        self.metadata_path = metadata_path

    def __iter__(self):
        data_paths = sorted(glob(self.data_path))
        metadata_paths = sorted(glob(join(self.metadata_path, '')))
        metadata_filepaths = sorted(glob(join(self.metadata_path + '.json')))
        paths = zip(data_paths, metadata_paths, metadata_filepaths)

        name = self._wheres.get('name')
        if name is not None:
            paths = filter(lambda x: basename(x[0]) == name,
                           paths)

        for data_path, metadata_path, metadata_filepath in paths:
            yield Publisher(data_path, metadata_path, metadata_filepath)


class Publisher:
    def __init__(self, data_path, metadata_path, metadata_filepath):
        self.data_path = data_path
        self.metadata_path = metadata_path
        self.metadata_filepath = metadata_filepath
        self._metadata = None

    @property
    def name(self):
        return basename(self.data_path)

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, self.name)

    @property
    def datasets(self):
        data_path = join(self.data_path, '*')
        metadata_path = join(self.metadata_path, '*')
        return DatasetSet(data_path, metadata_path)

    @property
    def activities(self):
        return ActivitySet(self.datasets)

    @property
    def metadata(self):
        if not self._metadata:
            with open(self.metadata_filepath) as f:
                self._metadata = json.load(f)
        return self._metadata
