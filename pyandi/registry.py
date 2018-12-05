from glob import glob
from os.path import basename, join

from .models import Publisher


class PyandiSet:
    def where(self, **kwargs):
        wheres = dict(self._wheres, **kwargs)
        return self.__class__(self._basepath, **wheres)

    def first(self):
        for first in self:
            return first

    def all(self):
        return list(iter(self))

    def find(self, **kwargs):
        return self.where(**kwargs).first()


class PublisherSet(PyandiSet):
    def __init__(self, basepath, **kwargs):
        self._basepath = basepath
        self._wheres = kwargs

    def __len__(self):
        return len(list(iter(self)))

    def __iter__(self):
        paths = glob(join(self._basepath, '*'))

        where_name = self._wheres.get('name')
        if where_name:
            paths = filter(lambda x: basename(x) == where_name, paths)

        for path in paths:
            name = basename(path)
            yield Publisher(path, name)


class Registry:
    def __init__(self):
        self.path = join('__pyandicache__', 'data')

    @property
    def publishers(self):
        return PublisherSet(self.path)


def publishers():
    return Registry().publishers
