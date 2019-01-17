from os.path import basename, exists, splitext
from glob import glob
import json
import logging
import webbrowser

from lxml import etree as ET

from ..utils.abstract import GenericSet
from ..utils.exceptions import SchemaNotFoundError, MappingsNotFoundError
from ..utils.validator import Validator, ValidationError
from ..standard.xsd_schema import XSDSchema
from ..standard.codelist_mappings import CodelistMappings
from .activity import ActivitySet


class Dataset(object):
    """Class representing an IATI dataset."""

    def __init__(self, data_path, metadata_path=None):
        """Construct a new Dataset object.

        The file locations of the data and metadata must be specified with
        the ``data_path`` and ``metadata_path`` arguments.
        """
        self.data_path = data_path
        self.metadata_path = metadata_path
        self._etree = None
        self._metadata = None
        self._schema = None

    @property
    def name(self):
        """Return the name of this dataset, derived from the filename."""
        return splitext(basename(self.data_path))[0]

    @property
    def etree(self):
        """Return the XML of this dataset, as an lxml element tree."""
        try:
            self.validate_xml()
        except ET.XMLSyntaxError:
            logging.warning('Dataset "%s" XML is invalid', self.name)
            raise
        return self._etree

    @property
    def xml(self):
        """Return the raw XML of this dataset, as a byte-string."""
        return bytes(ET.tostring(self.etree))

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, self.name)

    def show(self):
        """Open a new browser tab to the iatiregistry.org page
        for this dataset.
        """
        url = 'https://iatiregistry.org/dataset/{}'.format(
            self.name)
        webbrowser.open_new_tab(url)

    @property
    def schema(self):
        """Get the XSD Schema for this dataset."""
        if not self._schema:
            self._schema = XSDSchema(self.filetype, self.version)
        return self._schema

    def validate_xml(self):
        """Check whether the XML in this dataset can be parsed."""
        if not self._etree:
            try:
                self._etree = ET.parse(self.data_path)
            except ET.XMLSyntaxError as error:
                return Validator(False, [ValidationError(str(error))])
        return Validator(True)

    def validate_iati(self):
        """Validate dataset against the relevant IATI schema."""
        xml_valid = self.validate_xml()
        if not xml_valid:
            msg = 'Can\'t perform IATI schema validation for ' + \
                  'invalid XML.'
            return Validator(False, [ValidationError(msg)])
        try:
            return self.schema.validate(self)
        except SchemaNotFoundError as error:
            logging.warning(error)
            return Validator(False, [ValidationError(str(error))])

    def validate_codelists(self):
        """Validate dataset against the relevant IATI codelists."""
        xml_valid = self.validate_xml()
        if not xml_valid:
            msg = 'Can\'t perform codelist validation for ' + \
                  'invalid XML.'
            return Validator(False, [ValidationError(msg)])
        try:
            mappings = CodelistMappings(self.filetype, self.version)
        except MappingsNotFoundError:
            msg = 'Can\'t perform codelist validation for ' + \
                  'IATI version %s datasets.'
            logging.warning(msg, self.version)
            return Validator(True)
        return mappings.validate(self)

    @property
    def metadata(self):
        """Return a dictionary of registry metadata for this dataset."""
        if self._metadata is None:
            if self.metadata_path is not None and exists(self.metadata_path):
                with open(self.metadata_path) as handler:
                    self._metadata = json.load(handler)
                extras = self.metadata.get('extras')
                self._metadata['extras'] = {x['key']: x['value']
                                            for x in extras}
            else:
                msg = 'No metadata was found for dataset "%s"'
                logging.warning(msg, self.name)
                self._metadata = {}
        return self._metadata

    @property
    def filetype(self):
        """Return the filetype according to the metadata
        (i.e. "activity" or "organisation").

        If it can't be found in the metadata, revert to using
        the XML root node.

        Returns '[Invalid filetype]' if the filetype can't be determined.
        """
        try:
            filetype = self.metadata['extras']['filetype']
            if filetype in ['activity', 'organisation']:
                return filetype
        except KeyError:
            pass

        try:
            return {
                'iati-activities': 'activity',
                'iati-organisations': 'organisation',
            }[self.root]
        except KeyError:
            pass

        return '[Invalid filetype]'

    @property
    def root(self):
        """Return the name of the XML root node."""
        return self.etree.getroot().tag

    @property
    def version(self):
        """Return the IATI version according to the XML root node.

        Return "1.01" if the version can't be determined.
        """
        try:
            version = self.etree.getroot().get('version')
            if version is not None:
                return version
        except ET.XMLSyntaxError:
            pass

        logging.warning('@version attribute is not declared. Assuming "1.01".')
        # default version
        return '1.01'

    @property
    def activities(self):
        """Return an iterator of all activities in this dataset."""
        return ActivitySet([self])


class DatasetSet(GenericSet):
    """Class representing a grouping of ``Dataset`` objects.

    Objects in this grouping can be filtered and iterated over.
    Queries are only constructed and run when needed, so they
    can be efficient.
    """

    _key = 'name'
    _filters = ['name', 'filetype']
    _instance_class = Dataset

    def __init__(self, data_path, metadata_path, **kwargs):
        super(DatasetSet, self).__init__()
        self.wheres = kwargs

        self.data_path = data_path
        self.metadata_path = metadata_path

    def __iter__(self):
        data_paths = sorted(glob(self.data_path))
        metadata_paths = sorted(glob(self.metadata_path))
        paths = zip(data_paths, metadata_paths)

        name = self.wheres.get('name')
        if name is not None:
            paths = filter(
                lambda x: splitext(basename(x[0]))[0] == name, paths)

        where_filetype = self.wheres.get('filetype')

        for data_path, metadata_path in paths:
            dataset = Dataset(data_path, metadata_path)
            if where_filetype is not None and \
                    dataset.filetype != where_filetype:
                continue
            yield dataset
