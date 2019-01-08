from os.path import basename, exists, splitext
from glob import glob
import json
import logging
import webbrowser

from lxml import etree as ET

from ..utils.abstract import GenericSet
from ..utils.exceptions import SchemaNotFoundError
from ..standard.xsd_schema import XSDSchema
from .activity import ActivitySet


class DatasetSet(GenericSet):
    """Class representing a grouping of ``Dataset`` objects.

    Objects in this grouping can be filtered and iterated over.
    Queries are only constructed and run when needed, so they
    can be efficient.
    """

    def __init__(self, data_path, metadata_path, **kwargs):
        super(DatasetSet, self).__init__()
        self._key = 'name'
        self._filters = ['name', 'filetype']
        self._wheres = kwargs
        self._instance_class = Dataset

        self.data_path = data_path
        self.metadata_path = metadata_path

    def __iter__(self):
        data_paths = sorted(glob(self.data_path))
        metadata_paths = sorted(glob(self.metadata_path))
        paths = zip(data_paths, metadata_paths)

        name = self._wheres.get('name')
        if name is not None:
            paths = filter(
                lambda x: splitext(basename(x[0]))[0] == name, paths)

        where_filetype = self._wheres.get('filetype')

        for data_path, metadata_path in paths:
            dataset = Dataset(data_path, metadata_path)
            if where_filetype is not None and \
                    dataset.filetype != where_filetype:
                continue
            yield dataset


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

    @property
    def name(self):
        """Return the name of this dataset, derived from the filename."""
        return splitext(basename(self.data_path))[0]

    @property
    def etree(self):
        """Return the XML of this dataset, as an lxml element tree."""
        if not self._etree:
            try:
                self._etree = ET.parse(self.data_path)
            except ET.XMLSyntaxError:
                logging.warning('Dataset "{}" XML is invalid'.format(
                    self.name))
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

    def get_schema(self):
        """Get the XSD Schema for this dataset."""
        return XSDSchema(self.filetype, self.version)

    def is_valid_xml(self):
        """Check whether the XML in this dataset can be parsed."""
        try:
            if self.etree:
                return True
        except ET.XMLSyntaxError:
            pass
        return False

    def is_valid_iati(self):
        """Validate dataset against the relevant IATI schema."""
        if not self.is_valid_xml():
            return False
        try:
            return self.get_schema().validate(self)
        except SchemaNotFoundError as e:
            logging.warning(e)
            return False

    @property
    def metadata(self):
        """Return a dictionary of registry metadata for this dataset."""
        if self._metadata is None:
            if self.metadata_path is not None and exists(self.metadata_path):
                with open(self.metadata_path) as f:
                    self._metadata = json.load(f)
                extras = self.metadata.get('extras')
                self._metadata['extras'] = {x['key']: x['value']
                                            for x in extras}
            else:
                msg = 'No metadata was found for dataset "{}"'
                logging.warning(msg.format(self.name))
                self._metadata = {}
        return self._metadata

    @property
    def filetype(self):
        """Return the filetype according to the metadata
        (i.e. "activity" or "organisation").

        If it can't be found in the metadata, revert to using
        the XML root node.

        Return ``None`` if the filetype can't be determined.
        """
        try:
            return self.metadata.get('extras').get('filetype')
        except AttributeError:
            pass
        return {
            'iati-activities': 'activity',
            'iati-organisations': 'organisation',
        }.get(self.root)

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
