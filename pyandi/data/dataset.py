from os.path import basename, splitext
from glob import glob
import json

from lxml import etree

from ..utils.abstract import PyandiSet
from .activity import ActivitySet


class DatasetSet(PyandiSet):
    def __init__(self, data_path, metadata_path, **kwargs):
        self.data_path = data_path
        self.metadata_path = metadata_path
        self._wheres = kwargs

    def __iter__(self):
        data_paths = sorted(glob(self.data_path))
        metadata_paths = sorted(glob(self.metadata_path))
        paths = zip(data_paths, metadata_paths)

        for k, v in self._wheres.items():
            if k == 'name':
                paths = filter(
                    lambda x: splitext(basename(x[0]))[0] == v, paths)

        where_filetype = self._wheres.get('filetype')

        for data_path, metadata_path in paths:
            dataset = Dataset(data_path, metadata_path)
            if where_filetype and dataset.filetype != where_filetype:
                continue
            yield dataset


class Dataset:
    def __init__(self, data_path, metadata_path):
        self.data_path = data_path
        self.metadata_path = metadata_path
        self._xml = None
        self._metadata = None

    @property
    def name(self):
        return splitext(basename(self.data_path))[0]

    @property
    def xml(self):
        if not self._xml:
            self._xml = etree.parse(self.data_path)
        return self._xml

    @property
    def raw_xml(self):
        return etree.tostring(self.xml)

    def __repr__(self):
        return '<{} ({})>'.format(self.__class__.__name__, self.name)

    def is_valid(self):
        # TODO: This currently just checks for valid XML
        try:
            if self.xml:
                return True
        except etree.XMLSyntaxError:
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
        return self.metadata.get('extras').get('filetype')

    @property
    def root(self):
        roottag = self.xml.getroot().tag
        if roottag in ['iati-activities', 'iati-organisations']:
            return roottag
        return None

    @property
    def version(self):
        try:
            return self.xml.getroot().get('version')
        except:
            pass
        return None

    @property
    def activities(self):
        return ActivitySet([self])
