from time import time
from glob import glob
import json
import logging
from os.path import join
from os import unlink, makedirs
import shutil
import zipfile

import requests
from lxml import etree


# class Transaction():
#     def __init__(self, _type, date, amount=None, currency=None,
#                  value=None, xml=None):
#         # TODO: we basically ignore these for now
#         self._type = _type
#         self.date = date
#         self.xml = xml

#         if value:
#             self.value = value
#         else:
#             self.value = {
#                 currency: amount
#             }

#     def __str__(self):
#         return ', '.join(['{} {}'.format(round(y), x)
#                           for x, y in self.value.items()])

#     def __mul__(self, other):
#         if type(other) not in [int, float]:
#             raise Exception('No way')
#         new_val = dict(self.value)
#         for k, v in new_val.items():
#             new_val[k] = v * other
#         return Transaction(
#             type_=self.type_,
#             value=new_val,
#             date=self.date,
#         )

#     def __add__(self, other):
#         if type(other) in [int, float]:
#             return self
#         if type(other) != Transaction:
#             other_type = str(type(other))
#             raise Exception('Can\'t add Transaction and {}'.format(other_type))
#         new_val = dict(self.value)
#         for k, v in other.value.items():
#             new_val[k] = v + new_val.get(k, 0.)
#         return Transaction(
#             type_=self.type_,
#             value=new_val,
#             date=self.date,
#         )

#     __radd__ = __add__
#     __rmul__ = __mul__

#     def uses_sector(self, *sectors):
#         expr = 'sector[@vocabulary="1" or @vocabulary="2"]/@code'
#         codes = self.xml.xpath(expr)
#         for code in codes:
#             if code in sectors:
#                 return True
#         return False


class Organisation():
    def __init__(self, xml, dataset=None):
        self.xml = xml
        self._logger = logging.getLogger('pwyf')
        self._dataset = dataset


class QueryBuilder():
    class ActivityDate:
        def __init__(self, version, datetype):
            self.datetype = datetype
            self._version = version

        def get(self):
            datetype = {
                'planned_start': ('start-planned', 1),
                'actual_start': ('start-actual', 2),
                'planned_end': ('end-planned', 3),
                'actual_end': ('end-actual', 4),
            }.get(self.datetype)
            if self._version.startswith('1'):
                datetype = datetype[0]
            else:
                datetype = datetype[1]
            return 'activity-date[@type="{}"]/@iso-date'.format(datetype)

        def where(self, op, value):
            op = {
                'lt': '<', 'lte': '<=',
                'gt': '>', 'gte': '>=',
                'eq': '=',
            }.get(op)
            if not op:
                raise Exception
            return 'number(translate({expr}, "-", "")) {op} {value}'.format(
                expr=self.get(),
                op=op,
                value=value.replace('-', ''),
            )

    class SimpleString:
        def __init__(self, version, expr):
            self._version = version
            self._expr = expr

        def get(self):
            return self._expr

        def where(self, op, value):
            if op in ['contains', 'startswith']:
                if op == 'startswith':
                    op = 'starts-with'
                return '{expr}[{op}(., "{value}")]'.format(
                    expr=self.get(),
                    op=op,
                    value=value,
                )
            elif op != 'eq':
                raise Exception
            return '{expr} = "{value}"'.format(
                expr=self.get(),
                value=value,
            )

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
        return self.SimpleString(self._version, '@hierarchy')

    @property
    def iati_identifier(self):
        return self.SimpleString(self._version, 'iati-identifier/text()')

    @property
    def transaction_sector(self):
        return self.SimpleString(self._version, 'transaction/sector/@code')

    @property
    def sector(self):
        return self.SimpleString(self._version, 'sector/@code')

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
                yield Activity(activity, dataset.version, dataset)

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

    def all(self):
        return list(iter(self))


