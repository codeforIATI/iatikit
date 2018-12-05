from os.path import basename, join
from glob import glob

from .abstract import PyandiSet
from .dataset import DatasetSet
from .activity import ActivitySet


class PublisherSet(PyandiSet):
    def __init__(self, basepath, **kwargs):
        self._basepath = basepath
        self._wheres = kwargs

    def __iter__(self):
        paths = glob(join(self._basepath, '*'))

        where_name = self._wheres.get('name')
        if where_name:
            paths = filter(lambda x: basename(x) == where_name, paths)

        for path in paths:
            name = basename(path)
            yield Publisher(path, name)


class Publisher:
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, self.name)

    @property
    def datasets(self):
        return DatasetSet(self.path)

    @property
    def activities(self):
        return ActivitySet(self.datasets)
