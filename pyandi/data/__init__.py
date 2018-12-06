from os.path import join

from .registry import Registry
from .dataset import DatasetSet


def publishers():
    return Registry().publishers()


def datasets():
    r = Registry().publishers()
    data_path = join(r.data_path, '*')
    metadata_path = join(r.data_path, '*')
    return DatasetSet(data_path, metadata_path)
