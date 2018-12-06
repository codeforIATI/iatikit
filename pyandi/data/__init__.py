from os.path import join

from .registry import Registry
from .dataset import DatasetSet
from .activity import ActivitySet


def publishers():
    return Registry().publishers()


def datasets():
    r = Registry().publishers()
    data_path = join(r.data_path, '*')
    metadata_path = join(r.data_path, '*')
    return DatasetSet(data_path, metadata_path)


def activities():
    r = Registry().publishers()
    data_path = join(r.data_path, '*')
    metadata_path = join(r.data_path, '*')
    return ActivitySet(DatasetSet(data_path, metadata_path))
