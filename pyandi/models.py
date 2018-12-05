import json
from glob import glob
from os.path import basename, join, splitext

from lxml import etree

from .schemas import ActivitySchema
from .querybuilder import QueryBuilder


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


class ActivitySet():
    def __init__(self, datasets, **kwargs):
        self.datasets = datasets
        self.wheres = kwargs

    def where(self, **kwargs):
        wheres = dict(self.wheres, **kwargs)
        return ActivitySet(self.datasets, **wheres)

    def __iter__(self):
        for dataset in self.datasets:
            if not dataset.is_valid():
                continue
            schema = ActivitySchema(dataset.version)
            query = '//iati-activity'
            query += QueryBuilder(schema).where(**self.wheres)
            activities = dataset.xml.xpath(query)
            for activity in activities:
                yield Activity(activity, dataset)

    def __len__(self):
        return self.count()

    def count(self):
        # TODO
        total = 0
        for dataset in self.datasets:
            schema = ActivitySchema(dataset.version)
            query = '//iati-activity'
            query += QueryBuilder(schema).where(**self.wheres)
            query = 'count({})'.format(query)
            total += dataset.xml.xpath(query)
        return int(total)

    def first(self):
        for first in self:
            return first

    def all(self):
        return list(iter(self))

    def find(self, **kwargs):
        # TODO
        pass


class Activity:
    def __init__(self, xml, dataset):
        self.version = dataset.version
        # self.schema = ActivitySchema(self.version)
        self.xml = xml
        self.default_currency = self.xml.get('default-currency')
        self._dataset = dataset

    @property
    def iati_identifier(self):
        x = self.xml.xpath('iati-identifier/text()')
        if len(x) == 1:
            return x[0]
        return None


class DatasetSet:
    def __init__(self, basepath, **kwargs):
        self._basepath = basepath
        self._wheres = kwargs

    def where(self, **kwargs):
        wheres = dict(self._wheres, **kwargs)
        return DatasetSet(self._basepath, **wheres)

    def __len__(self):
        return len(list(iter(self)))

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
            try:
                yield Dataset(path, name)
            except etree.XMLSyntaxError:
                continue

    def first(self):
        for first in self:
            return first

    def all(self):
        return list(iter(self))

    def find(self, **kwargs):
        return self.where(**kwargs).first()
