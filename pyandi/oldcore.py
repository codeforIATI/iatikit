from glob import glob
import json
import logging
from os.path import join

from lxml import etree

from .querybuilder import QueryBuilder
from .types import DateType, NarrativeType, StringType


class Transaction:
    def __init__(self, xml, activity):
        self.version = activity.version
        self.xml = xml
        self.default_currency = activity.default_currency
        self._activity = activity

    # def __add__(self, other):
    #     if type(other) != Transaction:
    #         other_type = str(type(other))
    #         raise Exception('Can\'t add Transaction and {}'.format(other_type))
    #     new_val = dict(self.value)
    #     for k, v in other.value.items():
    #         new_val[k] = v + new_val.get(k, 0.)
    #     return Transaction(
    #         type_=self.type_,
    #         value=new_val,
    #         date=self.date,
    #     )

    # __radd__ = __add__

    def get_transactions(self, type_):
        if type_ == 'commitments':
            expr = 'transaction[transaction-type/@code="2" or ' + \
                   'transaction-type/@code="C"]'
        elif type_ == 'disbursements':
            expr = 'transaction[transaction-type/@code="3" or ' + \
                   'transaction-type/@code="D"]'
        elif type_ == 'expenditures':
            expr = 'transaction[transaction-type/@code="4" or ' + \
                   'transaction-type/@code="E"]'
        trans = self.xml.xpath(expr)
        transactions = []
        for t in trans:
            try:
                value = t.xpath('value')[0]
                amount = float(value.text)
            except IndexError:
                continue
            except TypeError:
                continue
            transaction = Transaction(
                type_=type_,
                amount=amount,
                currency=value.get('currency', self.default_currency),
                date=value.get('value-date'),
                xml=t,
            )
            transactions.append(transaction)
        return transactions

    def __getattr__(self, attr):
        query = QueryBuilder(self.version).get(attr)
        return self.xml.xpath(query)


class Organisation:
    def __init__(self, xml, dataset=None):
        self.xml = xml
        self._logger = logging.getLogger('pwyf')
        self._dataset = dataset


class Activity:
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
        # if attr in ['_planned_start', '_actual_start',
        #             '_planned_end', '_actual_end']:
        #     return DateType(self._version, attr)
        query = QueryBuilder(self).get(attr)
        return self.xml.xpath(query)

    @property
    def transactions(self):
        return TransactionSet(self)

    # def related_activities(self, **kwargs):
    #     related_acts = self.xml.xpath('related-activity')
    #     for k, v in kwargs.items():
    #         related_acts = filter(lambda x: x.get(k) == v, related_acts)
    #     return list(related_acts)

    @property
    def _hierarchy_query(self):
        return StringType('@hierarchy')

    @property
    def _iati_identifier_query(self):
        return StringType('iati-identifier/text()')

    @property
    def _transaction_sector_query(self):
        return StringType('transaction/sector/@code')

    @property
    def _org_role_query(self):
        return StringType('participating-org/@role')

    @property
    def _org_ref_query(self):
        return StringType('participating-org/@ref')

    @property
    def _location_query(self):
        return StringType('location')

    @property
    def _title_query(self):
        return NarrativeType(self._version, 'title')

    @property
    def _sector_query(self):
        return StringType('sector/@code')


class Publisher:
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


class CodelistItem:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return '{name} ({code})'.format(name=self.name, code=self.code)


class Codelist:
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


class TransactionSet:
    def __init__(self, activity, **kwargs):
        self.activity = activity
        self.wheres = kwargs

    def where(self, **kwargs):
        wheres = dict(self.wheres, **kwargs)
        return TransactionSet(self.datasets, **wheres)

    def __len__(self):
        return self.count()

    def __iter__(self):
        query = 'transaction'
        query += QueryBuilder(self.activity.version).where(**self.wheres)
        transactions = self.activity.xml.xpath(query)
        for transaction in transactions:
            yield Transaction(transaction, self.activity)

    def count(self):
        query = 'transaction'
        query += QueryBuilder(self.activity.version).where(**self.wheres)
        query = 'count({})'.format(query)
        return self.activity.xml.xpath(query)


class ActivitySet:
    def __init__(self, datasets, **kwargs):
        self.datasets = datasets
        self.wheres = kwargs

    def where(self, **kwargs):
        wheres = dict(self.wheres, **kwargs)
        return ActivitySet(self.datasets, wheres)

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
