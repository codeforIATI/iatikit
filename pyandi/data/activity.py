from ..standard import get_schema
from ..utils.abstract import GenericSet
from ..utils.querybuilder import QueryBuilder

from lxml import etree


class ActivitySet(GenericSet):
    def __init__(self, datasets, **kwargs):
        self.datasets = datasets
        self._wheres = kwargs
        self._filetype = 'activity'
        self._element = 'iati-activity'
        self._instance_class = Activity

    def __len__(self):
        total = 0
        for dataset in self.datasets:
            if dataset.filetype != self._filetype:
                continue
            if not dataset.is_valid():
                continue
            try:
                schema = get_schema(dataset.filetype, dataset.version)
            except:
                continue
            prefix = '//' + self._element
            query = QueryBuilder(
                schema,
                prefix=prefix,
                count=True
            ).where(**self._wheres)
            total += int(dataset.xml.xpath(query))
        return total

    def __iter__(self):
        for dataset in self.datasets:
            if dataset.filetype != self._filetype:
                continue
            if not dataset.is_valid():
                continue
            try:
                schema = get_schema(dataset.filetype, dataset.version)
            except:
                continue
            prefix = '//' + self._element
            query = QueryBuilder(
                schema,
                prefix=prefix,
            ).where(**self._wheres)
            activities_xml = dataset.xml.xpath(query)
            for xml in activities_xml:
                yield self._instance_class(xml, dataset, schema)


class Activity:
    def __init__(self, xml, dataset, schema):
        self.version = dataset.version
        self.xml = xml
        self.dataset = dataset
        self.schema = schema

    def __repr__(self):
        id_ = self.iati_identifier()
        id_ = id_[0].strip() if len(id_) > 0 else '[No identifier]'
        return '<{} ({})>'.format(self.__class__.__name__, id_)

    @property
    def raw_xml(self):
        return etree.tostring(self.xml)

    def __getattr__(self, attr):
        if not hasattr(self.schema, attr):
            raise AttributeError(attr)

        def wrapper(*args, **kwargs):
            typeobj = getattr(self.schema, attr)()
            return typeobj.exec(self.xml, *args, **kwargs)
        return wrapper
