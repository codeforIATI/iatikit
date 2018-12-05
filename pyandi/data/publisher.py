from os.path import basename, join
from glob import glob

from ..abstract import PyandiSet
from .dataset import DatasetSet
from .activity import ActivitySet


class PublisherSet(PyandiSet):
    def __init__(self, path, **kwargs):
        self._path = path
        self._wheres = kwargs

    def __iter__(self):
        data_paths = glob(join(self._path, 'data', '*'))
        metadata_paths = glob(join(self._path, 'metadata', '*'))
        paths = zip(data_paths, metadata_paths)

        where_name = self._wheres.get('name')
        if where_name:
            paths = filter(lambda x: basename(x[0]) == where_name,
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
        return DatasetSet(self.data_path, self.metadata_path)

    @property
    def activities(self):
        return ActivitySet(self.datasets)
