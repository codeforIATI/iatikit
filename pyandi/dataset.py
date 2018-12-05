from os.path import basename, join, splitext
from glob import glob
import json

from lxml import etree

from .activity import ActivitySet


class DatasetSet:
    def __init__(self, basepath, **kwargs):
        self._basepath = basepath
        self._wheres = kwargs

    def __iter__(self):
        paths = glob(join(self._basepath, '*.xml'))

        where_path = self._wheres.get('path')
        if where_path:
            paths = filter(
                lambda x: x == where_path, paths)
        where_name = self._wheres.get('name')
        if where_name:
            paths = filter(
                lambda x: splitext(basename(x))[0] == where_name, paths)

        for path in paths:
            name = splitext(basename(path))[0]
            yield Dataset(path, name)


class Dataset:
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self._xml = None

    @property
    def xml(self):
        if not self._xml:
            self._xml = etree.parse(self.path)
        return self._xml

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, self.name)

    def __str__(self):
        return self.name

    def is_valid(self):
        if self.filetype:
            return True
        return False

    @property
    def metadata(self):
        with open(splitext(self.path)[0] + '.json') as f:
            return json.load(f)

    @property
    def filetype(self):
        roottag = self.xml.getroot().tag
        if roottag == 'iati-activities':
            return 'activity'
        if roottag == 'iati-organisations':
            return 'organisation'
        return None

    @property
    def version(self):
        query = '//{}/@version'.format(self.filetype)
        v = self.xml.xpath(query)
        if len(v) == 1:
            return v[0]
        return None

    @property
    def activities(self):
        return ActivitySet([self])
