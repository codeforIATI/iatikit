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


class Organisation(object):
    """Class representing an IATI organisation."""

    def __init__(self, etree, dataset=None, schema=None):
        self.etree = etree
        self.dataset = dataset
        self._schema = schema
        self.version = self.schema.version

    def __repr__(self):
        id_ = self.org_identifier
        id_ = id_ if id_ else '[No identifier]'
        return '<{} ({})>'.format(self.__class__.__name__, id_)

    def show(self):
        """Open a new browser tab to the d-portal.org page
        for this organisation.
        """
        params = {'publisher': self.org_identifier}
        url = 'http://d-portal.org/ctrack.html?{}#view=main'.format(
            urlencode(params))
        webbrowser.open_new_tab(url)

    @property
    def schema(self):
        return self._schema

    @property
    def xml(self):
        """Return the raw XML of this organisation, as a byte-string."""
        return bytes(ET.tostring(self.etree, pretty_print=True))

    @property
    def org_identifier(self):
        """Return the org-identifier for this organisation,
        or ``None`` if it isn't provided.
        """
        id_ = self.schema.org_identifier().run(self.etree)
        if id_:
            return id_[0].strip()
        return None

    def validate_iati(self):
        etree = ET.Element('iati-organisations')
        etree.set('version', self.version)
        etree.append(self.etree)
        xsd_schema = XSDSchema('organisation', self.version)
        return xsd_schema.validate(etree)

    @property
    def id(self):  # pylint: disable=invalid-name
        """Alias of ``org_identifier``."""
        return self.org_identifier


class OrganisationSet(GenericSet):
    """Class representing a grouping of ``Organisation`` objects.

    Objects in this grouping can be filtered and iterated over.
    Queries are only constructed and run when needed, so they
    can be efficient.
    """

    _key = 'org_identifier'
    _multi_filters = [
        'id', 'org_identifier', 'xpath',
    ]
    _instance_class = Organisation
    _filetype = 'organisation'
    _element = '/iati-organisations/iati-organisation'

    def __init__(self, datasets, **kwargs):
        super(OrganisationSet, self).__init__()
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
            organisation_etrees = dataset.etree.xpath(self._query(schema))
            for tree in organisation_etrees:
                yield self._instance_class(tree, dataset, schema)
