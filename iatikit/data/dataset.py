from os.path import basename, exists, splitext
from glob import glob
import json
import logging
import webbrowser

from past.builtins import basestring
from lxml import etree as ET

from ..utils.abstract import GenericSet
from ..utils.exceptions import SchemaNotFoundError, MappingsNotFoundError
from ..utils.validator import Validator, ValidationError
from ..standard.xsd_schema import XSDSchema
from ..standard.codelist_mappings import CodelistMappings
from .activity import ActivitySet
from .organisation import OrganisationSet


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
        if isinstance(self.data_path, basestring):
            return splitext(basename(self.data_path))[0]
        elif isinstance(self.metadata_path, basestring):
            return splitext(basename(self.metadata_path))[0]
        else:
            return 'dataset'

    @property
    def etree(self):
        """Return the XML of this dataset, as an lxml element tree."""
        if not self._etree:
            try:
                parser = ET.XMLParser(remove_blank_text=True, huge_tree=True)
                self._etree = ET.parse(self.data_path, parser)
            except ET.XMLSyntaxError:
                logging.warning('Dataset "%s" XML is invalid', self.name)
                raise
        return self._etree

    @property
    def xml(self):
        """Return the raw XML of this dataset, as a byte-string."""
        return bytes(ET.tostring(self.etree, pretty_print=True))

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, self.name)

    def show(self):
        """Open a new browser tab to the iatiregistry.org page
        for this dataset.
        """
        name = self.metadata.get('name')
        if name:
            url = 'https://iatiregistry.org/dataset/{}'.format(name)
            webbrowser.open_new_tab(url)
            return True
        logging.warning('Can\'t show dataset - metadata missing.')
        return False

    def _get_schema(self):
        """Get the XSD Schema for this dataset. Raise exception on error."""
        if not self._schema:
            self._schema = XSDSchema(self.filetype, self.version)
        return self._schema

    @property
    def schema(self):
        """Get the XSD Schema for this dataset."""
        try:
            return self._get_schema()
        except SchemaNotFoundError as error:
            logging.warning(str(error))

    def unminify_xml(self):
        self._etree = ET.ElementTree(ET.fromstring(self.xml))

    def validate_xml(self):
        """Check whether the XML in this dataset can be parsed."""
        try:
            self.etree
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
            return self._get_schema().validate(self.etree)
        except SchemaNotFoundError as error:
            logging.warning(str(error))
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

        Returns None if the filetype can't be determined.
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

    @property
    def root(self):
        """Return the name of the XML root node."""
        try:
            return self.etree.getroot().tag
        except ET.XMLSyntaxError:
            pass

    @property
    def version(self):
        """Return the IATI version according to the XML root node.

        Return "1.01" if the version can't be determined.
        """
        version = self.etree.getroot().get('version')
        if version is not None:
            return version

        logging.warning('@version attribute is not declared. Assuming "1.01".')
        # default version
        return '1.01'

    @property
    def activities(self):
        """Return an iterator of all activities in this dataset."""
        return ActivitySet([self])

    @property
    def organisations(self):
        """Return an iterator of all organisations in this dataset."""
        return OrganisationSet([self])


class DatasetSet(GenericSet):
    """Class representing a grouping of ``Dataset`` objects.

    Objects in this grouping can be filtered and iterated over.
    Queries are only constructed and run when needed, so they
    can be efficient.
    """

    _key = 'name'
    _filters = ['name', 'filetype']
    _multi_filters = ['xpath']
    _instance_class = Dataset

    def __init__(self, data_path, metadata_path, **kwargs):
        super(DatasetSet, self).__init__(**kwargs)
        self.data_path = data_path
        self.metadata_path = metadata_path

    def __iter__(self):
        data_paths = {
            splitext(basename(x))[0]: x
            for x in glob(self.data_path)
        } if self.data_path else {}
        metadata_paths = {
            splitext(basename(x))[0]: x
            for x in glob(self.metadata_path)
        } if self.metadata_path else {}

        paths = {x: (data_paths.get(x), metadata_paths.get(x))
                 for x in set(list(data_paths.keys()) +
                              list(metadata_paths.keys()))}

        where_name = self.wheres.get('name')
        if where_name is not None:
            paths = [paths[where_name]] if where_name in paths else []
        else:
            paths = sorted(list(paths.values()))

        where_filetype = self.wheres.get('filetype')
        where_xpaths = self.wheres.get('xpath', [])

        for data_path, metadata_path in paths:
            dataset = Dataset(data_path, metadata_path)
            if where_filetype is not None and \
                    dataset.filetype != where_filetype:
                continue
            if where_xpaths != []:
                if not dataset.validate_xml():
                    continue
                for where_xpath in where_xpaths:
                    if dataset.etree.xpath(where_xpath) == []:
                        break
                else:
                    yield dataset
                continue
            yield dataset