class Activity():
    def __init__(self, xml, version, dataset=None):
        self.version = version
        self.xml = xml
        self.default_currency = self.xml.get('default-currency')
        self._logger = logging.getLogger('pwyf')
        self._dataset = dataset

    # @classmethod
    # def from_xml(cls, xml_str):
    #     l = etree.fromstring(xml_str.decode('utf-8'))
    #     return cls(xml=l)

    def __getattr__(self, attr):
        query = QueryBuilder(self.version).get(attr)
        return self.xml.xpath(query)

    # def related_activities(self, **kwargs):
    #     related_acts = self.xml.xpath('related-activity')
    #     for k, v in kwargs.items():
    #         related_acts = filter(lambda x: x.get(k) == v, related_acts)
    #     return list(related_acts)

    # def get_transactions(self, type_):
    #     if type_ == 'commitments':
    #         expr = 'transaction[transaction-type/@code="2" or ' + \
    #                'transaction-type/@code="C"]'
    #     elif type_ == 'disbursements':
    #         expr = 'transaction[transaction-type/@code="3" or ' + \
    #                'transaction-type/@code="D"]'
    #     elif type_ == 'expenditures':
    #         expr = 'transaction[transaction-type/@code="4" or ' + \
    #                'transaction-type/@code="E"]'
    #     trans = self.xml.xpath(expr)
    #     transactions = []
    #     for t in trans:
    #         try:
    #             value = t.xpath('value')[0]
    #             amount = float(value.text)
    #         except IndexError:
    #             continue
    #         except TypeError:
    #             continue
    #         transaction = Transaction(
    #             type_=type_,
    #             amount=amount,
    #             currency=value.get('currency', self.default_currency),
    #             date=value.get('value-date'),
    #             xml=t,
    #         )
    #         transactions.append(transaction)
    #     return transactions


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

    # @classmethod
    # def get(cls, pub_path):
    #     name = pub_path.split('/')[-1]
    #     return cls(name=name, path=pub_path)

    @property
    def datasets(self):
        dataset_paths = glob(join(self.path, '*'))
        return [Dataset(path) for path in dataset_paths]

    @property
    def activities(self):
        return ActivitySet(self.datasets)

    # @property
    # def organisations(self):
    #     xpath_expr = '//iati-organisation'
    #     for dataset in self.datasets:
    #         organisations = dataset.xml.xpath(xpath_expr)
    #         for organisation in organisations:
    #             yield Organisation(organisation, dataset)

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
            path = join('pyandi', 'data')
        pub_paths = glob(join(path, '*'))
        self.publishers = [Publisher(
            name=path.split('/')[-1],
            path=path) for path in pub_paths]

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
        filepath = join('pyandi', 'codelists', version[0], name + '.json')
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


def timer(func):
    def wrapper(*args, **kwargs):
        if not kwargs.get('verbose'):
            return func(*args, **kwargs)
        else:
            start = time()
            out = func(*args, **kwargs)
            end = time()
            print('Done ({:.1f} seconds elapsed.)'.format(end - start))
            return out

    return wrapper


@timer
def refresh_data(**kwargs):
    # downloads from https://andylolz.github.io/iati-data-dump/
    data_url = 'https://www.dropbox.com/s/kkm80yjihyalwes/iati_dump.zip?dl=1'
    data_path = join('pyandi', 'data')
    shutil.rmtree(data_path, ignore_errors=True)
    makedirs(data_path)
    zip_filepath = join(data_path, 'iati_dump.zip')

    print('Downloading...')
    r = requests.get(data_url, stream=True)
    with open(zip_filepath, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    print('Unzipping...')
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(data_path)
    print('Cleaning up...')
    unlink(zip_filepath)


@timer
def refresh_codelists(**kwargs):
    base_tmpl = 'http://reference.iatistandard.org/{version}/' + \
                'codelists/downloads/'
    print('Refreshing codelists...')
    for version in ['105', '201']:
        codelist_path = join('pyandi', 'codelists', version[0])
        shutil.rmtree(codelist_path, ignore_errors=True)
        makedirs(codelist_path)
        codelist_url = base_tmpl.format(version=version) + 'clv1/codelist.json'
        j = requests.get(codelist_url).json()
        codelist_names = [x['name'] for x in j['codelist']]
        for codelist_name in codelist_names:
            codelist_url = base_tmpl.format(version=version) + \
                           'clv2/json/en/{}.json'.format(codelist_name)
            j = requests.get(codelist_url)
            codelist_filepath = join(codelist_path, '{}.json'.format(
                codelist_name))
            with open(codelist_filepath, 'wb') as f:
                f.write(j.content)
