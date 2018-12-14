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
        metadata_paths = sorted(glob(self.metadata_path))
        paths = zip(data_paths, metadata_paths)

        name = self._wheres.get('name')
        if name is not None:
            paths = filter(lambda x: basename(x[0]) == name,
                           paths)

        for data_path, metadata_path in paths:
            yield Publisher(data_path, metadata_path)


class Publisher:
    def __init__(self, data_path, metadata_path):
        self.data_path = data_path
        self.metadata_path = metadata_path

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
