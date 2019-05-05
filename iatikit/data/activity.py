import webbrowser
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from lxml import etree as ET

from ..standard.schema import get_schema
from ..standard.xsd_schema import XSDSchema
from ..utils.abstract import GenericSet
from ..utils.exceptions import SchemaError
from ..utils.querybuilder import XPathQueryBuilder


class Activity(object):
    """Class representing an IATI activity."""

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
        """Open a new browser tab to the d-portal.org page
        for this dataset.
        """
        params = {'aid': self.iati_identifier}
        url = 'http://d-portal.org/q.html?{}'.format(urlencode(params))
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
        """Return the raw XML of this activity, as a byte-string."""
        return bytes(ET.tostring(self.etree, pretty_print=True))

    @property
    def iati_identifier(self):
        """Return the iati-identifier for this activity,
        or ``None`` if it isn't provided.
        """
        id_ = self.schema.iati_identifier().run(self.etree)
        if id_:
            return id_[0].strip()
        return None

    def validate_iati(self):
        etree = ET.Element('iati-activities')
        etree.set('version', self.version)
        etree.append(self.etree)
        xsd_schema = XSDSchema('activity', self.version)
        return xsd_schema.validate(etree)

    @property
    def id(self):  # pylint: disable=invalid-name
        """Alias of ``iati_identifier``."""
        return self.iati_identifier

    @property
    def title(self):
        """Return a list of titles for this activity."""
        return self.schema.title().run(self.etree)

    @property
    def description(self):
        """Return a list of descriptions for this activity."""
        return self.schema.description().run(self.etree)

    @property
    def location(self):
        """Return a list of locations for this activity."""
        return self.schema.location().run(self.etree)

    @property
    def sector(self):
        """Return a list of sectors for this activity."""
        return self.schema.sector().run(self.etree)

    @property
    def humanitarian(self):
        """Return a list of sectors for this activity."""
        return self.schema.humanitarian().run(self.etree)

    @property
    def planned_start(self):
        """Return the planned start date for this activity,
        as a python ``date``.
        """
        date = self.schema.planned_start().run(self.etree)
        return date[0] if date else None

    @property
    def actual_start(self):
        """Return the actual start date for this activity,
        as a python ``date``.
        """
        date = self.schema.actual_start().run(self.etree)
        return date[0] if date else None

    @property
    def start(self):
        """Return the actual start date for this activity,
        if present. Otherwise, return the planned start.
        """
        start = self.actual_start
        if start:
            return start
        return self.planned_start

    @property
    def planned_end(self):
        """Return the planned end date for this activity,
        as a python ``date``.
        """
        date = self.schema.planned_end().run(self.etree)
        return date[0] if date else None

    @property
    def actual_end(self):
        """Return the actual end date for this activity,
        as a python ``date``.
        """
        date = self.schema.actual_end().run(self.etree)
        return date[0] if date else None

    @property
    def end(self):
        """Return the actual end date for this activity,
        if present. Otherwise, return the planned end.
        """
        end = self.actual_end
        if end:
            return end
        return self.planned_end


class ActivitySet(GenericSet):
    """Class representing a grouping of ``Activity`` objects.

    Objects in this grouping can be filtered and iterated over.
    Queries are only constructed and run when needed, so they
    can be efficient.
    """

    _key = 'iati_identifier'
    _multi_filters = [
        'id', 'iati_identifier', 'title', 'description',
        'location', 'sector', 'planned_start',
        'actual_start', 'planned_end', 'actual_end',
        'xpath', 'humanitarian',
    ]
    _instance_class = Activity
    _filetype = 'activity'
    _element = '/iati-activities/iati-activity'

    def __init__(self, datasets, **kwargs):
        super(ActivitySet, self).__init__()
        self.wheres = kwargs
        self.datasets = datasets

    def __len__(self):
        total = 0
        for dataset in self.datasets:
            if dataset.filetype != self._filetype:
                continue
            if not dataset.validate_xml():
                continue
            try:
                schema = get_schema(dataset.filetype, dataset.version)
            except SchemaError:
                continue
            prefix = self._element
            query = XPathQueryBuilder(
                schema,
                prefix=prefix,
                count=True
            ).where(**self.wheres)
            total += int(dataset.etree.xpath(query))
        return total

    def _query(self, schema=None):
        if schema is None:
            schema = get_schema(self._filetype, '2.03')
        return XPathQueryBuilder(
            schema,
            prefix=self._element,
        ).where(**self.wheres)

    def __iter__(self):
        for dataset in self.datasets:
            if dataset.filetype != self._filetype:
                continue
            if not dataset.validate_xml():
                continue
            try:
                schema = get_schema(dataset.filetype, dataset.version)
            except SchemaError:
                continue
            activity_etrees = dataset.etree.xpath(self._query(schema))
            for tree in activity_etrees:
                yield self._instance_class(tree, dataset, schema)
