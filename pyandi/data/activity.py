from ..abstract import PyandiSet
from ..standard.schema import ActivitySchema
from ..querybuilder import QueryBuilder

from lxml import etree


class ActivitySet(PyandiSet):
    def __init__(self, datasets, **kwargs):
        self.datasets = datasets
        self.wheres = kwargs
        self._filetype = 'activity'

    def __len__(self):
        total = 0
        for dataset in self.datasets:
            if dataset.filetype != self._filetype:
                continue
            if not dataset.is_valid():
                continue
            schema = ActivitySchema(dataset.version)
            query = '//iati-activity'
            query += QueryBuilder(schema).where(**self.wheres)
            total += int(dataset.xml.xpath('count({})'.format(query)))
        return total

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


class Activity:
    def __init__(self, xml, dataset):
        self.version = dataset.version
        # self.schema = ActivitySchema(self.version)
        self.xml = xml
        self.default_currency = self.xml.get('default-currency')
        self._dataset = dataset

    @property
    def raw_xml(self):
        return etree.tostring(self.xml)

    def iati_identifier(self):
        x = self.xml.xpath('iati-identifier/text()')
        if len(x) == 1:
            return x[0]
        return None
