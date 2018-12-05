from .abstract import PyandiSet
from .schemas import ActivitySchema
from .querybuilder import QueryBuilder


class ActivitySet(PyandiSet):
    def __init__(self, datasets, **kwargs):
        self.datasets = datasets
        self.wheres = kwargs

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
        # TODO
        total = 0
        for dataset in self.datasets:
            schema = ActivitySchema(dataset.version)
            query = '//iati-activity'
            query += QueryBuilder(schema).where(**self.wheres)
            query = 'count({})'.format(query)
            total += dataset.xml.xpath(query)
        return int(total)


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
