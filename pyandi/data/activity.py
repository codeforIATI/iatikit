import webbrowser

from ..standard import get_schema
from ..utils.abstract import GenericSet
from ..utils.querybuilder import QueryBuilder

from lxml import etree as ET


class ActivitySet(GenericSet):
    def __init__(self, datasets, **kwargs):
        super(ActivitySet, self).__init__()
        self._key = 'iati_identifier'
        self._filters = [
            'iati_identifier', 'title', 'description',
            'location', 'sector', 'planned_start',
            'actual_start', 'planned_end', 'actual_end',
        ]
        self._wheres = kwargs
        self._instance_class = Activity

        self.datasets = datasets
        self._filetype = 'activity'
        self._element = 'iati-activity'

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
            total += int(dataset.etree.xpath(query))
        return total

    def _query(self, schema):
        prefix = '//' + self._element
        return QueryBuilder(
            schema,
            prefix=prefix,
        ).where(**self._wheres)

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
            activity_etrees = dataset.etree.xpath(self._query(schema))
            for tree in activity_etrees:
                yield self._instance_class(tree, dataset, schema)


class Activity(object):
    def __init__(self, etree, dataset=None, schema=None):
        self.etree = etree
        self.dataset = dataset
        self._schema = schema
        self.version = self.schema.version

    def __repr__(self):
        id_ = self.iati_identifier
        id_ = id_ if id_ else '[No identifier]'
        return '<{} ({})>'.format(self.__class__.__name__, id_)

    def show(self):
        url = 'http://d-portal.org/q.html?aid={}'.format(self.iati_identifier)
        webbrowser.open_new_tab(url)

    @property
    def schema(self):
        if not self._schema:
            # TODO: Add a schema guesser,
            # based on the activity XML
            pass
        return self._schema

    @property
    def xml(self):
        return ET.tostring(self.etree)

    @property
    def iati_identifier(self):
        id_ = self.schema.iati_identifier().run(self.etree)
        if len(id_) > 0:
            return id_[0].strip()
        return None

    @property
    def title(self):
        return self.schema.title().run(self.etree)

    @property
    def description(self):
        return self.schema.description().run(self.etree)

    @property
    def location(self):
        return self.schema.location().run(self.etree)

    @property
    def sector(self):
        return self.schema.sector().run(self.etree)

    @property
    def planned_start(self):
        date = self.schema.planned_start().run(self.etree)
        return date[0] if len(date) > 0 else None

    @property
    def actual_start(self):
        date = self.schema.actual_start().run(self.etree)
        return date[0] if len(date) > 0 else None

    @property
    def planned_end(self):
        date = self.schema.planned_end().run(self.etree)
        return date[0] if len(date) > 0 else None

    @property
    def actual_end(self):
        date = self.schema.actual_end().run(self.etree)
        return date[0] if len(date) > 0 else None

    @property
    def start(self):
        start = self.actual_start
        if start:
            return start
        return self.planned_start

    @property
    def end(self):
        end = self.actual_end
        if end:
            return end
        return self.planned_end
