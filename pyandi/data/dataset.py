from os.path import basename, splitext
from glob import glob
import json
import logging
import webbrowser

from lxml import etree as ET

from ..utils.abstract import GenericSet
from .activity import ActivitySet


class DatasetSet(GenericSet):
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
    def __init__(self, data_path, metadata_path):
        self.data_path = data_path
        self.metadata_path = metadata_path
        self._etree = None
        self._metadata = None

    @property
    def name(self):
        return splitext(basename(self.data_path))[0]

    @property
    def etree(self):
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
        return ET.tostring(self.etree)

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, self.name)

    def show(self):
        url = 'https://iatiregistry.org/dataset/{}'.format(
            self.name)
        webbrowser.open_new_tab(url)

    def is_valid(self):
        # TODO: This currently just checks for valid XML
        try:
            if self.etree:
                return True
        except ET.XMLSyntaxError:
            pass
        return False

    @property
    def metadata(self):
        if not self._metadata:
            with open(self.metadata_path) as f:
                self._metadata = json.load(f)
            self._metadata['extras'] = {x['key']: x['value']
                                        for x in self.metadata.get('extras')}
        return self._metadata

    @property
    def filetype(self):
        try:
            return self.metadata.get('extras').get('filetype')
        except FileNotFoundError:
            return {
                'iati-activities': 'activity',
                'iati-organisations': 'organisation',
            }.get(self.root)

    @property
    def root(self):
        return self.etree.getroot().tag

    @property
    def version(self):
        try:
            return self.etree.getroot().get('version')
        except ET.XMLSyntaxError:
            pass
        return None

    @property
    def activities(self):
        return ActivitySet([self])
