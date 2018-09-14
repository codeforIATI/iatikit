from glob import glob
import json
import logging
from os.path import join

from lxml import etree


class Organisation():
    def __init__(self, xml, dataset=None):
        self.xml = xml
        self._logger = logging.getLogger('pwyf')
        self._dataset = dataset


class QueryBuilder():
    def __init__(self, version):
        self._version = version

    def where(self, **kwargs):
        exprs = []
        for k, value in kwargs.items():
            if '__' in k:
                k, op = k.split('__')
            else:
                op = 'eq'
            expr = getattr(self, k).where(op, value)
            exprs.append(expr)
        return ''.join(['[{}]'.format(x) for x in exprs])

    def get(self, attr):
        return getattr(self, attr).get()

    @property
    def version(self):
        return self._version

    @property
    def hierarchy(self):
        return self.SimpleString('@hierarchy')

    @property
    def iati_identifier(self):
        return self.SimpleString('iati-identifier/text()')

    @property
    def transaction_sector(self):
        return self.SimpleString('transaction/sector/@code')

    @property
    def org_role(self):
        return self.SimpleString('participating-org/@role')

    @property
    def org_ref(self):
        return self.SimpleString('participating-org/@ref')

    @property
    def location(self):
        return self.SimpleString('location')

    @property
    def title(self):
        return self.NarrativeString(self._version, 'title')

    @property
    def sector(self):
        return self.SimpleString('sector/@code')

    def __getattr__(self, attr):
        if attr in ['planned_start', 'actual_start',
                    'planned_end', 'actual_end']:
            return self.ActivityDate(self._version, attr)
        raise AttributeError


class ActivitySet():
    def __init__(self, datasets, **kwargs):
        self.datasets = datasets
        self.wheres = kwargs

    def where(self, **kwargs):
        return ActivitySet(self.datasets, **kwargs)

    def __iter__(self):
        for dataset in self.datasets:
            query = '//iati-activity'
            query += QueryBuilder(dataset.version).where(**self.wheres)
            activities = dataset.xml.xpath(query)
            for activity in activities:
                yield Activity(activity, dataset)

    def __len__(self):
        return self.count()

    def count(self):
        total = 0
        for dataset in self.datasets:
            query = '//iati-activity'
            query += QueryBuilder(dataset.version).where(**self.wheres)
            query = 'count({})'.format(query)
            total += dataset.xml.xpath(query)
        return int(total)

    def first(self):
        for x in self:
            return x

    def all(self):
        return list(iter(self))


class Activity():
    def __init__(self, xml, dataset):
        self.version = dataset.version
        self.xml = xml
        self.default_currency = self.xml.get('default-currency')
        self._logger = logging.getLogger('pwyf')
        self._dataset = dataset

    def __str__(self):
        return '{} ({})'.format(
            self.title[0],
            self.iati_identifier[0])

    def __getattr__(self, attr):
        query = QueryBuilder(self.version).get(attr)
        return self.xml.xpath(query)

    # def related_activities(self, **kwargs):
    #     related_acts = self.xml.xpath('related-activity')
    #     for k, v in kwargs.items():
    #         related_acts = filter(lambda x: x.get(k) == v, related_acts)
    #     return list(related_acts)


class DatasetSet():
    def __init__(self, path):
        dataset_paths = glob(join(path, '*'))
        self.datasets = [Dataset(path) for path in dataset_paths]
        self._path = path

    def __len__(self):
        return len(self.datasets)

    def __iter__(self):
        return iter(self.datasets)


class Dataset():
    def __init__(self, path):
        self._path = path
        self._xml = None

    def __str__(self):
        return self._path

    @property
    def xml(self):
        if not self._xml:
            try:
                self._xml = etree.parse(self._path)
            except etree.XMLSyntaxError:
                print('failed to parse: {}'.format(self._path))
        return self._xml

    @property
    def filetype(self):
        root = self.xml.getroot()
        if root.tag not in ['iati-activities', 'iati-organisations']:
            raise Exception
        return root.tag

    @property
    def version(self):
        query = '//{}/@version'.format(self.filetype)
        return self.xml.xpath(query)[0]

    @property
    def activities(self):
        return ActivitySet([self])


class Publisher():
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.path = kwargs.get('path')
        self._logger = logging.getLogger('pwyf')

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, self.name)

    @property
    def datasets(self):
        return DatasetSet(self.path)

    @property
    def activities(self):
        return ActivitySet(self.datasets)

    def find(self, expr):
        out = []
        for activity in self.activities:
            res = activity.xml.xpath(expr)
            if res != []:
                out.append(res)
        return out


class PublisherSet():
    def __init__(self, path=None):
        if not path:
            path = join('__pyandicache__', 'data')
        pub_paths = glob(join(path, '*'))
        self.publishers = [Publisher(
            name=path.split('/')[-1],
            path=path) for path in pub_paths]

    def __len__(self):
        return len(list(iter(self)))

    def __iter__(self):
        return iter(self.publishers)

    def __getitem__(self, key):
        return self.publishers[key]

    def where(self, **kwargs):
        filtered = self.publishers
        for k, v in kwargs.items():
            filtered = filter(lambda x: getattr(x, k) == v, filtered)
        return list(filtered)

    def find(self, **kwargs):
        return self.where(**kwargs)[0]


class CodelistItem():
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return '{name} ({code})'.format(name=self.name, code=self.code)


class Codelist():
    def __init__(self, name, version='2'):
        filepath = join('__pyandicache__', 'codelists',
                        version[0], name + '.json')
        with open(filepath) as f:
            j = json.load(f)
        for attr_name, attr_val in j['attributes'].items():
            setattr(self, attr_name, attr_val)
        self._data = {x['code']: CodelistItem(**x) for x in j['data']}

    def get(self, value):
        item = self._data.get(value)
        return item

    def startswith(self, value):
        return list(filter(
            lambda x: x.code.startswith(value), self._data.values()))
